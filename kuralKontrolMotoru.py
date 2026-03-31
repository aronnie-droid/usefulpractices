import arcpy
import csv

def evaluate(val, operator, rule_val):
    if val is None:
        val = ""
    val = str(val).strip()

    if operator == "always": return True
    if operator == "is_empty": return val == ""
    if operator == "not_empty": return val != ""
    if operator == "in":
        return val in [v.strip() for v in rule_val.split("|")]
    if operator == "not_in":
        return val not in [v.strip() for v in rule_val.split("|")]
    if operator == "starts_with":
        prefixes = [p.strip() for p in rule_val.split("|")]
        return any(val.startswith(p) for p in prefixes)
    
    return False

def main():
    target_fc = arcpy.GetParameterAsText(0)  
    rule_csv = arcpy.GetParameterAsText(1)   
    note_field = arcpy.GetParameterAsText(2) 

    arcpy.AddMessage("Adım 1: Kurallar CSV'den okunuyor...")
    
    rules = {}
    rule_count = 0
    
    # EN ÖNEMLİ DÜZELTME: 'utf-8-sig' görünmez BOM karakterini temizler
    with open(rule_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            # Sütun adlarındaki olası boşlukları da temizleyerek yeni bir dict oluştur
            clean_row = { (k.strip() if k else ''): v for k, v in row.items() }
            
            ak = clean_row.get('alt_kullanim', '').strip()
            if not ak: continue
            
            # Eğer sayı 25.0 gibi gelirse .0 kısmını at (Eşleşme garantisi için)
            if ak.endswith('.0'): ak = ak[:-2]
                
            if ak not in rules:
                rules[ak] = []
            rules[ak].append(clean_row)
            rule_count += 1

    arcpy.AddMessage(f"-> BAŞARILI: CSV'den toplam {rule_count} kural hafızaya alındı!")
    arcpy.AddMessage(f"-> Kural bulunan alt_kullanim kodları: {', '.join(rules.keys())}")

    arcpy.AddMessage("Adım 2: Katman alanları analiz ediliyor...")
    field_names = [f.name for f in arcpy.ListFields(target_fc)]
    idx_map = {name.lower(): i for i, name in enumerate(field_names)}
    
    if "alt_kullanim" not in idx_map:
        arcpy.AddError("'alt_kullanim' alanı katmanda bulunamadı!")
        return
    if note_field.lower() not in idx_map:
        arcpy.AddError(f"'{note_field}' alanı katmanda bulunamadı!")
        return

    alt_kullanim_idx = idx_map["alt_kullanim"]
    kontrol_idx = idx_map[note_field.lower()]

    arcpy.AddMessage("Adım 3: Kayıtlar taranıyor...")
    
    update_count = 0
    match_count = 0
    
    with arcpy.da.UpdateCursor(target_fc, field_names) as cursor:
        for row in cursor:
            row_list = list(row)
            
            # Veritabanındaki alt kullanım değerini al ve temizle
            val_raw = row_list[alt_kullanim_idx]
            if val_raw is None: val_raw = ""
            alt_kul_val = str(val_raw).strip()
            if alt_kul_val.endswith('.0'): alt_kul_val = alt_kul_val[:-2]
            
            mevcut_not = row_list[kontrol_idx]
            if mevcut_not is None: mevcut_not = ""

            mesajlar = []

            # Eşleşme kontrolü
            if alt_kul_val in rules:
                match_count += 1
                for r in rules[alt_kul_val]:
                    cond_f = r.get('condition_field', '').strip().lower()
                    cond_op = r.get('condition_operator', '').strip()
                    cond_v = r.get('condition_value', '')

                    check_f = r.get('check_field', '').strip().lower()
                    check_op = r.get('check_operator', '').strip()
                    check_v = r.get('check_value', '')
                    
                    sev = r.get('severity', '').upper()
                    cat = r.get('category', '').upper()
                    msg = r.get('message', '')

                    # Koşul Aşaması
                    cond_result = True
                    if cond_f and cond_f != "null":
                        if cond_f not in idx_map:
                            mesajlar.append(f"[SİSTEM] Alan Yok: {cond_f}")
                            continue 
                        val = row_list[idx_map[cond_f]]
                        cond_result = evaluate(val, cond_op, cond_v)

                    # Kontrol Aşaması
                    if cond_result:
                        if not check_f or check_f == "null":
                            continue 
                            
                        if check_f not in idx_map:
                            mesajlar.append(f"[SİSTEM] Alan Yok: {check_f}")
                            continue

                        val2 = row_list[idx_map[check_f]]
                        check_result = evaluate(val2, check_op, check_v)

                        if check_result:
                            mesajlar.append(f"[{sev}][{cat}] {msg}")

            if mesajlar:
                yeni_mesaj = " | ".join(mesajlar)
                
                if mevcut_not:
                    final_not = mevcut_not
                    for m in mesajlar:
                        if m not in mevcut_not:
                            final_not += f" | {m}"
                else:
                    final_not = yeni_mesaj

                if final_not != mevcut_not:
                    row_list[kontrol_idx] = final_not
                    cursor.updateRow(row_list)
                    update_count += 1

    arcpy.AddMessage(f"-> İSTATİSTİK: 12.000+ kayıttan {match_count} tanesinin alt_kullanim kodu kurallarla EŞLEŞTİ.")
    arcpy.AddMessage(f"-> İŞLEM TAMAMLANDI! Toplam {update_count} satıra başarıyla not düşüldü.")

if __name__ == '__main__':
    main()
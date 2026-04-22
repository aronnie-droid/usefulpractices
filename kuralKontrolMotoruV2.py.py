import arcpy
import csv
import os

def evaluate(val, operator, rule_val):
    if val is None: val = ""
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
    # PARAMETRELER
    input_fc = arcpy.GetParameterAsText(0)   # Orijinal Veri (Giriş)
    output_fc = arcpy.GetParameterAsText(1)  # Yeni Oluşturulacak Veri (Çıkış)
    rule_csv = arcpy.GetParameterAsText(2)   # Kurallar
    note_field = arcpy.GetParameterAsText(3) # Not Yazılacak Alan

    arcpy.AddMessage("Adım 1: Veri yeni konuma kopyalanıyor...")
    # Orijinal veriyi bozmamak için kopyasını oluşturuyoruz
    if arcpy.Exists(output_fc):
        arcpy.management.Delete(output_fc)
    
    # Veri tipine göre kopyalama (Feature Class veya Table)
    desc = arcpy.Describe(input_fc)
    if desc.dataType == "FeatureLayer" or desc.dataType == "FeatureClass":
        arcpy.management.CopyFeatures(input_fc, output_fc)
    else:
        arcpy.management.Copy(input_fc, output_fc)

    # Not yazılacak alan yoksa yeni veriye ekle
    fields = [f.name for f in arcpy.ListFields(output_fc)]
    if note_field not in fields:
        arcpy.AddMessage(f"-> {note_field} alanı oluşturuluyor...")
        arcpy.management.AddField(output_fc, note_field, "TEXT", field_length=1000)

    arcpy.AddMessage("Adım 2: Kurallar CSV'den okunuyor...")
    rules = {}
    with open(rule_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            clean_row = { (k.strip() if k else ''): v for k, v in row.items() }
            ak = clean_row.get('alt_kullanim', '').strip()
            if not ak: continue
            if ak.endswith('.0'): ak = ak[:-2]
            if ak not in rules: rules[ak] = []
            rules[ak].append(clean_row)

    arcpy.AddMessage("Adım 3: Kayıtlar taranıyor...")
    all_fields = [f.name for f in arcpy.ListFields(output_fc)]
    idx_map = {name.lower(): i for i, name in enumerate(all_fields)}
    
    alt_kullanim_idx = idx_map["alt_kullanim"]
    kontrol_idx = idx_map[note_field.lower()]

    update_count = 0
    with arcpy.da.UpdateCursor(output_fc, all_fields) as cursor:
        for row in cursor:
            row_list = list(row)
            val_raw = row_list[alt_kullanim_idx]
            alt_kul_val = str(val_raw if val_raw is not None else "").strip()
            if alt_kul_val.endswith('.0'): alt_kul_val = alt_kul_val[:-2]
            
            mesajlar = []
            if alt_kul_val in rules:
                for r in rules[alt_kul_val]:
                    cond_f = r.get('condition_field', '').strip().lower()
                    cond_op = r.get('condition_operator', '').strip()
                    cond_v = r.get('condition_value', '')
                    check_f = r.get('check_field', '').strip().lower()
                    check_op = r.get('check_operator', '').strip()
                    check_v = r.get('check_value', '')
                    msg = f"[{r.get('severity','').upper()}][{r.get('category','').upper()}] {r.get('message','')}"

                    # Koşul Kontrolü
                    res = True
                    if cond_f and cond_f != "null" and cond_f in idx_map:
                        res = evaluate(row_list[idx_map[cond_f]], cond_op, cond_v)
                    
                    # Kontrol Kontrolü
                    if res and check_f and check_f in idx_map:
                        if evaluate(row_list[idx_map[check_f]], check_op, check_v):
                            mesajlar.append(msg)

            if mesajlar:
                row_list[kontrol_idx] = " | ".join(mesajlar)
                cursor.updateRow(row_list)
                update_count += 1

    arcpy.AddMessage(f"-> İŞLEM TAMAMLANDI! Orijinal veri korundu.")
    arcpy.AddMessage(f"-> Yeni veri şuraya oluşturuldu: {output_fc}")
    arcpy.AddMessage(f"-> Toplam {update_count} hatalı kayıt işaretlendi.")

if __name__ == '__main__':
    main()
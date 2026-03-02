# Meraklısınıa kolaylaştırıcı notlar

## Gündelik

- Google maps, Harita istanbul gibi panaromik görüntü sitelerinde sokak görünümündeyken **WASD** ve ok tuşlarıyla gezinme yapılabiliyor.
- ArcGIS Pro'da **Ctrl + Alt + L** kısayolu select by location penceresini açar. **Ctrl + Alt + T** ise Select by attributes penceresini açar. *[Daha fazla kısayol için ekli pdf dosyasına bakabilirsin](https://www.esri.com/content/dam/esrisites/en-us/media/products/arcgis-pro-issues-addressed/shortcut-keys/3-6/arcgis-pro-keyboard-shortcuts-en.pdf)*

- Map görünümünde selected features sayısının yazdığı yere tıklamak o seçili objelere zoom yapar.
- ![Map görünümü selected features alanı](https://raw.githubusercontent.com/aronnie-droid/public-photos-documents-etc/refs/heads/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202026-02-23%20101533.png)
- Çok sayıda katman açıkken zoom out vs yapma ve **map**in yüklenmesini bekleme gibi bir durumla karşılaştığımda buranın iki sağındaki pause tuşu ⏸️ renderlamayı durdurur. Pek işlevseldir.

## Kodlamalık

>Bu satırdaki komutla arcgis pro içindeki python konsolunda hızlıca select by attributes yapabilirsin. Ben bunu o gün editlediğim poligonlara hızlıca bakmak için kullanıyorum.

    arcpy.management.SelectLayerByAttribute("detayli_ak", "NEW_SELECTION", "ilce = 2054 AND last_edited_user = 'user_name' AND last_edited_date > DATE '2026-02-23'")

>ilce kolonunda domain kullanıldığı için çalışılan ilçenin UAVT kodunu yazmak gerekiyor. Sancaktepe için ilce = 2054 last_edited_date için tarih girildiğinde o tarihteki 00:00:00 satini kabul ediyor. Gece 12'den sonra yapılan editlerin tümü görünür.
>BUNUN GİBİ İHTİYAÇ OLAN PRATİK SATIRLAR GEREKİYORSA KONUŞUP BULALIM

---

## Kontrol yöntemleri
Field calculator içinde arcade kullanarak kontrol_ipa kolonuna kontrol yorumları yazdırabliriz. Bu, kontrol_ipa kolonu için çalıştırıldığında ilgili kayıtlara not düşen basit bir örnek. alt_kullanim değeri için coded value domain'in kodlarını girerek kontrol etmek gerekiyor. En yaygın fonksiyondan en nadir fonksiyona doğru çapraz tablo kontrollerini listeleyelim.
| alt_kullanim           | Kural | Arcade |
| -----------------------| ----------- | ---|
| 1 - Kentsel Konut Alanı| "detay_konut" kolonu boş olamaz. | Hazır |
| 1 - Kentsel Konut Alanı| (Site) sınıfındaki konut alanlarında "ad" kolonu boş olamaz. | Hazır |
| 8 - Ticaret Konut Alanı| (Site) sınıfındaki konut alanlarında "ad" kolonu boş olamaz. | **Hazır Değil** |
| 8 - Ticaret Konut Alanı| "detay_konut" kolonu boş olamaz. | **Hazır Değil** |
| 8 - Ticaret Konut Alanı| "detay_ticaret" kolonu boş olamaz. | **Hazır Değil** |
| 8 - Ticaret Konut Alanı| "nacekodu" kolonu boş olamaz. | **Hazır Değil** |

--- 
        if ($feature.alt_kullanim == "1" && IsEmpty($feature.detay_konut)) {
            return "DETAY_KONUT alanı boş bırakılamaz.";
        }
        return null;
        
        //-------------------------------------------------------------------------------------------------
        
        var mevcutNot = $feature.kontrol;

        var siteKodlari = ["2","4","6"];

        var konutMu = $feature.alt_kullanim == "1";
        var siteTipi = Includes(siteKodlari, $feature.detay_konut);
        var adBos = IsEmpty($feature.AD);

        if (konutMu && siteTipi && adBos) {

            var yeniMesaj = "Ad girilmeli";

            // Eğer mevcut not boşsa direkt yaz
            if (IsEmpty(mevcutNot)) {
                return yeniMesaj;
            }
            // Eğer zaten aynı mesaj varsa tekrar ekleme
            else if (Find(yeniMesaj, mevcutNot) > -1) {
                return mevcutNot;
            }
            // Mevcut not varsa sonuna ekle
            else {
                return mevcutNot + " | " + yeniMesaj;
            }
        }

        // Şart sağlanmıyorsa mevcut değeri koru
        return mevcutNot;
---

        var mevcutNot = $feature.kontrol_ipa;

        var siteKodlari = ["2","4","6"];

        var konutMu = $feature.alt_kullanim == "1";
        var detayBos = IsEmpty($feature.detay_konut);
        var siteTipi = Includes(siteKodlari, $feature.detay_konut);
        var adBos = IsEmpty($feature.AD);

        var mesajlar = [];

        // KURAL 1 → Detay konut boş
        if (konutMu && detayBos) {
            Push(mesajlar, "Detay konut girilmeli");
        }

        // KURAL 2 → Site tipi + AD boş
        if (konutMu && siteTipi && adBos) {
            Push(mesajlar, "Ad girilmeli");
        }

        // Eğer yeni mesaj yoksa hiç dokunma
        if (Count(mesajlar) == 0) {
            return;
        }

        // Mesajları birleştir
        var yeniMesaj = Concatenate(mesajlar, " | ");

        var sonuc;

        // Hücre boşsa direkt yaz
        if (IsEmpty(mevcutNot)) {
            sonuc = yeniMesaj;
        }
        else {

            sonuc = mevcutNot;

            // Her mesajı kontrol edip yoksa ekle
            for (var m in mesajlar) {
                if (Find(m, sonuc) == -1) {
                    sonuc = sonuc + " | " + m;
                }
            }
        }

        // SADECE gerçekten değişiklik varsa update yap
        if (sonuc != mevcutNot) {
            return sonuc;
        }

        return;

## Veri Temin Edilebilecek Linkler (Crawl)
[MEB Özel Öğretim Kurumları Genel Müdürlüğü tüm özel öğretim kurumları listesi](https://ookgm.meb.gov.tr/kurumlar.php?sayfa=7&tur=okul&il=%C4%B0STANBUL&tur2=0) *Açık adres* içeren tablo bazlı veri bulunuyor. **crawl + geocode** ile haritaya alınabilir (15.10.2025 tarihli)
## Faydalı Linkler
1. [Harita İstanbul](harita.istanbul)
2. [İBB Şehir Haritası](https://sehirharitasiapi.ibb.gov.tr)
3. [İBB Şehir Haritası API Reference](https://sehirharitasiapi.ibb.gov.tr/developer/index.html)
4. 

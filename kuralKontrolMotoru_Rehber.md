# Kural Kontrol Motoru

Daha önce Arcade Engine ve Attribute Rules/Field Calculator üzerinden yürüttüğümüz hesaplama süreçlerini daha kapsamlı ve ölçeklenebilir olan **ArcGIS Pro Geoprocessing (GP) Tools** yapısına taşıdık.

Aşağıdaki rehber, GitHub'daki Arcade dokümantasyonumuza benzer bir yapıda, ekibimizin GP Tool ekosistemine geçişini kolaylaştırmak için hazırlanmıştır.

---

# ArcGIS Pro Geoprocessing Tool Eğitim Notu

Bu doküman, Arcade ile yapılan satır bazlı hesaplamaların ötesine geçerek, karmaşık veri manipülasyonlarını ve toplu işlemleri **Python (ArcPy)** kullanarak nasıl GP Tool haline getireceğimizi özetler.

## 1. Neden Arcade'den GP Tool'a Geçiyoruz?

| **Özellik**    | **Arcade (Attribute Rules/Calc)**  | **Geoprocessing Tool (Python)**                        |
| --------------------- | ---------------------------------------- | ------------------------------------------------------------ |
| **Kapsam**      | Sadece ilgili katman/satır.             | Tüm proje, harici veri tabanları ve dosyalar.              |
| **Performans**  | Düzenleme anında hızlı (on-the-fly). | Büyük veri setlerinde toplu işlemlerde çok daha hızlı. |
| **Kütüphane** | Kısıtlı Arcade fonksiyonları.        | Pandas, NumPy, Request gibi tüm Python dünyası.           |
| **Etkileşim**  | Otomatiktir, kullanıcıdan girdi almaz. | Kullanıcı dostu arayüz ile parametre girişi sağlar.     |

---

## 2. GP Tool Yapılandırması (Adım Adım)

Bir GP Tool oluşturmak için izlememiz gereken standart iş akışı şu şekildedir:

### A. Toolbox Oluşturma

1. **Catalog** panelinde projenize sağ tıklayın.
2. `New > Toolbox (.atbx)` seçeneğini seçin.
3. Toolbox içerisine sağ tıklayarak `New > Script` yolunu izleyin.

### B. Parametre Tanımlama

Arcade'de değişkenleri kod içinde tanımlıyorduk, GP Tool'da ise kullanıcıdan alıyoruz. **Parameters** sekmesinde şunları mutlaka tanımlayın:

* **Input Features:** İşlem yapılacak katman.
* **Target Field:** Hesaplanacak alan.
* **Filter Criteria (Opsiyonel):** SQL sorgusu için metin kutusu.

---

## 3. Kod Yapısı ve Mantığı

Arcade'deki `$feature.FieldName` mantığının yerini burada `arcpy.da.UpdateCursor` veya `arcpy.management.CalculateField` alır.

### Örnek Şablon:

Ekibimizin kullanacağı standart Python script yapısı şöyledir:

**Python**

```
import arcpy

def execute_calculation(input_fc, field_name):
    try:
        # 1. Parametreleri Al
        arcpy.AddMessage(f"İşlem başlatıldı: {input_fc}")
    
        # 2. Hesaplama Mantığı (Arcade'deki Expression'ın karşılığı)
        # UpdateCursor ile satır satır dönme (En kontrollü yöntem)
        with arcpy.da.UpdateCursor(input_fc, [field_name, "SHAPE@AREA"]) as cursor:
            for row in cursor:
                # Örn: Alanı hektara çevirip yazdır
                row[0] = row[1] / 10000 
                cursor.updateRow(row)
    
        arcpy.AddMessage("Hesaplama başarıyla tamamlandı.")
    
    except Exception as e:
        arcpy.AddError(f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    # Tool arayüzünden gelen değerleri yakala
    fc = arcpy.GetParameterAsText(0)
    field = arcpy.GetParameterAsText(1)
    execute_calculation(fc, field)
```

---

## 4. Kritik Farklar ve İpuçları

Arcade'den GP Tool'a geçerken şu "çeviri" tablosunu kullanabilirsiniz:

* **Geometry İşlemleri:** Arcade'deki `Area($feature)` yerine ArcPy'da `!shape.area!` veya `SHAPE@AREA` (Cursor içinde) kullanın.
* **Global Değişkenler:** Arcade'deki `$datastore` yerine `arcpy.Describe()` veya doğrudan veritabanı yolunu kullanın.
* **Hata Ayıklama:** Arcade'de `Console()` kullanırken, GP Tool'da `arcpy.AddMessage()` kullanıyoruz. Bu mesajlar ArcGIS Pro'nun **History** panelinde görünür.

---

## 5. Doğrulama (Validation) Kuralları

GP Tool'un en güçlü yanı, kullanıcı henüz "Run" butonuna basmadan hataları yakalayabilmesidir. Tool özelliklerindeki **Validation** sekmesini kullanarak:

* Kullanıcının yanlış veri tipi seçmesini engelleyebilirsiniz.
* Sadece belirli isimdeki alanların (Field) listelenmesini sağlayabilirsiniz.

> **⚠️ Not:** Yeni oluşturduğunuz script araçlarını projenize eklemeden önce mutlaka `Analysis > History` sekmesinden önceki denemelerin çıktılarını kontrol edin.

---

Bu yeni yapı, projelerimizdeki veri tutarlılığını artıracak ve manuel hesaplama yükümüzü minimize edecektir. Takıldığınız noktalarda eski Arcade scriptlerini iletirseniz, bunları hızlıca Python fonksiyonlarına dönüştürebiliriz.

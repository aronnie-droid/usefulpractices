# IPA Kontrol Sistemi – Ekip İçi Eğitim Notu

## Amaç

Bu sistemin amacı, CBS verisi üzerindeki kontrolleri **Arcade + kural tablosu (CSV)** kullanarak dinamik ve sürdürülebilir hale getirmektir.

Yeni kontrol ihtiyaçlarında Arcade scriptinin değiştirilmesi yerine yalnızca **kural tablosuna yeni satır eklenmesi** yeterlidir.

---

## Sistem Mimarisi

Sistem üç ana bileşenden oluşur:

### 1. Arcade Engine

Dosya: `proArcadeEngine2.js`

Bu script:

* Kural tablosunu okur
* Her feature için uygun kuralları filtreler
* Kuralları çalıştırır
* Sonuçları `kontrol` alanına yazar

---

### 2. Kural Tablosu

Dosya: `full_rule_table.csv`

Her satır bir kontrol kuralını temsil eder.

---

### 3. Domain Tabloları

Dosya: `naceDomains.csv` NACE Kodu domain açıklamalarını içerir. 
Dosya: `domains.csv` Alt Kullanım domain açıklamalarını içerir.

---

## Arcade Engine Çalışma Prensibi

### Kural Tablosunun Okunması

```javascript
var rules = FeatureSetByName($datastore, "full_rule_table", [...]);
```

Sistem `full_rule_table` içerisindeki tüm kuralları okur.

---

### Kural Filtreleme

```javascript
var filteredRules = Filter(rules, "alt_kullanim = '" + alt + "'");
```

Sadece ilgili `alt_kullanim` değerine sahip kurallar çalıştırılır.

---

### Kural Döngüsü

```javascript
for (var r in filteredRules)
```

Her satır bağımsız bir kontrol olarak değerlendirilir.

---

## Kural Tablosu Alanları (full_rule_table.csv)

### 1. alt_kullanim

Kuralın hangi veri grubuna uygulanacağını belirler.

Örnek:

* `1` → Konut Alanı
* `8` → Ticaret + Konut
* `38` → Anaokulu

---

### 2. condition_field

Kuralın çalışması için gerekli ön koşul alanıdır.

---

### 3. condition_operator

Ön koşulun nasıl değerlendirileceğini belirler.

Desteklenen operatörler:

| Operatör    | Açıklama                         |
| ----------- | -------------------------------- |
| always      | Her zaman çalışır                |
| is_empty    | Alan boş mu kontrolü             |
| not_empty   | Alan dolu mu kontrolü            |
| in          | Değer listede var mı             |
| not_in      | Değer listede yok mu             |
| starts_with | Belirli karakter ile başlıyor mu |

---

### 4. condition_value

Operatöre bağlı kontrol değeridir.

Örnek:

* `2|4|6` → liste kontrolü
* `C|T` → başlangıç karakteri kontrolü

---

### 5. check_field

Kontrol edilecek asıl alanı ifade eder.

---

### 6. check_operator

Bu alan üzerinde yapılacak kontrolü belirler.

Örnek:

* `is_empty`
* `not_empty`
* `in`

---

### 7. check_value

Kontrol için referans alınan değerdir.

---

### 8. severity

Hata seviyesini belirler.

| Değer   | Açıklama      |
| ------- | ------------- |
| error   | Kritik hata   |
| warning | Uyarı         |
| info    | Bilgilendirme |

Çıktı örneği:

```
[ERROR][GENEL] Detay konut girilmeli
```

---

### 9. category

Hatanın türünü belirtir.

Örnek:

* GENEL
* NACE
* AD
* DETAY

---

### 10. message

Kullanıcıya gösterilecek açıklama metnidir.

---

## Kural Çalışma Mantığı

Genel yapı:

```
Eğer (condition doğruysa)
    ve (check doğruysa)
        → mesaj üret
```

---

## evaluate() Fonksiyonu

```javascript
function evaluate(value, operator, ruleValue)
```

Tüm kontrol işlemleri bu fonksiyon içerisinde gerçekleştirilir.

---

### Desteklenen Operasyonlar

#### is_empty

```javascript
IsEmpty(value)
```

#### in

```javascript
Includes(Split(ruleValue,"|"), val)
```

#### starts_with

```javascript
Left(val,1)
```

---

## Mesaj Üretimi

```javascript
Push(mesajlar, finalMesaj);
```

---

### Mesaj Formatı

```
[SEVERITY][CATEGORY] mesaj
```

---

### Mevcut Notun Korunması

```javascript
if (Find(m,sonuc) == -1)
```

Aynı mesajın tekrar yazılması engellenir.

---

### Güncelleme Davranışı

```javascript
if (Count(mesajlar) == 0) {
    return;
}
```

Hiç mesaj üretilmezse:

* Feature güncellenmez
* Last edited date değişmez

---

## Örnek Kural

```csv
8,,always,,detay_ticaret,is_empty,,error,GENEL,Detay Ticaret girilmeli
```

Anlamı:

* `alt_kullanim = 8` olan kayıtlar için
* `detay_ticaret` alanı boş ise
* hata mesajı üretilir

---

## Sistem Avantajları

* Arcade kodu sabit kalır
* Yeni kural eklemek kolaydır
* Domain yapıları ile uyumludur
* Ölçeklenebilir yapıdadır
* Ekip tarafından yönetilebilir

---

## Geliştirme Alanları

* AND / OR koşul desteği
* İstisna (except) operatörleri
* Regex desteği
* JSON tabanlı kural yapısı

---

## Sonuç

Bu yapı ile:

* Kontroller koddan ayrılmıştır
* Kural yönetimi veri tabanına taşınmıştır
* Sistem sürdürülebilir hale gelmiştir

---

## Not

Kural güncellemeleri yapılmadan önce:

* Domain tabloları kontrol edilmelidir
* Kod ve metin (text) veri tipleri dikkate alınmalıdır

---

Bu yapı ile birlikte kontrol geliştirme yaklaşımı:

“Arcade kodu yazmak” yerine
“kural tanımlamak” olarak değişmiştir.

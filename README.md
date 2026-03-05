# Meraklısınıa kolaylaştırıcı notlar

## Notların düzenlenmiş halini [projenin wiki sayfası](https://github.com/aronnie-droid/usefulpractices/wiki)nda bulabilirsiniz. Artık burada kod snippetleri olacak.
## Kodlar master brancha taşındı. Main daha çok viki amaçlı kalacak

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

**Harita İstanbul uyumlu koordinat üretici snippet**

    #bu kodun çıktısını harita istanbul linkinde doğru yere yapıştırınca mevcut ayarlarla websitesinde o bölgeye zoom yapar
    mv = arcpy.mp.ArcGISProject("CURRENT").activeView
    ext = mv.camera.getExtent()

    center_x = (ext.XMin + ext.XMax) / 2
    center_y = (ext.YMin + ext.YMax) / 2

    sr_map = mv.map.spatialReference
    sr_wgs = arcpy.SpatialReference(4326)

    pt = arcpy.PointGeometry(arcpy.Point(center_x, center_y), sr_map)
    pt_wgs = pt.projectAs(sr_wgs)

    lon = pt_wgs.centroid.X
    lat = pt_wgs.centroid.Y

    zoom = 17

    print(f"{lon:.5f},{lat:.5f},{zoom}")


---

## Kontrol yöntemleri
Field calculator içinde arcade kullanarak kontrol_ipa kolonuna kontrol yorumları yazdırabliriz. Bu, kontrol_ipa kolonu için çalıştırıldığında ilgili kayıtlara not düşen basit bir örnek. alt_kullanim değeri için coded value domain'in kodlarını girerek kontrol etmek gerekiyor. En yaygın fonksiyondan en nadir fonksiyona doğru çapraz tablo kontrollerini listeleyelim.
| alt_kullanim           | Kural | Arcade |
| -----------------------| ----------- | ---|
| 1 - Kentsel Konut Alanı| "detay_konut" kolonu boş olamaz. | Hazır |
| 1 - Kentsel Konut Alanı| (Site) sınıfındaki konut alanlarında "ad" kolonu boş olamaz. | Hazır |
| 1 - Kentsel Konut Alanı| "detay_konut", "ad", "not", kolonları hariç diğer kolonların boş olmasını bekleriz. | **Hazır Değil** |
| 8 - Ticaret Konut Alanı| (Site) sınıfındaki konut alanlarında "ad" kolonu boş olamaz. | **Hazır Değil** |
| 8 - Ticaret Konut Alanı| "detay_konut" kolonu boş olamaz. | **Hazır Değil** |
| 8 - Ticaret Konut Alanı| "detay_ticaret" kolonu boş olamaz. | **Hazır Değil** |
| 8 - Ticaret Konut Alanı| "nacekodu" kolonu boş olamaz. | **Hazır Değil** |

--- 
## Veri Temin Edilebilecek Linkler (Crawl)
[MEB Özel Öğretim Kurumları Genel Müdürlüğü tüm özel öğretim kurumları listesi](https://ookgm.meb.gov.tr/kurumlar.php?sayfa=7&tur=okul&il=%C4%B0STANBUL&tur2=0) *Açık adres* içeren tablo bazlı veri bulunuyor. **crawl + geocode** ile haritaya alınabilir (15.10.2025 tarihli)
## Projeye kapsamında uyulabilecek çerçeveler
Veriyi AI ready şekilde hazırlamak ve bulundurmak. TR'de bununla ilgili başlık içeren bir standart çalışmasını henüz bulamadım. Varsa TR standardına, yoksa UK ya da EU standardına uymayı düşünebiliriz. Arazi kullanımı verisi üretilirken kullanılan tüm altlık veri setlerinin açık veri standardını sağladığı bir evrende veri üretme ve kontrol aşamasının büyük kısmının otomasyona tabi tutulması teorik olarak mümkün. *AGI olsaydı mümkündü?*
>Birleşik Krallık hükümeti, kamu sektörü verilerini yapay zekaya hazır hale getirmek için bir çerçeve geliştirdi. Bu, hükümet veri kümelerinin yüksek kaliteli, iyi yönetilen ve kullanımı kolay olmasını sağlayarak yapay zekanın tüm potansiyelinin ortaya çıkarılmasına yardımcı olacaktır. Yapay zekaya hazır veri, doğru, eksiksiz, tutarlı, güvenli ve hem insanlar hem de makineler tarafından güvenilebilen ve anlaşılabilen meta verilerle zenginleştirilmiş veri anlamına gelir.
>
>Bu yeni çerçeve, Bulunabilir, Erişilebilir, Birlikte Çalışabilir, Yeniden Kullanılabilir (FAIR) prensiplerine dayanarak, yapay zekaya hazır veri kümelerinin hazırlanması için en iyi uygulamaları ortaya koymaktadır. Kalite, yönetişim, meta veri ve API'ler için standartların yanı sıra, insan müdahalesi gerektiren kontroller ve veri yönetimi için net roller gibi gözetim önlemlerini de kapsamaktadır. Bu yaklaşım, Birleşik Krallık'ı yapay zeka için sorumlu veri yönetiminde küresel bir lider olarak konumlandırmayı amaçlamaktadır. [kaynak](https://www.gov.uk/government/publications/making-government-datasets-ready-for-ai#:~:text=AI%20%2Dready%20data%20means%20accurate,Interoperable%2C%20Reusable%20(%20FAIR%20).)
## Faydalı Linkler
1. [Harita İstanbul](harita.istanbul)
2. [İBB Şehir Haritası](https://sehirharitasiapi.ibb.gov.tr)
3. [İBB Şehir Haritası API Reference](https://sehirharitasiapi.ibb.gov.tr/developer/index.html)
4. [AI Ready Data Standards](https://www.ibm.com/think/topics/ai-ready-data)

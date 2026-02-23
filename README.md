# Meraklısınıa kolaylaştırıcı notlar

## Gündelik

- Google maps, Harita istanbul gibi panaromik görüntü sitelerinde sokak görünümündeyken **WASD** ve ok tuşlarıyla gezinme yapılabiliyor.
- ArcGIS Pro'da **Ctrl + Alt + L** kısayolu select by location penceresini açar. **Ctrl + Alt + T** ise Select by attributes penceresini açar. *[Daha fazla kısayol için ekli pdf dosyasına bakabilirsin](https://www.esri.com/content/dam/esrisites/en-us/media/products/arcgis-pro-issues-addressed/shortcut-keys/3-6/arcgis-pro-keyboard-shortcuts-en.pdf)*

- Map görünümünde selected features sayısının yazdığı yere tıklamak o seçili objelere zoom yapar.
- ![Map görünümü selected features alanı](https://raw.githubusercontent.com/aronnie-droid/public-photos-documents-etc/refs/heads/main/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202026-02-23%20101533.png)
- Çok sayıda katman açıkken zoom out vs yapma ve **map**in yüklenmesini bekleme gibi bir durumla karşılaştığımda buranın hemen solundaki pause tuşu ⏸️ renderlamayı durdurur. Pek işlevseldir.

## Kodlamalık

>Bu satırdaki komutla arcgis pro içindeki python konsolunda hızlıca select by attributes yapabilirsin. Ben bunu o gün editlediğim poligonlara hızlıca bakmak için kullanıyorum.

    arcpy.management.SelectLayerByAttribute("detayli_ak", "NEW_SELECTION", "ilce = 2054 AND last_edited_user = 'user_name' AND last_edited_date > DATE '2026-02-23'")

>ilce kolonunda domain kullanıldığı için çalışılan ilçenin UAVT kodunu yazmak gerekiyor. Sancaktepe için ilce = 2054 last_edited_date için tarih girildiğinde o tarihteki 00:00:00 satini kabul ediyor. Gece 12'den sonra yapılan >editlerin tümü görünür.
>BUNUN GİBİ İHTİYAÇ OLAN PRATİK SATIRLAR GEREKİYORSA KONUŞUP BULALIM

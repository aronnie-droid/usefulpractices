import arcpy
import webbrowser
import os
import tempfile

class Toolbox(object):
    def __init__(self):
        self.label = "Harita Linkleri Kutusu"
        self.alias = "haritalink"
        self.tools = [LinkUretici]

class LinkUretici(object):
    def __init__(self):
        self.label = "Merkez Koordinat Linklerini Üret"
        self.description = "Aktif harita görünümünün merkezini alarak linkleri tarayıcıda açar."
        self.canRunInBackground = False

    def getParameterInfo(self):
        return []

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        pass

    def updateMessages(self, parameters):
        pass

    def execute(self, parameters, messages):
        try:
            aprx = arcpy.mp.ArcGISProject("CURRENT")
            mv = aprx.activeView

            if mv is None or not hasattr(mv, "camera"):
                arcpy.AddError("Aktif bir harita görünümü yok. Lütfen bir harita ekranına tıklayıp tekrar deneyin.")
                return

            ext = mv.camera.getExtent()
            sr = mv.map.spatialReference
            
            # Koordinatı WGS84'e (4326) çevir
            pt = arcpy.PointGeometry(
                arcpy.Point((ext.XMin+ext.XMax)/2, (ext.YMin+ext.YMax)/2), sr
            ).projectAs(arcpy.SpatialReference(4326))
            
            lon, lat = pt.centroid.X, pt.centroid.Y
            
            # Tıklanabilir butonların olduğu bir HTML sayfası oluştur
            html_content = f"""
            <html>
            <head>
                <title>Harita Linkleri</title>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f4f4f9; }}
                    .container {{ background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }}
                    h2 {{ color: #333; font-size: 18px; margin-bottom: 5px; text-align: center; }}
                    .coords {{ color: #666; font-size: 14px; margin-bottom: 20px; text-align: center; }}
                    a {{ display: block; padding: 12px; margin-bottom: 10px; background-color: #0078d7; color: white; text-decoration: none; border-radius: 4px; text-align: center; font-weight: bold; font-size: 14px; transition: background-color 0.3s; }}
                    a:hover {{ background-color: #005a9e; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>📍 Anlık Merkez Koordinatı</h2>
                    <div class="coords">Enlem: {lat:.5f} | Boylam: {lon:.5f}</div>
                    <a href="https://harita.istanbul/2d?@={lon:.5f},{lat:.5f},18&ms=!b241!c" target="_blank">Harita.İst 2D</a>
                    <a href="https://harita.istanbul/3d?@={lon:.5f},{lat:.5f},18" target="_blank">Harita.İst 3D</a>
                    <a href="https://www.google.com/maps/@{lat:.5f},{lon:.5f},18z" target="_blank">Google Maps</a>
                    <a href="https://yandex.com.tr/maps/?ll={lon:.5f}%2C{lat:.5f}&z=17&l=sat" target="_blank">Yandex Maps</a>
                    <a href="https://earth.google.com/web/@{lat:.5f},{lon:.5f},1000a,17d,35y,0h,0t,0r" target="_blank">Google Earth</a>
                </div>
            </body>
            </html>
            """
            
            # Geçici bir HTML dosyası olarak kaydet
            temp_dir = tempfile.gettempdir()
            html_path = os.path.join(temp_dir, "harita_linkleri.html")
            
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            # Dosyayı varsayılan web tarayıcısında aç
            webbrowser.open('file://' + os.path.realpath(html_path))
            
            arcpy.AddMessage("Linkler tarayıcınızda yeni bir sekmede açıldı!")

        except Exception as e:
            arcpy.AddError(f"Bir hata oluştu: {str(e)}")
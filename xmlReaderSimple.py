import requests
import xml.etree.ElementTree as ET

# URL of the XML
rss_url = "https://www.mgm.gov.tr/FTPDATA/analiz/sonSOA.xml"

# Download and decode the XML
response = requests.get(rss_url)
response.encoding = 'utf-8'

# Parse the XML content
root = ET.fromstring(response.text)

# Extract general info
genel_durum = root.findtext(".//GenelDurum", default="Veri bulunamadı.").strip()
periyot_baslama = root.findtext(".//PeryotBaslama", default="Bilinmiyor")
periyot_bitis = root.findtext(".//PeryotBitis", default="Bilinmiyor")

print("📰 Genel Hava Durumu\n")
print(f"🕒 Dönem: {periyot_baslama} → {periyot_bitis}")
print(f"📌 Genel Durum: {genel_durum}")
print("\n" + "="*60 + "\n")

# Extract region-based weather summaries
print("🔎 Bölgesel Hava Durumu Tahminleri:\n")
for i in range(8):
    region_tag = f"BolgeAdi{i}"
    forecast_tag = f"BolgeDurum{i}"

    region_elem = root.find(f".//{region_tag}")
    forecast_elem = root.find(f".//{forecast_tag}")

    if region_elem is not None and forecast_elem is not None:
        print(f"📍 {region_elem.text}")
        print(f"{forecast_elem.text.strip()}\n{'-'*60}")

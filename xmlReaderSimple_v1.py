import requests
import xml.etree.ElementTree as ET

rss_url = "https://www.mgm.gov.tr/FTPDATA/analiz/sonSOA.xml"

def get_xml_data(rss_url):
    response = requests.get(rss_url)
    response.encoding = 'utf-8'
    root = ET.fromstring(response.text)
    return root

def get_weather_summary():
    try:
        root = get_xml_data(rss_url)
        genel_durum = root.findtext(".//GenelDurum", default="Veri bulunamadı.").strip()
        periyot_baslama = root.findtext(".//PeryotBaslama", default="Bilinmiyor")
        periyot_bitis = root.findtext(".//PeryotBitis", default="Bilinmiyor")

        text = f"📰 Genel Hava Durumu\n\n"
        text += f"🕒 Dönem: {periyot_baslama} → {periyot_bitis}\n"
        text += f"📌 Genel Durum: {genel_durum}\n\n"
        text += "="*50 + "\n\n"
        text += "🔎 Bölgesel Hava Durumu Tahminleri:\n\n"

        for i in range(8):
            region = root.findtext(f".//BolgeAdi{i}")
            forecast = root.findtext(f".//BolgeDurum{i}")
            if region and forecast:
                text += f"📍 {region}\n{forecast.strip()}\n{'-'*50}\n"

        return text
    except Exception as e:
        return f"Veri alınamadı.\n\nHata: {e}"


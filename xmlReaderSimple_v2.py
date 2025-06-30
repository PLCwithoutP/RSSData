import requests
import xml.etree.ElementTree as ET
import unicodedata

rss_url = "https://www.mgm.gov.tr/FTPDATA/analiz/sonSOA.xml"

def normalize(text):
    return unicodedata.normalize("NFKD", text).casefold().strip()

def get_xml_data(rss_url):
    response = requests.get(rss_url)
    response.encoding = 'utf-8'
    root = ET.fromstring(response.text)
    return root

def get_general():
    try:
        root = get_xml_data(rss_url)
        genel_durum = root.findtext(".//GenelDurum", default="Veri bulunamadı.").strip()
        periyot_baslama = root.findtext(".//PeryotBaslama", default="Bilinmiyor")
        periyot_bitis = root.findtext(".//PeryotBitis", default="Bilinmiyor")

        return (
            f"📰 Genel Hava Durumu\n\n"
            f"🕒 Dönem: {periyot_baslama} → {periyot_bitis}\n"
            f"📌 Genel Durum:\n{genel_durum}"
        )
    except Exception as e:
        return f"Genel veri alınamadı.\n\nHata: {e}"

def get_regional():
    try:
        root = get_xml_data(rss_url)
        regional_summaries = {}
        for i in range(8):
            region = root.findtext(f".//BolgeAdi{i}")
            forecast = root.findtext(f".//BolgeDurum{i}")
            if region and forecast:
                regional_summaries[f"region_{i}"] = (
                    f"📍 {region}\n\n"
                    f"{forecast.strip()}"
                )
        return regional_summaries
    except Exception as e:
        return {"error": f"Bölgesel veri alınamadı.\n\nHata: {e}"}

def get_city_data(city_name):
    try:
        root = get_xml_data(rss_url)
        city_entries = []

        for sehir in root.findall(".//sehirler"):
            city = sehir.findtext("ili", "").strip()
            if normalize(city) == normalize(city_name):
                bolge = sehir.findtext("Bolge", "Bilinmiyor")
                peryot = sehir.findtext("Peryot", "Bilinmiyor")
                merkez = sehir.findtext("Merkez", "Bilinmiyor")
                durum = sehir.findtext("Durum", "Bilinmiyor")
                mak = sehir.findtext("Mak", "–")
                min_ = sehir.findtext("Min", "–")

                city_entries.append(
                    f"📍 {merkez} ({bolge})\n"
                    f"🕑 {peryot}\n"
                    f"🌤️ Durum: {durum}\n"
                    f"🌡️ Maks: {mak}°C | Min: {min_}°C\n"
                    f"{'-'*40}"
                )

        if not city_entries:
            return f"Şehir verisi bulunamadı: {city_name}"

        return "\n".join(city_entries)

    except Exception as e:
        return f"Şehir verisi alınamadı.\n\nHata: {e}"


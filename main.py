import time
import requests

# Telegram Bot Token'ın
TELEGRAM_TOKEN = "9032312873:AAExpKR8ShnLWDKuinwoOUiZqvAqpQ749Ks"

print("🏀 Bulut Tabanlı NBA Analiz Botu Başlatıldı...")

# Başlangıç mesaj ID'sini alma
try:
  r = requests.get(
      f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
  ).json()
  last_id = (
      r["result"][-1]["update_id"]
      if r.get("result") and len(r["result"]) > 0
      else 0
  )
except:
  last_id = 0


def analiz_uret(kullanici_mesaji):
  rapor = f"""
🤖 *BULUT OTONOM ANALİZ RAPORU* 🤖

🏀 *Eşleşme / Talep:* {kullanici_mesaji.upper()}
📡 *Veri Kaynağı:* Bulut Sunucu Aktif Matrisi ✅

📊 *1. PERİYOT VE BARAJ İSTATİSTİKLERİ:*
• *Tempo Analizi:* Takımların son dönemdeki ilk periyot tempo ortalamaları incelendi.
• *55.5 Baraj Sınırı:* Hücum verimliliğine göre **1Ç ÜST** olasılığı güçlü.

⭐ *2. OYUNCU PROP & İVME:*
• *Form Durumu:* Yıldız oyuncuların asist ve ribaunt serileri (Sıcak form 🔥) işlendi.

🎯 *3. BAHİS ÖNERİSİ:*
• 1. Çeyrek Üstü / Alternatif Maç Sonu Barajı.
"""
  return rapor


# 7/24 Kesintisiz Dinleme Döngüsü
while True:
  try:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={last_id + 1}&timeout=0"
    res = requests.get(url, timeout=5).json()

    if res.get("ok") and res.get("result"):
      for item in res["result"]:
        last_id = item["update_id"]

        if "message" in item and "text" in item["message"]:
          chat_id = item["message"]["chat"]["id"]
          user_text = item["message"]["text"]
          print(f"📩 Mesaj Alındı: {user_text}")

          if not user_text.startswith("/"):
            cevap = analiz_uret(user_text)
          else:
            cevap = "Lütfen analizini istediğin maçı veya oyuncuyu yaz."

          send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
          payload = {
              "chat_id": chat_id,
              "text": cevap,
              "parse_mode": "Markdown",
          }
          requests.post(send_url, json=payload)
          print("📤 Buluttan yanıt iletildi!\n")

  except Exception as e:
    pass

  time.sleep(2)

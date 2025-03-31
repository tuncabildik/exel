import time
from datetime import datetime
import csv
from price_tracker import FiyatTakipci

print("Programın başlangıcı - modüller içe aktarılıyor...")

# Takip sınıfını başlat
print("FiyatTakipci sınıfı başlatılıyor...")
takipci = FiyatTakipci()
print("FiyatTakipci sınıfı başlatıldı.")

# Saat aralıkları (dakika cinsinden)
saat_araliklari = [4, 8, 10, 12]

while True:
    print("\nYeni döngü başlatılıyor...\n")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for rota, url in takipci.urls.items():
        for saat in saat_araliklari:
            print(f"\n🔍 Rota: {rota} | Saat: {saat} saat")
            try:
                fiyat, tedarikci, arac, tum_sonuclar = takipci.get_all_prices_and_suppliers(saat, url)
                if tum_sonuclar:
                    for sonuc in tum_sonuclar:
                        try:
                            with open("veriler.csv", "a", newline="", encoding="utf-8") as f:
                                writer = csv.writer(f)
                                writer.writerow([
                                    timestamp,
                                    rota,
                                    f"{saat} saat",
                                    sonuc["price"],
                                    sonuc["supplier"],
                                    f"{sonuc['vehicle_type']} ({sonuc['vehicle_model']})"
                                ])
                            print(f"✅ Kaydedildi: €{sonuc['price']} - {sonuc['supplier']} - {sonuc['vehicle_type']} ({sonuc['vehicle_model']})")
                        except Exception as e:
                            print(f"⚠️ Veri işleme hatası: {e} → {sonuc}")
                else:
                    print("❌ Veri bulunamadı.")
            except Exception as e:
                print(f"❌ Hata oluştu: {e}")

    print("⏳ 10 dakika bekleniyor...")
    time.sleep(600)
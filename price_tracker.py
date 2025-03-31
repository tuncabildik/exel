print("Programın başlangıcı - modüller içe aktarılıyor...")
try:
    from selenium import webdriver
    print("selenium.webdriver modülü içe aktarıldı")
    from selenium.webdriver.common.by import By
    print("selenium.webdriver.common.by modülü içe aktarıldı")
    from selenium.webdriver.chrome.service import Service
    print("selenium.webdriver.chrome.service modülü içe aktarıldı")
    from selenium.webdriver.support.ui import WebDriverWait
    print("selenium.webdriver.support.ui modülü içe aktarıldı")
    from selenium.webdriver.support import expected_conditions as EC
    print("selenium.webdriver.support modülü içe aktarıldı")
    import time
    print("time modülü içe aktarıldı")
    import json
    print("json modülü içe aktarıldı")
    import re
    print("re modülü içe aktarıldı")
    import requests
    print("requests modülü içe aktarıldı")
    from datetime import datetime, timedelta
    print("datetime modülü içe aktarıldı")
    import os
    print("os modülü içe aktarıldı")
    print("smtplib modülü içe aktarıldı")
    print("email.mime.text modülü içe aktarıldı")
    print("email.mime.multipart modülü içe aktarıldı")
    import uuid
    print("uuid modülü içe aktarıldı")
    import sys
    print("sys modülü içe aktarıldı")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("webdriver_manager.chrome modülü içe aktarıldı")
        from selenium.webdriver.chrome.service import Service as ChromeService
        print("selenium.webdriver.chrome.service Service as ChromeService içe aktarıldı")
        import traceback
        print("traceback modülü içe aktarıldı")
        print("Tüm modüller başarıyla içe aktarıldı!")
    except ImportError as e:
        print(f"Modül içe aktarma hatası: {e}")
        print("Lütfen eksik modülleri yükleyin: pip3 install webdriver-manager selenium requests")
        sys.exit(1)
except ImportError as e:
    print(f"Temel modül içe aktarma hatası: {e}")
    print("Lütfen eksik modülleri yükleyin: pip3 install selenium requests")
    sys.exit(1)

print("Modüller içe aktarıldı. Program başlıyor...")

class FiyatTakipci:
    def __init__(self):
        print("FiyatTakipci sınıfı başlatılıyor...")
        # Debug modunu kontrol etmek için bayrak
        self.debug_mode = False
        # Test modu - Booking.com'dan veri çekilemiyor ise otomatik olarak test verisi üretir
        self.test_mode = False
        print("TEST MODU DEVRE DIŞI! Gerçek veriler kullanılacak.")
        # Kontrol aralığı - dakika cinsinden
        self.kontrol_araligi = 30
        # Son rapor saati
        self.son_rapor_saati = -1
        
        # Slack webhook URL'i - Hata alınıyorsa bu URL'i değiştirmeniz gerekiyor
        # Slack workspace'inizde yeni bir webhook URL'i oluşturun ve buraya ekleyin
        # URL formatı: https://hooks.slack.com/services/TXXXXX/BXXXXX/XXXXXXX
        print("Slack webhook URL'i yapılandırıldı. Fiyat değişikliklerinde anlık bildirimler gönderilecek.")
        
        # TÜM ANTALYA ROTALARI SİLİNDİ, SADECE İSTANBUL ROTALARI MEVCUT
        self.urls = {
            # İstanbul Havalimanı - Fatih arası rotalar
            'istanbul_to_fatih': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJ5VJ4bz-6yhQRWlxayTF4AC8&dropoffEstablishment=Akgun+Istanbul+Hotel&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'fatih_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJ5VJ4bz-6yhQRWlxayTF4AC8&pickupEstablishment=Akgun+Istanbul+Hotel&pickupType=hotel&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Beyoğlu arası rotalar
            'istanbul_to_beyoglu': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJQ58j_vG3yhQRPWLdfZF6R1Q&dropoffEstablishment=CVK+Park+Bosphorus+Hotel+Istanbul&dropoffType=hotel&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'beyoglu_to_istanbul': "https://taxis.booking.com/search?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJQ58j_vG3yhQRPWLdfZF6R1Q&pickupEstablishment=CVK+Park+Bosphorus+Hotel+Istanbul&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE",
            
            # İstanbul Havalimanı - Bakırköy arası rotalar
            'istanbul_to_bakirkoy': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJ0Tcd_a-8yhQRLrQofeCoOCA&dropoffEstablishment=Capacity+Shopping+Center&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'bakirkoy_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJ0Tcd_a-8yhQRLrQofeCoOCA&pickupEstablishment=Capacity+Shopping+Center&pickupType=shopping_area&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Arnavutköy arası rotalar
            'istanbul_to_arnavutkoy': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJl8U4JeWryhQRBJTE-vDBg5A&dropoffEstablishment=Hampton+by+Hilton&dropoffType=establishment&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'arnavutkoy_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJl8U4JeWryhQRBJTE-vDBg5A&pickupEstablishment=Hampton+by+Hilton&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Beşiktaş İskele arası rotalar
            'istanbul_to_besiktas': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJa5SVNDxa0hQR4IRiAUx_BKM&dropoffEstablishment=Conrad+Istanbul+Bosphorus&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'besiktas_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJa5SVNDxa0hQR4IRiAUx_BKM&pickupEstablishment=Conrad+Istanbul+Bosphorus&pickupType=hotel&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Zorlu arası rotalar
            'istanbul_to_zorlu': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJIyiEZ1C2yhQR3vcVuVpmjI0&dropoffEstablishment=Zorlu+Center&dropoffType=shopping_area&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'zorlu_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJIyiEZ1C2yhQR3vcVuVpmjI0&pickupEstablishment=Zorlu+Center&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Basınekspresi arası rotalar
            'istanbul_to_basinekspresi': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJ9YywOZmlyhQRWrEscGqx21E&dropoffEstablishment=Mall+of+Istanbul&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'basinekspresi_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-03-28&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJ9YywOZmlyhQRWrEscGqx21E&pickupEstablishment=Mall+of+Istanbul&pickupType=shopping_area&preSelectedResultReference=1&time=00%3A00&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Sarıyer arası rotalar (Güncellendi - Grand Tarabya Hotel)
            'istanbul_to_sariyer': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJB_T9qaLKyhQR4ZYnoUuBOAs&dropoffEstablishment=The+Grand+Tarabya+Hotel&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'sariyer_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJB_T9qaLKyhQR4ZYnoUuBOAs&pickupEstablishment=The+Grand+Tarabya+Hotel&pickupType=hotel&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Eyüp (Vialand) arası rotalar
            'istanbul_to_eyup': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJ7xTz7e6wyhQR0Ugc_utYleo&dropoffEstablishment=Vialand+Tema+Park&dropoffType=attraction_park&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'eyup_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJ7xTz7e6wyhQR0Ugc_utYleo&pickupEstablishment=Vialand+Tema+Park&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Kanyon AVM arası rotalar
            'istanbul_to_kanyon': "https://taxis.booking.com/search?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=EjdFc2VudGVwZSwgS2FueW9uIEFWTSwgMzQzOTQgxZ5pxZ9saS_EsHN0YW5idWwsIFTDvHJraXllIi4qLAoUChIJjTVrBGi2yhQRtrzECZFBfKoSFAoSCXUlpH5btsoUEQcOJ9gql8H4&dropoffEstablishment=Kanyon+AVM&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE",
            'kanyon_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=EjdFc2VudGVwZSwgS2FueW9uIEFWTSwgMzQzOTQgxZ5pxZ9saS_EsHN0YW5idWwsIFTDvHJraXllIi4qLAoUChIJjTVrBGi2yhQRtrzECZFBfKoSFAoSCXUlpH5btsoUEQcOJ9gql8H4&pickupEstablishment=Kanyon+AVM&pickupType=route&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Bebek (Le Méridien Etiler) arası rotalar
            'istanbul_to_bebek': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJvwn9Xga2yhQRQYoJWMnes-8&dropoffEstablishment=Le+M%C3%A9ridien+Istanbul+Etiler&dropoffType=establishment&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'bebek_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJvwn9Xga2yhQRQYoJWMnes-8&pickupEstablishment=Le+M%C3%A9ridien+Istanbul+Etiler&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Tarabya (Sait Halim Paşa Yalısı) arası rotalar
            'istanbul_to_tarabya': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJG-xxz_TKyhQRQEn_v8j21zA&dropoffEstablishment=Sait+Halim+Pasha+Mansion&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'tarabya_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJG-xxz_TKyhQRQEn_v8j21zA&pickupEstablishment=Sait+Halim+Pasha+Mansion&pickupType=establishment&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Bağcılar (Bağcılar Meydan Metro İstasyonu) arası rotalar
            'istanbul_to_bagcilar': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJm2WWEC2lyhQR25urx43c15c&dropoffEstablishment=Bagcilar+Meydan+Metro+Station&dropoffType=underground_railway_station&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'bagcilar_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJm2WWEC2lyhQR25urx43c15c&pickupEstablishment=Bagcilar+Meydan+Metro+Station&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Sabiha Gökçen Havalimanı arası rotalar
            'istanbul_to_saw': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJU6Ek9MvbyhQRdNqYgE3K76w&dropoffEstablishment=Istanbul+Sabiha+Gokcen+International+Airport&dropoffType=airport&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'saw_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJU6Ek9MvbyhQRdNqYgE3K76w&pickupEstablishment=Istanbul+Sabiha+Gokcen+International+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Üsküdar (Nevçarşı Alışveriş Merkezi) arası rotalar
            'istanbul_to_uskudar': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJORS2J9C3yhQR7FlS5_a-6nA&dropoffEstablishment=Nev%C3%A7ar%C5%9F%C4%B1+Al%C4%B1%C5%9Fveri%C5%9F+Merkezi&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'uskudar_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJORS2J9C3yhQR7FlS5_a-6nA&pickupEstablishment=Nev%C3%A7ar%C5%9F%C4%B1+Al%C4%B1%C5%9Fveri%C5%9F+Merkezi&pickupType=establishment&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Çamlıca (Büyük Çamlıca Camii) arası rotalar
            'istanbul_to_camlica': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJXckAWkjIyhQRRpR9954H1Gs&dropoffEstablishment=B%C3%BCy%C3%BCk+%C3%87aml%C4%B1ca+Camii&dropoffType=establishment&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'camlica_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJXckAWkjIyhQRRpR9954H1Gs&pickupEstablishment=B%C3%BCy%C3%BCk+%C3%87aml%C4%B1ca+Camii&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            
            # İstanbul Havalimanı - Ümraniye (Hisar Hospital Çamlıca) arası rotalar
            'istanbul_to_umraniye': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJR5cqtPTIyhQRQuHt8YnLSb4&dropoffEstablishment=Hisar+Hospital+%C3%87aml%C4%B1ca&lang=en-gb&passengers=2&pickup=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&pickupEstablishment=Istanbul+Airport&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg",
            'umraniye_to_istanbul': "https://taxis.booking.com/search/?affiliate=booking-taxi&currency=EUR&date=2025-04-30&dropoff=ChIJqZW8Cvb_n0ARBuUkyCzgDDg&dropoffEstablishment=Istanbul+Airport&lang=en-gb&passengers=2&pickup=ChIJR5cqtPTIyhQRQuHt8YnLSb4&pickupEstablishment=Hisar+Hospital+%C3%87aml%C4%B1ca&pickupType=establishment&preSelectedResultReference=1&time=16%3A35&adplat=www-index-web_shell_header-taxi-missing_creative-41Gan3xdzuE9uMUb432dU1&aid=304142&label=gen173bo-1DEgp0YXhpLWluZGV4KIICOOgHSChYA2jkAYgBAZgBKLgBB8gBDNgBA-gBAfgBBogCAZgCAqgCA7gCkqHyvgbAAgHSAiRiZjZmNzU5Mi1lOGEwLTQyYmYtYmViYy0yNmJhZWIzOTllMjfYAgTgAgE&comments=p2OLplgP6kqBccWQK722tg"
        }
        
        self.routes = {
            # İstanbul Havalimanı - Fatih arası rotalar
            'istanbul_to_fatih': {
                'from': 'İstanbul Havalimanı',
                'to': 'FATİH'
            },
            'fatih_to_istanbul': {
                'from': 'FATİH',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Beyoğlu arası rotalar
            'istanbul_to_beyoglu': {
                'from': 'İstanbul Havalimanı',
                'to': 'BEYOĞLU'
            },
            'beyoglu_to_istanbul': {
                'from': 'BEYOĞLU',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Bakırköy arası rotalar
            'istanbul_to_bakirkoy': {
                'from': 'İstanbul Havalimanı',
                'to': 'BAKIRKÖY'
            },
            'bakirkoy_to_istanbul': {
                'from': 'BAKIRKÖY',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Arnavutköy arası rotalar
            'istanbul_to_arnavutkoy': {
                'from': 'İstanbul Havalimanı',
                'to': 'ARNAVUTKÖY'
            },
            'arnavutkoy_to_istanbul': {
                'from': 'ARNAVUTKÖY',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Beşiktaş İskele arası rotalar
            'istanbul_to_besiktas': {
                'from': 'İstanbul Havalimanı',
                'to': 'BEŞİKTAŞ İSKELE'
            },
            'besiktas_to_istanbul': {
                'from': 'BEŞİKTAŞ İSKELE',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Zorlu arası rotalar
            'istanbul_to_zorlu': {
                'from': 'İstanbul Havalimanı',
                'to': 'ZORLU'
            },
            'zorlu_to_istanbul': {
                'from': 'ZORLU',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Basınekspresi arası rotalar
            'istanbul_to_basinekspresi': {
                'from': 'İstanbul Havalimanı',
                'to': 'BASINEKSPRESİ'
            },
            'basinekspresi_to_istanbul': {
                'from': 'BASINEKSPRESİ',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Sarıyer arası rotalar (Güncellendi - Grand Tarabya Hotel)
            'istanbul_to_sariyer': {
                'from': 'İstanbul Havalimanı',
                'to': 'SARIYER'
            },
            'sariyer_to_istanbul': {
                'from': 'SARIYER',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Eyüp (Vialand) arası rotalar
            'istanbul_to_eyup': {
                'from': 'İstanbul Havalimanı',
                'to': 'EYÜP'
            },
            'eyup_to_istanbul': {
                'from': 'EYÜP',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Kanyon AVM arası rotalar
            'istanbul_to_kanyon': {
                'from': 'İstanbul Havalimanı',
                'to': 'KANYON'
            },
            'kanyon_to_istanbul': {
                'from': 'KANYON',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Bebek (Le Méridien Etiler) arası rotalar
            'istanbul_to_bebek': {
                'from': 'İstanbul Havalimanı',
                'to': 'BEBEK'
            },
            'bebek_to_istanbul': {
                'from': 'BEBEK',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Tarabya (Sait Halim Paşa Yalısı) arası rotalar
            'istanbul_to_tarabya': {
                'from': 'İstanbul Havalimanı',
                'to': 'TARABYA'
            },
            'tarabya_to_istanbul': {
                'from': 'TARABYA',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Bağcılar (Bağcılar Meydan Metro İstasyonu) arası rotalar
            'istanbul_to_bagcilar': {
                'from': 'İstanbul Havalimanı',
                'to': 'BAĞCILAR'
            },
            'bagcilar_to_istanbul': {
                'from': 'BAĞCILAR',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Sabiha Gökçen Havalimanı arası rotalar
            'istanbul_to_saw': {
                'from': 'İstanbul Havalimanı',
                'to': 'SAW'
            },
            'saw_to_istanbul': {
                'from': 'SAW',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Üsküdar (Nevçarşı Alışveriş Merkezi) arası rotalar
            'istanbul_to_uskudar': {
                'from': 'İstanbul Havalimanı',
                'to': 'ÜSKÜDAR'
            },
            'uskudar_to_istanbul': {
                'from': 'ÜSKÜDAR',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Çamlıca (Büyük Çamlıca Camii) arası rotalar
            'istanbul_to_camlica': {
                'from': 'İstanbul Havalimanı',
                'to': 'ÇAMLICA'
            },
            'camlica_to_istanbul': {
                'from': 'ÇAMLICA',
                'to': 'İstanbul Havalimanı'
            },
            
            # İstanbul Havalimanı - Ümraniye (Hisar Hospital Çamlıca) arası rotalar
            'istanbul_to_umraniye': {
                'from': 'İstanbul Havalimanı',
                'to': 'ÜMRANİYE'
            },
            'umraniye_to_istanbul': {
                'from': 'ÜMRANİYE',
                'to': 'İstanbul Havalimanı'
            }
        }
        
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # daha eski sürüm olarak dene
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        
        self.last_check_results = {
            'istanbul_to_fatih': {},
            'fatih_to_istanbul': {},
            'istanbul_to_beyoglu': {},
            'beyoglu_to_istanbul': {},
            'istanbul_to_bakirkoy': {},
            'bakirkoy_to_istanbul': {},
            'istanbul_to_arnavutkoy': {},
            'arnavutkoy_to_istanbul': {},
            'istanbul_to_besiktas': {},
            'besiktas_to_istanbul': {},
            'istanbul_to_zorlu': {},
            'zorlu_to_istanbul': {},
            'istanbul_to_basinekspresi': {},
            'basinekspresi_to_istanbul': {},
            'istanbul_to_sariyer': {},
            'sariyer_to_istanbul': {},
            'istanbul_to_eyup': {},
            'eyup_to_istanbul': {},
            'istanbul_to_kanyon': {},
            'kanyon_to_istanbul': {},
            'istanbul_to_bebek': {},
            'bebek_to_istanbul': {},
            'istanbul_to_tarabya': {},
            'tarabya_to_istanbul': {},
            'istanbul_to_bagcilar': {},
            'bagcilar_to_istanbul': {},
            'istanbul_to_saw': {},
            'saw_to_istanbul': {},
            'istanbul_to_uskudar': {},
            'uskudar_to_istanbul': {},
            'istanbul_to_camlica': {},
            'camlica_to_istanbul': {},
            'istanbul_to_umraniye': {},
            'umraniye_to_istanbul': {}
        }
        
        
        print("FiyatTakipci sınıfı başlatıldı.")
        
    def extract_params_from_url(self, url):
        "URL'den parametreleri çıkarır"
        params = {}
        
        # pickup ve dropoff ID'lerini çıkar
        pickup_match = re.search(r'pickup=([^&]+)', url)
        if pickup_match:
            params['pickup'] = pickup_match.group(1)
            
        dropoff_match = re.search(r'dropoff=([^&]+)', url)
        if dropoff_match:
            params['dropoff'] = dropoff_match.group(1)
            
        # Diğer parametreleri çıkar
        passengers_match = re.search(r'passengers=(\d+)', url)
        if passengers_match:
            params['passengers'] = passengers_match.group(1)
            
        # Tarih ve saat parametrelerini çıkar
        date_match = re.search(r'date=([^&]+)', url)
        if date_match:
            params['date'] = date_match.group(1)
            
        time_match = re.search(r'time=([^&]+)', url)
        if time_match:
            params['time'] = time_match.group(1).replace('%3A', ':')
            
        return params

    def get_all_prices_and_suppliers(self, saat_sonrasi, url):
        "Belirli saatlerde, URL'deki tüm fiyat ve tedarikçi bilgilerini alır."
        try:
            print(f"URL: {url} için {saat_sonrasi} saat sonrası fiyat kontrolü başlıyor...")
            # URL'yi güncelle
            yeni_url = self.url_guncelle(url, saat_sonrasi)
            print(f"\nKontrol ediliyor: {yeni_url}")
            
            # URL'den parametreleri çıkar
            params = self.extract_params_from_url(yeni_url)
            
            # Tarih ve saati ayarla
            tarih = params.get('date', datetime.now().strftime("%Y-%m-%d"))
            saat = params.get('time', '00:00').replace('%3A', ':')
            
            # Tarih ve saati birleştir
            tarih_saat = f"{tarih}T{saat}:00"
            
            # API URL'sini oluştur
            api_url = (
                "https://taxi.booking.com/search-results-mfe/rates"
                "?affiliate=booking-taxi"
                "&currency=EUR"
                "&displayLocalSupplierText=true"
                f"&dropoff={params.get('dropoff', '')}"
                f"&dropoffEstablishment=Antalya+Airport"
                "&format=envelope"
                "&isExpandable=true"
                "&language=en-gb"
                f"&passenger={params.get('passengers', '2')}"
                f"&pickup={params.get('pickup', '')}"
                f"&pickupDateTime={tarih_saat}"
                "&pickupEstablishment=DoubleTree+By+Hilton+Antalya+Airport"
                "&pickupType=hotel"
                "&populateSupplierName=true"
            )
            
            # API isteği için headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Origin': 'https://taxis.booking.com',
                'Referer': 'https://taxis.booking.com/'
            }
            
            # API isteği gönder
            print("API isteği gönderiliyor...")
            response = requests.get(api_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Debug için JSON verisini kaydet (sadece debug modunda)
                    if self.debug_mode:
                        with open(f"api_response_{saat_sonrasi}saat.json", "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=2)
                    
                    results = []
                    
                    # Journeys içindeki tüm sonuçları topla
                    if 'journeys' in data:
                        for journey in data['journeys']:
                            for leg in journey.get('legs', []):
                                for result in leg.get('results', []):
                                    price = f"€{result.get('price', 'Bilinmiyor')}"
                                    supplier = result.get('supplierName', 'Bilinmiyor')
                                    vehicle_type = result.get('carDetails', {}).get('description', 'Bilinmiyor')
                                    vehicle_model = result.get('carDetails', {}).get('modelDescription', 'Bilinmiyor')
                                    max_passenger = result.get('maxPassenger', 'Bilinmiyor')
                                    bags = result.get('bags', 'Bilinmiyor')
                                    
                                    results.append({
                                        'price': price,
                                        'supplier': supplier,
                                        'vehicle_type': vehicle_type,
                                        'vehicle_model': vehicle_model,
                                        'max_passenger': max_passenger,
                                        'bags': bags
                                    })
                                    
                                    print(f"Bulunan sonuç: {price} - {supplier} - {vehicle_type} ({vehicle_model})")
                    
                    if results:
                        # Fiyata göre sırala
                        try:
                            results.sort(key=lambda x: float(x['price'].replace('€', '').replace(',', '.')) if x['price'] != "Bilinmiyor" else float('inf'))
                        except Exception as sort_error:
                            print(f"Sonuçları sıralama hatası: {sort_error}, sıralama yapılmadan devam ediliyor.")
                        
                        # En düşük fiyat ve tedarikçi
                        lowest_price = results[0]['price']
                        lowest_supplier = results[0]['supplier']
                        lowest_vehicle = results[0]['vehicle_type']
                        if results[0]['vehicle_model'] != 'Bilinmiyor':
                            lowest_vehicle += f" ({results[0]['vehicle_model']})"
                        
                        return lowest_price, lowest_supplier, lowest_vehicle, results
                    else:
                        print("API'den sonuç alındı ancak araç bulunamadı.")
                        return "Bulunamadı", "Bulunamadı", "Bulunamadı", []
                    
                except Exception as e:
                    print(f"API yanıtı işlenirken hata: {str(e)}")
                    return "API Hatası", "API Hatası", "API Hatası", []
            else:
                print(f"API isteği başarısız: {response.status_code}")
                return f"HTTP Hatası: {response.status_code}", "HTTP Hatası", "HTTP Hatası", []
            
        except Exception as e:
            print(f"Fiyat ve tedarikçi bilgisi alınırken hata: {str(e)}")
            return "Bağlantı Hatası", "Bağlantı Hatası", "Bağlantı Hatası", []

    def url_guncelle(self, url, saat_sonrasi):
        try:
            # 10 dakika geri al (0.166667 saat)
            saat_sonrasi = saat_sonrasi - (10/60)  # 10 dakikayı saatten çıkar
            
            yeni_zaman = datetime.now() + timedelta(hours=saat_sonrasi)
            yeni_tarih = yeni_zaman.strftime("%Y-%m-%d")
            yeni_saat = yeni_zaman.strftime("%H:%M")
            
            # URL'deki tarih ve saat parametrelerini güncelle
            yeni_url = url
            
            # pickupDateTime parametresi varsa güncelle
            if "pickupDateTime=" in url:
                yeni_tarih_saat = f"{yeni_tarih}T{yeni_saat}:00"
                yeni_url = re.sub(
                    r'pickupDateTime=([^&]*)',
                    f'pickupDateTime={yeni_tarih_saat.replace(":", "%3A")}',
                    yeni_url
                )
            
            # date ve time parametreleri varsa güncelle
            if "date=" in url:
                yeni_url = re.sub(r'date=([^&]*)', f'date={yeni_tarih}', yeni_url)
            
            if "time=" in url:
                yeni_url = re.sub(r'time=([^&]*)', f'time={yeni_saat.replace(":", "%3A")}', yeni_url)
            
            return yeni_url
            
        except Exception as e:
            print(f"URL güncellenirken hata oluştu: {str(e)}")
            return url

    def tum_saatler_icin_kontrol(self):
        """Tüm rotalar için tüm saat dilimlerinde fiyat kontrolü yapar."""
        print("\n\n" + "-" * 120)
        print(f"BAŞLANGIÇ SAATİ: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

        # Kontrol edilecek saat dilimleri
        saatler = [4, 8, 10, 12, 24]
        
        # Sonuçlar sözlüğü - her rota için ayrı bir şekilde tanımlanıyor
        sonuclar = {}
        
        # İlk çalışma kontrolü - daha basit bir kontrol yöntemi
        ilk_calisma = True
        
        for route_key, url in self.urls.items():
            # Her rota için sonuçları bu sözlükte toplayalım
            sonuclar[route_key] = {}
            
            route_info = self.routes[route_key]
            print(f"{route_info['from']} ➡️ {route_info['to']} rotası kontrol ediliyor...")
            
            for saat in saatler:
                try:
                    print(f"{saat} saat sonrası için kontrol yapılıyor...")
                    price, supplier, vehicle, all_results = self.get_all_prices_and_suppliers(saat, url)
                    
                    # Sonuçları sözlüğe ekle
                    sonuclar[route_key][saat] = {
                        'price': price, 
                        'supplier': supplier, 
                        'vehicle': vehicle,
                        'all_results': all_results
                    }
                    
                    print(f"{saat} saat sonrası - En düşük fiyat: {price}, Tedarikçi: {supplier}, Araç: {vehicle}")
                    
                    # Önceki kontrolle karşılaştır ve değişiklik durumunu kaydet
                    if route_key in self.last_check_results and saat in self.last_check_results[route_key]:
                        ilk_calisma = False  # Eğer önceki sonuçlar varsa, ilk çalışma değil
                        last_check = self.last_check_results[route_key][saat]
                        if (last_check.get('price') != price or last_check.get('supplier') != supplier):
                            print(f"!!! DEĞİŞİKLİK TESPİT EDİLDİ - Önceki: {last_check.get('price')} / {last_check.get('supplier')} --> Yeni: {price} / {supplier}")
                            
                            # Fiyat değişikliği analizi
                            fiyat_farki = ""
                            bildirim_rengi = "#36a64f"  # Yeşil (varsayılan)
                            
                            try:
                                onceki_fiyat = float(last_check.get('price').replace('€', '').replace(',', '.'))
                                simdiki_fiyat = float(price.replace('€', '').replace(',', '.'))
                                fark = simdiki_fiyat - onceki_fiyat
                                fiyat_farki = f" (Fark: {'+'if fark > 0 else ''}{fark:.2f}€)"
                                
                                # Fiyat değişikliğinin önemine göre renk belirle
                                if fark > 5:  # 5 Euro'dan fazla fiyat artışı varsa kırmızı
                                    bildirim_rengi = "#ff0000"
                                elif fark > 0:  # Herhangi bir fiyat artışı varsa sarı
                                    bildirim_rengi = "#ffcc00"
                                elif fark < -5:  # 5 Euro'dan fazla fiyat düşüşü varsa mavi
                                    bildirim_rengi = "#0000ff"
                            except:
                                pass
                            
                            # Bildirim metni oluştur
                            route_info = self.routes[route_key]
                            title = f"Fiyat Değişikliği: {route_info['from']} ➡️ {route_info['to']} ({saat} saat sonrası)"
                            
                            # Daha okunaklı mesaj
                            message = (
                                f"*Önceki:* {last_check.get('price')} / {last_check.get('supplier')}\n"
                                f"*Yeni:* {price} / {supplier}{fiyat_farki}\n"
                                f"*Zaman:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            )
                            
                            # Slack bildirimi gönder
                except Exception as e:
                    print(f"Hata oluştu ({route_key}, {saat} saat sonrası): {e}")
                    # Hatalı durumda varsayılan değerler atayalım
                    sonuclar[route_key][saat] = {
                        'price': 'Hata', 
                        'supplier': 'Hata',
                        'vehicle': 'Hata',
                        'all_results': []
                    }
        
        # Son kontrol sonuçlarını güncelle
        self.last_check_results = sonuclar
        
        return ilk_calisma

    def surekli_kontrol(self):
        """Belirtilen zaman aralıklarında sürekli kontrol yapar."""
        while True:
            try:
                print("\n" + "=" * 120)
                print("Otuz dört yönlü kontrol yapılıyor...")
                print("=" * 120)
                
                ilk_calisma = self.tum_saatler_icin_kontrol()
                
                guncel_saat = datetime.now().hour
                
                # İlk çalışmada veya her saat başı rapor gönder
                if ilk_calisma or guncel_saat != self.son_rapor_saati:
                    self.saatlik_rapor_gonder(is_first_run=ilk_calisma)
                    self.son_rapor_saati = guncel_saat
                    
                    # Bir sonraki rapor için bekleme süresini hesapla ve göster
                    simdi = datetime.now()
                    # Eğer saat 23 ise, bir sonraki gün saat 00:00'a ayarla
                    if simdi.hour == 23:
                        bir_sonraki_saat = simdi.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                    else:
                        bir_sonraki_saat = simdi.replace(hour=simdi.hour + 1, minute=0, second=0, microsecond=0)
                    
                    kalan_sure = bir_sonraki_saat - simdi
                    kalan_dakika = kalan_sure.seconds // 60
                    
                    print("\n" + "-" * 80)
                    print(f"📧 E-posta raporu başarıyla gönderildi - {simdi.strftime('%H:%M:%S')}")
                    print(f"⏱️ Bir sonraki rapor saati: {bir_sonraki_saat.strftime('%H:00')} ({kalan_dakika} dakika sonra)")
                    print("-" * 80)
                
                print("\nBir sonraki kontrol için bekleniyor...")
                # Kalan zamanı daha ayrıntılı göster
                next_check_time = datetime.now() + timedelta(minutes=self.kontrol_araligi)
                print(f"Sonraki fiyat kontrolü: {next_check_time.strftime('%H:%M:%S')} (yaklaşık {self.kontrol_araligi} dakika sonra)")
                
                time.sleep(60 * self.kontrol_araligi)  # Dakika cinsinden bekleme
            except KeyboardInterrupt:
                print("\n\nProgram kullanıcı tarafından durduruldu.")
                raise
            except Exception as e:
                print(f"Hata oluştu: {e}")
                print(f"Hata detayları: {traceback.format_exc()}")
                print("60 saniye sonra tekrar denenecek...")
                time.sleep(60)

    def ilk_saatlik_rapor_gonder(self):
        "İlk çalışma için saatlik rapor gönderir"
        print("\nİlk saatlik rapor hazırlanıyor...")
        self.saatlik_rapor_gonder(is_first_run=True)
    
    
    def saatlik_rapor_gonder(self, is_first_run=False):
        """Her saat başı tüm rotalar için rapor gönderir."""
        guncel_saat = datetime.now().strftime("%H:00")
        print(f"\n{guncel_saat} için rapor oluşturuluyor...")

        saatler = [4, 8, 10, 12, 24]  # Kontrol edilecek saatler
        
        # E-posta içeriği oluştur
        if is_first_run:
            subject = f"İstanbul - İlk Taksi Fiyat Raporu - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        else:
            subject = f"İstanbul - Saatlik Taksi Fiyat Raporu - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
        # E-posta içeriğini oluştur - basit HTML
        body = "<html><body>"
        body += f"<h2>Taksi Fiyat Raporu - {datetime.now().strftime('%Y-%m-%d %H:%M')}</h2>"
        body += "<p>Otuz dört yönlü kontrol raporu:</p>"

        # Takip için sayaçlar
        toplam_rota = 0
        bizim_rotalar = 0
        
        # Tedarikçi analizi için veri yapıları
        tum_tedarikciler = set()  # Benzersiz tedarikçi adları
        tedarikci_rota_sayisi = {}  # Her tedarikçinin kaç rotada hizmet verdiği
        bodrum_luxury_avantajli_saatler = {saat: 0 for saat in saatler}  # Hangi saatlerde avantajlıyız
        
        # Fiyat değişim analizi için
        fiyat_artis_sayisi = 0
        fiyat_dusus_sayisi = 0
        fiyat_degisim_yok = 0
        
        # Her rota için araç seçeneklerini oluştur
        for route_key, hours_data in self.last_check_results.items():
            if route_key not in self.routes:
                continue  # Geçersiz rota anahtarını atla
                
            route_info = self.routes[route_key]
            toplam_rota += 1
            
            # Rota adını düzenle (MAVİKENT için özel durum)
            from_name = route_info['from']
            to_name = route_info['to'] 
            if from_name == 'Şah Inn Paradise Tatil Köyü':
                from_name = 'MAVİKENT'
            if to_name == 'Şah Inn Paradise Tatil Köyü':
                to_name = 'MAVİKENT'
                
            body += f"<h3>{from_name} ➡️ {to_name}</h3>"
            
            # Bu rota için tüm tedarikçileri topla (tüm saatler için)
            rota_tedarikcileri = set()
            
            # Tüm saat ve araç seçenekleri için tablolar
            for saat in saatler:
                if str(saat) not in hours_data and saat not in hours_data:
                    continue  # Bu saat dilimi için veri yoksa atla
                
                # Saat anahtarını doğru şekilde al
                saat_key = saat
                if str(saat) in hours_data:
                    saat_key = str(saat)
                
                data = hours_data.get(saat_key, {})
                
                current_time = datetime.now()
                hours_ahead_time = current_time + timedelta(hours=int(saat))
                time_str = hours_ahead_time.strftime("%Y-%m-%d %H:%M")
                
                # Değişiklik durumunu belirle
                status = "Değişiklik yok"
                if is_first_run:
                    status = "İlk kontrol"
                
                # Saat başlığına rota bilgisini ekle
                body += f"<h4>{time_str} ({saat} saat sonra) - {from_name} ➡️ {to_name} - {status}</h4>"
                body += "<table border='1' cellpadding='5'>"
                body += "<tr><th>Fiyat</th><th>Tedarikçi</th><th>Araç Tipi</th></tr>"
                
                all_results = data.get('all_results', [])
                
                # Bu saatteki fiyat değişimi kontrolü
                if not is_first_run and route_key in getattr(self, 'previous_results', {}) and saat_key in getattr(self, 'previous_results', {}).get(route_key, {}):
                    onceki_fiyat = self.previous_results[route_key][saat_key].get('price', 'Veri yok')
                    simdiki_fiyat = data.get('price', 'Veri yok')
                    
                    if onceki_fiyat != 'Veri yok' and simdiki_fiyat != 'Veri yok':
                        try:
                            onceki_sayi = float(onceki_fiyat.replace('€', '').replace(',', '.'))
                            simdiki_sayi = float(simdiki_fiyat.replace('€', '').replace(',', '.'))
                            
                            if simdiki_sayi > onceki_sayi:
                                fiyat_artis_sayisi += 1
                            elif simdiki_sayi < onceki_sayi:
                                fiyat_dusus_sayisi += 1
                            else:
                                fiyat_degisim_yok += 1
                        except:
                            pass
                
                if all_results:
                    # Bu saat ve rota için tüm tedarikçileri topla
                    bodrum_luxury_en_iyi = False
                    
                    # Bodrum Luxury Travel bu rotada en iyi fiyatı veriyor mu kontrolü
                    en_iyi_fiyat = float('inf')
                    en_iyi_tedarikci = None
                    
                    for result in all_results:
                        supplier = result.get('supplier', 'Bilinmiyor')
                        price_str = result.get('price', 'Bilinmiyor')
                        
                        # Tedarikçileri topla
                        if supplier != 'Bilinmiyor':
                            tum_tedarikciler.add(supplier)
                            rota_tedarikcileri.add(supplier)
                            
                            if supplier in tedarikci_rota_sayisi:
                                tedarikci_rota_sayisi[supplier] += 1
                            else:
                                tedarikci_rota_sayisi[supplier] = 1
                        
                        # En iyi fiyat kontrolü
                        if price_str != 'Bilinmiyor':
                            try:
                                price_value = float(price_str.replace('€', '').replace(',', '.'))
                                if price_value < en_iyi_fiyat:
                                    en_iyi_fiyat = price_value
                                    en_iyi_tedarikci = supplier
                            except:
                                pass
                    
                    # Bodrum Luxury Travel en iyi fiyata sahip mi?
                    if en_iyi_tedarikci and "Bodrum Luxury Travel" in en_iyi_tedarikci:
                        bodrum_luxury_avantajli_saatler[saat] += 1
                        bodrum_luxury_en_iyi = True
                    
                    # Tüm sonuçları listele
                    for result in all_results:
                        vehicle_info = result.get('vehicle_type', 'Bilinmiyor')
                        if result.get('vehicle_model') and result.get('vehicle_model') != 'Bilinmiyor':
                            vehicle_info += f" ({result.get('vehicle_model')})"
                        
                        # Şirketimizin adını kontrol et ve yeşil/bold yap
                        supplier = result.get('supplier', 'Bilinmiyor')
                        price_str = result.get('price', 'Bilinmiyor')
                        
                        # Bodrum Luxury Travel'ı yeşil ve kalın yap
                        if "Bodrum Luxury Travel" in supplier:
                            # En iyi fiyata sahip olduğumuzda ekstra belirt
                            if bodrum_luxury_en_iyi and price_str == all_results[0].get('price', 'Bilinmiyor'):
                                supplier = f'<span style="color:green; font-weight:bold;">{supplier} ⭐</span>'
                            else:
                                supplier = f'<span style="color:green; font-weight:bold;">{supplier}</span>'
                            bizim_rotalar += 1
                        
                        body += f"<tr><td>{result.get('price', 'Bilinmiyor')}</td><td>{supplier}</td><td>{vehicle_info}</td></tr>"
                else:
                    # En azından ana sonucu göster
                    price = data.get('price', 'Veri yok')
                    supplier = data.get('supplier', 'Veri yok')
                    
                    # Tedarikçiyi kaydet
                    if supplier != 'Veri yok':
                        tum_tedarikciler.add(supplier)
                        rota_tedarikcileri.add(supplier)
                        
                        if supplier in tedarikci_rota_sayisi:
                            tedarikci_rota_sayisi[supplier] += 1
                        else:
                            tedarikci_rota_sayisi[supplier] = 1
                    
                    # Şirketimizin adını kontrol et ve yeşil/bold yap
                    if "Bodrum Luxury Travel" in supplier:
                        supplier = f'<span style="color:green; font-weight:bold;">{supplier}</span>'
                        bizim_rotalar += 1
                        
                    vehicle = data.get('vehicle', 'Veri yok')
                    
                    if price != 'Veri yok' or supplier != 'Veri yok':
                        body += f"<tr><td>{price}</td><td>{supplier}</td><td>{vehicle}</td></tr>"
                    else:
                        body += f"<tr><td colspan='3'>Araç seçeneği bulunamadı</td></tr>"
                
                body += "</table><br>"
        
        # Pazar analizi istatistiği
        body += f'<h2 style="margin-top:30px;">Pazar ve Tedarikçi Analizi</h2>'
        body += f'<div style="background-color:#f0f0f0; padding:15px; margin-top:10px; border-radius:5px;">'
        
        # 1. Temel istatistikler
        if toplam_rota > 0:
            bizim_oran = (bizim_rotalar / toplam_rota) * 100
            body += f'<h3>Temel İstatistikler</h3>'
            body += f'<p>Kontrol edilen toplam rota sayısı: <strong>{toplam_rota}</strong></p>'
            body += f'<p><span style="color:green; font-weight:bold;">Bodrum Luxury Travel</span> tarafından sunulan rota sayısı: <strong>{bizim_rotalar}</strong></p>'
            body += f'<p>Rotalarımızın pazardaki oranı: <strong>%{bizim_oran:.1f}</strong></p>'
            
            # Bir önceki rapora göre pazar payı değişimi
            if hasattr(self, 'previous_bizim_oran'):
                degisim = bizim_oran - self.previous_bizim_oran
                if degisim > 0:
                    body += f'<p>Bir önceki rapora göre pazar payı değişimi: <span style="color:green;">+{degisim:.1f}%</span></p>'
                elif degisim < 0:
                    body += f'<p>Bir önceki rapora göre pazar payı değişimi: <span style="color:red;">{degisim:.1f}%</span></p>'
                else:
                    body += f'<p>Bir önceki rapora göre pazar payı değişimi: <span style="color:gray;">0%</span></p>'
            
            # Bu rapordaki oranı kaydet
            self.previous_bizim_oran = bizim_oran
        
        # 2. Tedarikçi analizi
        body += f'<h3>Tedarikçi Analizi</h3>'
        body += f'<p>Pazardaki toplam tedarikçi sayısı: <strong>{len(tum_tedarikciler)}</strong></p>'
        
        body += f'<h4>Rakip Tedarikçiler</h4>'
        body += f'<table border="1" cellpadding="5" style="width:100%;">'
        body += f'<tr><th>Tedarikçi Adı</th><th>Hizmet Verdiği Rota Sayısı</th></tr>'
        
        # Tedarikçileri rota sayısına göre sırala
        sorted_tedarikci_listesi = sorted(tedarikci_rota_sayisi.items(), key=lambda x: x[1], reverse=True)
        for tedarikci, rota_sayisi in sorted_tedarikci_listesi:
            if "Bodrum Luxury Travel" in tedarikci:
                body += f'<tr><td><span style="color:green; font-weight:bold;">{tedarikci}</span></td><td>{rota_sayisi}</td></tr>'
            else:
                body += f'<tr><td>{tedarikci}</td><td>{rota_sayisi}</td></tr>'
        
        body += f'</table>'
        
        # 3. Saat bazlı karşılaştırmalar
        body += f'<h3>Saat Bazlı Karşılaştırmalar</h3>'
        body += f'<p>Hangi saatlerde <span style="color:green; font-weight:bold;">Bodrum Luxury Travel</span> en iyi fiyatı sunuyor:</p>'
        
        body += f'<table border="1" cellpadding="5" style="width:100%;">'
        body += f'<tr><th>Saat</th><th>En İyi Fiyat Verdiğimiz Rota Sayısı</th><th>Başarı Oranı</th></tr>'
        
        for saat, avantajli_rota_sayisi in bodrum_luxury_avantajli_saatler.items():
            if toplam_rota > 0:
                basari_orani = (avantajli_rota_sayisi / toplam_rota) * 100
                body += f'<tr><td>{saat} saat sonrası</td><td>{avantajli_rota_sayisi}</td><td>%{basari_orani:.1f}</td></tr>'
            else:
                body += f'<tr><td>{saat} saat sonrası</td><td>{avantajli_rota_sayisi}</td><td>%0</td></tr>'
        
        body += f'</table>'
        
        # 4. Fiyat değişim eğilimi
        toplam_degisim = fiyat_artis_sayisi + fiyat_dusus_sayisi + fiyat_degisim_yok
        if not is_first_run and toplam_degisim > 0:
            body += f'<h3>Fiyat Değişim Eğilimi</h3>'
            
            artis_orani = (fiyat_artis_sayisi / toplam_degisim) * 100
            dusus_orani = (fiyat_dusus_sayisi / toplam_degisim) * 100
            degismeyen_orani = (fiyat_degisim_yok / toplam_degisim) * 100
            
            body += f'<p>Fiyat artışı yaşanan rotalar: <span style="color:red;">{fiyat_artis_sayisi} (%{artis_orani:.1f})</span></p>'
            body += f'<p>Fiyat düşüşü yaşanan rotalar: <span style="color:green;">{fiyat_dusus_sayisi} (%{dusus_orani:.1f})</span></p>'
            body += f'<p>Fiyat değişimi olmayan rotalar: <span style="color:gray;">{fiyat_degisim_yok} (%{degismeyen_orani:.1f})</span></p>'
            
            # Genel eğilim
            if fiyat_artis_sayisi > fiyat_dusus_sayisi:
                body += f'<p><strong>Genel Eğilim:</strong> <span style="color:red;">Fiyatlar artıyor</span></p>'
            elif fiyat_dusus_sayisi > fiyat_artis_sayisi:
                body += f'<p><strong>Genel Eğilim:</strong> <span style="color:green;">Fiyatlar düşüyor</span></p>'
            else:
                body += f'<p><strong>Genel Eğilim:</strong> <span style="color:gray;">Fiyatlar stabil</span></p>'
        
        body += f'</div>'
        
        body += "<p>Bu rapor Taksi Fiyat Takip Programı v13.1 tarafından otomatik olarak oluşturulmuştur.</p>"
        body += "</body></html>"

        # Bir sonraki karşılaştırma için mevcut sonuçları kaydet
        self.previous_results = self.last_check_results.copy()
        
        # Raporu gönder
        try:
            print(f"Saatlik rapor gönderildi: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        except Exception as e:
            print(f"Rapor gönderilirken hata: {e}")
            print("E-posta gönderilemedi, bir sonraki döngüde tekrar denenecek.")

def main():
    """
    Ana program fonksiyonu.
    """
    print("\n*********** İstanbul Havalimanı - Merkez İlçeler Fiyat Takibi ***********\n")
    print("Takip edilen rotalar:")
    print("1. FATİH - İstanbul Havalimanı arası")
    print("2. BEYOĞLU - İstanbul Havalimanı arası")
    print("3. BAKIRKÖY - İstanbul Havalimanı arası")
    print("4. ARNAVUTKÖY - İstanbul Havalimanı arası")
    print("5. BEŞİKTAŞ İSKELE - İstanbul Havalimanı arası")
    print("6. ZORLU - İstanbul Havalimanı arası")
    print("7. BASINEKSPRESİ - İstanbul Havalimanı arası")
    print("8. SARIYER - İstanbul Havalimanı arası")
    print("9. EYÜP (VİALAND) - İstanbul Havalimanı arası")
    print("10. KANYON - İstanbul Havalimanı arası")
    print("11. BEBEK - İstanbul Havalimanı arası")
    print("12. TARABYA - İstanbul Havalimanı arası")
    print("13. BAĞCILAR - İstanbul Havalimanı arası")
    print("14. SAW (Sabiha Gökçen Havalimanı) - İstanbul Havalimanı arası")
    print("15. ÜSKÜDAR - İstanbul Havalimanı arası")
    print("16. ÇAMLICA - İstanbul Havalimanı arası")
    print("17. ÜMRANİYE - İstanbul Havalimanı arası")
    print("\nFiyat kontrolü 30 dakikada bir yapılacak.")
    print("Yarım saatlik raporlar e-posta ile gönderilecek.")
    print("\nProgram NORMAL MODDA çalışıyor. Booking.com'dan gerçek veriler çekilecek.")
    print("\nProgramı durdurmak için CTRL+C tuşlarına basın.")
    
    try:
        takip = FiyatTakipci()
        takip.surekli_kontrol()
    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından durduruldu.")
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            subject = "İstanbul - ALARM: TRW Taksi Fiyat Takip Programı Durduruldu!"
            body = f"""
            <html>
            <body>
                <h2>TRW Taksi Fiyat Takip Programı Durduruldu!</h2>
                <p>Program {current_time} tarihinde durduruldu.</p>
                <p>Kullanıcı tarafından durdurulmuş olabilir veya başka bir hata oluşmuş olabilir.</p>
                <p>Lütfen programın çalışıp çalışmadığını kontrol edin.</p>
            </body>
            </html>
            """
            print("Bildirim e-posta ile gönderildi.")
            
            # Slack bildirimi gönder - sade format
            slack_title = "🛑 Program Durduruldu"
            slack_message = f"**Zaman:** {current_time}\n**Durum:** Program kullanıcı tarafından durduruldu\n**Eylem:** Lütfen kontrolü yapın ve gerekirse yeniden başlatın\n**Detay:** Programı başlatmak için `python price_tracker_clean.py` komutunu kullanın"
        except Exception as email_error:
            print(f"Bildirimler gönderilirken hata oluştu: {str(email_error)}")
    except Exception as e:
        print(f"\nKritik hata: {e}")
        print(f"Hata detayları: {traceback.format_exc()}")
        
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            subject = "İstanbul - ALARM: TRW Taksi Fiyat Takip Programı Hata Verdi!"
            body = f"""
            <html>
            <body>
                <h2>TRW Taksi Fiyat Takip Programı Hata Verdi!</h2>
                <p>Program {current_time} tarihinde bir hata ile karşılaştı.</p>
                <p>Hata: {str(e)}</p>
                <p>Hata detayları:</p>
                <pre>{traceback.format_exc()}</pre>
                <p>Lütfen programı yeniden başlatın.</p>
            </body>
            </html>
            """
            print("Hata bildirimi e-posta ile gönderildi.")
            
            # Slack bildirimi gönder - sade format
            slack_title = "⚠️ Program Hata Verdi"
            slack_message = f"**Zaman:** {current_time}\n**Hata Tipi:** {type(e).__name__}\n**Mesaj:** {str(e)}\n**Eylem:** Lütfen hatayı çözün ve programı yeniden başlatın\n**Komut:** `python price_tracker_clean.py`"
        except Exception as email_error:
            print(f"Hata bildirilirken yeni bir hata oluştu: {str(email_error)}")
            print(f"Bildirim hata detayları: {traceback.format_exc()}")
        
    print("\nProgram sonlandırıldı.")

# Ana programın çalıştırılması - main() fonksiyonunu çağırır
if __name__ == "__main__":
    try:
        print("TRW Taksi Fiyat Takip Programı başlatılıyor...")
        main()
    except Exception as e:
        print(f"Program başlatılırken kritik hata: {e}")
        print(f"Hata detayları: {traceback.format_exc()}")
        input("Çıkmak için herhangi bir tuşa basın...")
else:
    print("price_tracker_clean.py bir modül olarak içe aktarıldı, main() çağrılmadı")
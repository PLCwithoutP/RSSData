import tkinter as tk

weather_text = """
Tarih: 29.06.2025
Yayın No: 538
Periyot: 29.06.2025 - 06:00 / 30.06.2025 - 06:00

Genel Durum:
Meteoroloji Genel Müdürlüğü tarafından yapılan tahminlere göre:
Ülkemizin kuzey kesimlerinin parçalı, yer yer çok bulutlu,
Marmara'nın doğusu, Karadeniz (Gümüşhane ve Bayburt hariç) ile
Doğu Anadolu'nun kuzeydoğusunun yerel sağanak ve gök gürültülü
sağanak yağışlı, diğer yerlerin az bulutlu ve açık geçeceği tahmin ediliyor.

Yağışların Zonguldak, Bartın, Kastamonu, Sinop, Ordu ve Doğu Karadeniz kıyıları
ile Doğu Anadolu'nun kuzeydoğusunda yer yer kuvvetli olması bekleniyor.
"""

# Create the main window
root = tk.Tk()
root.title("Günlük Hava Durumu")
root.geometry("500x300")

# Make the window non-resizable
root.resizable(False, False)

# Create a label to display the weather
label = tk.Label(root, text=weather_text, justify="left", anchor="nw", padx=10, pady=10, font=("Arial", 10))
label.pack(fill="both", expand=True)

# Run the UI loop
root.mainloop()

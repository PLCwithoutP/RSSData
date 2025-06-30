import tkinter as tk
from xmlReaderSimple_v1 import get_weather_summary

# === UI Setup ===
root = tk.Tk()
root.title("MGM Canlı Hava Durumu")
root.geometry("650x500")
root.resizable(True, True)

weather_text = get_weather_summary()

text_widget = tk.Text(root, wrap="word", font=("Arial", 10))
text_widget.insert("1.0", weather_text)
text_widget.config(state="disabled")
text_widget.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()


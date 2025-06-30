import tkinter as tk
from tkinter import ttk
from xmlReaderSimple_v2 import get_general, get_regional, get_city_data, get_xml_data

# === Main Application ===
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MGM Canlı Hava Durumu")
        self.root.geometry("700x700")
        self.root.resizable(True, True)

        self.mode = tk.StringVar(value="light")  # Theme mode
        self.city_var = tk.StringVar()  # Selected city for dropdown

        self.create_widgets()
        self.apply_theme()
        self.load_general()
        self.load_regions()
        self.load_city_list()

    def create_widgets(self):
        # === Theme Toggle ===
        self.theme_frame = tk.Frame(self.root)
        self.theme_frame.pack(pady=(5, 0), fill="x")

        tk.Label(self.theme_frame, text="Tema:").pack(side="left", padx=(10, 5))
        self.theme_menu = ttk.OptionMenu(self.theme_frame, self.mode, "light", "light", "dark", command=self.apply_theme)
        self.theme_menu.pack(side="left")

        # === General Situation ===
        self.general_label = tk.Label(self.root, text="Genel Hava Durumu", font=("Arial", 12, "bold"))
        self.general_label.pack(pady=(10, 0))

        self.general_text = tk.Text(self.root, wrap="word", font=("Arial", 10), height=6)
        self.general_text.config(state="disabled")
        self.general_text.pack(fill="x", padx=10)

        # === Regional Forecasts ===
        self.region_frame = tk.Frame(self.root)
        self.region_frame.pack(pady=10, fill="x")

        tk.Label(self.region_frame, text="Bölge Seçin:").pack(side="left", padx=(10, 5))
        self.region_var = tk.StringVar()
        self.region_menu = ttk.OptionMenu(self.region_frame, self.region_var, "", command=self.display_region)
        self.region_menu.pack(side="left")

        self.region_text = tk.Text(self.root, wrap="word", font=("Arial", 10), height=8)
        self.region_text.config(state="disabled")
        self.region_text.pack(fill="x", padx=10)

        # === City Data Section ===
        self.city_frame = tk.Frame(self.root)
        self.city_frame.pack(pady=10, fill="x")

        tk.Label(self.city_frame, text="Şehir:").pack(side="left", padx=(10, 5))
        self.city_menu = ttk.Combobox(self.city_frame, textvariable=self.city_var, state="readonly")
        self.city_menu.pack(side="left")
        self.city_menu.bind("<<ComboboxSelected>>", self.on_city_selected)

        self.city_text = tk.Text(self.root, wrap="word", font=("Arial", 10), height=10)
        self.city_text.config(state="disabled")
        self.city_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def apply_theme(self, *args):
        theme = self.mode.get()
        bg = "#ffffff" if theme == "light" else "#2e2e2e"
        fg = "#000000" if theme == "light" else "#f0f0f0"

        widgets = [
            self.general_text, self.region_text, self.city_text,
            self.general_label
        ]
        for widget in widgets:
            try:
                widget.config(bg=bg, fg=fg, insertbackground=fg)
            except:
                pass

        self.root.config(bg=bg)
        for frame in [self.theme_frame, self.region_frame, self.city_frame]:
            frame.config(bg=bg)
            for child in frame.winfo_children():
                try:
                    child.config(bg=bg, fg=fg)
                except:
                    pass

    def load_general(self):
        self.general_text.config(state="normal")
        self.general_text.delete("1.0", tk.END)
        self.general_text.insert("1.0", get_general())
        self.general_text.config(state="disabled")

    def load_regions(self):
        self.regions = get_regional()
        region_names = [v.split('\n')[0][2:].strip() for v in self.regions.values() if isinstance(v, str)]
        keys = list(self.regions.keys())
        self.region_key_map = dict(zip(region_names, keys))

        menu = self.region_menu["menu"]
        menu.delete(0, "end")

        for name in region_names:
            menu.add_command(label=name, command=lambda v=name: self.set_region(v))

        if region_names:
            self.set_region(region_names[0])

    def set_region(self, region_display_name):
        self.region_var.set(region_display_name)
        self.display_region(region_display_name)

    def display_region(self, region_display_name):
        key = self.region_key_map.get(region_display_name, None)
        if key and key in self.regions:
            self.region_text.config(state="normal")
            self.region_text.delete("1.0", tk.END)
            self.region_text.insert("1.0", self.regions[key])
            self.region_text.config(state="disabled")

    def load_city_list(self):
        try:
            # Use pre-parsed XML root from get_city_data to avoid re-downloading
            root = get_xml_data("https://www.mgm.gov.tr/FTPDATA/analiz/sonSOA.xml")
            city_set = set()
            for sehir in root.findall(".//sehirler"):
                name = sehir.findtext("ili", "").strip()
                if name:
                    city_set.add(name)
            cities = sorted(city_set)
            self.city_menu["values"] = cities
            if "Ankara" in cities:
                self.city_var.set("Ankara")
                self.load_city("Ankara")
        except Exception as e:
            self.city_var.set("Hata")

    def on_city_selected(self, event):
        self.load_city(self.city_var.get())

    def load_city(self, city_name):
        self.city_text.config(state="normal")
        self.city_text.delete("1.0", tk.END)
        self.city_text.insert("1.0", get_city_data(city_name))
        self.city_text.config(state="disabled")

# === App Launch ===
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()


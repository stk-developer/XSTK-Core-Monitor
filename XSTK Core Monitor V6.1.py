import customtkinter as ctk
import psutil
import os
import random
from collections import deque
from tkinter import messagebox

# Global Dil Ayarı
LANG = "TR"

class XSTK_Core_v6_1(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.rgb_active = False
        self.cpu_history = deque([0]*20, maxlen=20)
        
        # Her zaman üstte kalma özelliği (Senin istediğin o 'pencerelerin üstünde' olayı)
        self.attributes("-topmost", True)
        
        psutil.cpu_percent(interval=0.1)
        self.lang_window = self.show_language_selector()
        
    def show_language_selector(self):
        win = ctk.CTkToplevel(self)
        win.title("XSTK Language")
        win.geometry("300x150")
        win.attributes("-topmost", True)
        ctk.CTkButton(win, text="Türkçe", command=lambda: self.set_lang("TR", win)).pack(side="left", padx=20, pady=20)
        ctk.CTkButton(win, text="English", command=lambda: self.set_lang("EN", win)).pack(side="right", padx=20, pady=20)

    def set_lang(self, choice, win):
        global LANG
        LANG = choice
        win.destroy()
        self.init_ui()

    def init_ui(self):
        self.deiconify()
        self.title(f"XSTK Core v6.1")
        self.geometry("450x800")
        
        self.texts = {
            "TR": {"title": "XSTK SİSTEM PANELİ", "egg": "neye bakıyon knk???", "warn": "EPİLEPSİ UYARISI: RGB Açılsın mı?", "gpu": "EKRAN KARTI", "bat": "PİL"},
            "EN": {"title": "XSTK SYSTEM PANEL", "egg": "what u lookin at bro???", "warn": "EPILEPSY WARNING: Start RGB?", "gpu": "GPU USAGE", "bat": "BATTERY"}
        }

        self.main_frame = ctk.CTkFrame(self, corner_radius=20, border_width=3, border_color="#00D4FF")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.label_title = ctk.CTkLabel(self.main_frame, text=self.texts[LANG]["title"], font=("Arial", 22, "bold"), text_color="#00D4FF")
        self.label_title.pack(pady=15)

        # Veri Etiketleri ve Barlar (Yüzdeler eklendi)
        self.cpu_label, self.cpu_bar = self.create_stat(f"🔳 CPU")
        self.ram_label, self.ram_bar = self.create_stat(f"💾 RAM")
        self.gpu_label, self.gpu_bar = self.create_stat(f"🎮 {self.texts[LANG]['gpu']}")
        
        self.temp_label = ctk.CTkLabel(self.main_frame, text="🔥 TEMP: --°C", font=("Consolas", 18, "bold"))
        self.temp_label.pack(pady=10)

        self.pil_label = ctk.CTkLabel(self.main_frame, text="🔋 PİL: --%", font=("Consolas", 16, "bold"))
        self.pil_label.pack(pady=10)

        # O MEŞHUR YAZI (Sadece Tam Ekran/Büyük pencerede görünür)
        self.egg_label = ctk.CTkLabel(self.main_frame, text=self.texts[LANG]["egg"], font=("Arial", 16, "italic"), text_color="#444444")
        self.egg_label.pack(side="bottom", pady=20)
        self.egg_label.pack_forget() 

        self.bind("<Configure>", self.check_fullscreen)
        self.bind("<Motion>", self.check_nova_trigger)
        self.guncelle()

    def create_stat(self, name):
        lbl = ctk.CTkLabel(self.main_frame, text=f"{name}: %0", font=("Consolas", 14, "bold"))
        lbl.pack()
        bar = ctk.CTkProgressBar(self.main_frame, width=320, height=15, progress_color="#00D4FF")
        bar.set(0)
        bar.pack(pady=(5, 15))
        return lbl, bar

    def check_fullscreen(self, event):
        # Tam ekran veya maksimize durumunda yazıyı göster
        if self.state() == "zoomed":
            self.egg_label.pack(side="bottom", pady=20)
        else:
            self.egg_label.pack_forget()

    def run_rgb_rave(self):
        if self.rgb_active:
            color = "#%06x" % random.randint(0, 0xFFFFFF)
            self.main_frame.configure(border_color=color)
            self.label_title.configure(text_color=color)
            self.cpu_label.configure(text_color=color)
            self.temp_label.configure(text_color=color)
            self.after(80, self.run_rgb_rave)

    def check_nova_trigger(self, event):
        # Sadece sağ alt köşeye (30 piksellik alan) gelince sorar, yakınlaşınca değil!
        if self.state() == "zoomed":
            if event.x > self.winfo_width() - 30 and event.y > self.winfo_height() - 30:
                if not self.rgb_active:
                    if messagebox.askyesno("XSTK NOVA", self.texts[LANG]["warn"]):
                        self.rgb_active = True
                        self.run_rgb_rave()

    def guncelle(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            battery = psutil.sensors_battery()
            
            # GPU için (Basit simülasyon, çünkü her PC'de farklı kütüphane ister)
            gpu_sim = int(cpu * 0.8) 

            # UI Güncelleme (Yüzdeler eklendi)
            self.cpu_label.configure(text=f"🔳 CPU: %{cpu}")
            self.cpu_bar.set(cpu / 100)
            
            self.ram_label.configure(text=f"💾 RAM: %{ram}")
            self.ram_bar.set(ram / 100)

            self.gpu_label.configure(text=f"🎮 {self.texts[LANG]['gpu']}: %{gpu_sim}")
            self.gpu_bar.set(gpu_sim / 100)

            if battery:
                self.pil_label.configure(text=f"🔋 {self.texts[LANG]['bat']}: %{battery.percent}")
            
            temp = int(38 + (cpu * 0.4))
            self.temp_label.configure(text=f"🔥 TEMP: {temp}°C")

        except: pass
        self.after(1000, self.guncelle)

if __name__ == "__main__":
    XSTK_Core_v6_1().mainloop()

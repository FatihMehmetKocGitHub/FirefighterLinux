#!/usr/bin/env python3
import gi
import os
import subprocess
import webbrowser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

DISABLE_FILE = os.path.expanduser("~/.config/firefighter-welcome-disabled")

LINKS = {
    "GitHub (Kaynak Kodu)": "https://github.com/FatihMehmetKocGitHub/FirefighterLinux",
    "Web Sitesi": "https://firefighterlinux.org",
    "KlavunOS (Paydaş Distro)": "https://boraklavun.blog/klavunos/",
    "LinkedIn": "https://www.linkedin.com/in/fatih-mehmet-ko%C3%A7",
    "Instagram": "https://www.instagram.com/fatihmehmet_koc",
    "X (Twitter)": "https://x.com/FatihMehmetKoc",
    "NSosyal / Teknofest Sosyal": "https://nsosyal.com",
}

class WelcomeWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Firefighter Linux V1.0 — Hoş Geldiniz")

        self.set_default_size(900, 680)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(0)

        css = b"""
        window { background: #f4f4f4; }
        .main-title { font-size: 24px; font-weight: bold; color: #111111; }
        .section-title { font-size: 15px; font-weight: bold; color: #111111; }
        .body-text { font-size: 12px; color: #222222; }
        .quote-text { font-style: italic; color: #333333; }
        button { padding: 8px; }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(outer)

        header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        header.set_margin_top(18)
        header.set_margin_bottom(10)
        header.set_margin_start(24)
        header.set_margin_end(24)
        outer.pack_start(header, False, False, 0)

        title = Gtk.Label(label="Firefighter Linux V1.0")
        title.get_style_context().add_class("main-title")
        title.set_xalign(0)
        header.pack_start(title, False, False, 0)

        subtitle = Gtk.Label(
            label="Offline-first afet koordinasyonu ve acil durum iletişimi için Linux dağıtımı"
        )
        subtitle.set_xalign(0)
        subtitle.get_style_context().add_class("body-text")
        header.pack_start(subtitle, False, False, 0)

        outer.pack_start(Gtk.Separator(), False, False, 0)

        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        content_box.set_margin_top(18)
        content_box.set_margin_bottom(12)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        outer.pack_start(content_box, True, True, 0)

        left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content_box.pack_start(left, True, True, 0)

        intro = Gtk.Label()
        intro.set_xalign(0)
        intro.set_yalign(0)
        intro.set_line_wrap(True)
        intro.set_markup(
            "<b>Merhaba, ben Fatih Mehmet Koç.</b>\n\n"
            "Ben bir itfaiyeci ve bilgisayar programcısıyım.\n"
            "Kendi bilgi birikimim, merakım ve gönüllü analizlerimle bireysel olarak geliştirdiğim "
            "<b>Firefighter Linux</b>, afet sahası, saha profili ve kriz masası kullanım senaryoları için "
            "tasarlanmış <b>offline-first</b> bir Linux dağıtımıdır.\n\n"
            "Bu proje; internet bağlantısının olmadığı veya kesintiye uğradığı afet ortamlarında "
            "bilgi kaydı, konum paylaşımı, fotoğraf aktarımı, harita işaretleme ve saha koordinasyonunu "
            "kolaylaştırmayı hedefler.\n\n"
            "Bu tamamen bağımsız ve bireysel bir açık kaynak projedir; hiçbir resmi kurum ya da kuruluşu temsil etmez."
        )
        intro.get_style_context().add_class("body-text")
        left.pack_start(intro, False, False, 0)

        feature_title = Gtk.Label()
        feature_title.set_xalign(0)
        feature_title.set_markup("<b>Öne çıkan özellikler:</b>")
        feature_title.get_style_context().add_class("section-title")
        left.pack_start(feature_title, False, False, 0)

        features = Gtk.Label()
        features.set_xalign(0)
        features.set_yalign(0)
        features.set_line_wrap(True)
        features.set_text(
            "• Offline rapor sistemi\n"
            "• Fotoğraf ekleme ve saha verisi kaydı\n"
            "• Konum paylaşımı ve harita işaretleme\n"
            "• SQLite yerel veritabanı\n"
            "• JSON dışa/içe aktarma\n"
            "• VDS merkezi API ve PostgreSQL altyapısı\n"
            "• LoRa / Meshtastic hazırlığı\n"
            "• APX / AX.25 tabanlı haberleşme hedefi\n"
            "• Node-RED ile alarm ve otomasyon hedefi\n"
            "• Firefighter Linux güncelleme altyapısı\n"
            "• Calamares ile kurulum desteği\n"
            "• GNOME test ortamı, XFCE hafif/saha masaüstü"
        )
        features.get_style_context().add_class("body-text")
        left.pack_start(features, False, False, 0)

        purpose = Gtk.Label()
        purpose.set_xalign(0)
        purpose.set_yalign(0)
        purpose.set_line_wrap(True)
        purpose.set_markup(
            "<b>Amaç:</b> Türkiye Cumhuriyeti Devleti ve Türk Milletine gönüllü katkı sağlamak; "
            "afet anında bilgi akışını hızlandırmak, sahadaki ekiplerin koordinasyonunu kolaylaştırmak "
            "ve hayat kurtarmaya destek olmaktır."
        )
        purpose.get_style_context().add_class("body-text")
        left.pack_start(purpose, False, False, 0)

        feedback = Gtk.Label()
        feedback.set_xalign(0)
        feedback.set_line_wrap(True)
        feedback.set_markup(
            "<b>Geri bildirim vermekten çekinmeyin!</b>\n"
            "Bu proje, her öneri ve katkıyla daha ileriye taşınacaktır. "
            "Hep birlikte daha iyisini yapabiliriz."
        )
        feedback.get_style_context().add_class("body-text")
        left.pack_start(feedback, False, False, 0)

        quote = Gtk.Label()
        quote.set_xalign(0)
        quote.set_line_wrap(True)
        quote.set_markup(
            "<i>“Felaket başa gelmeden evvel, koruyucu ve önleyici tedbirleri düşünmek lazımdır.\n"
            "Geldikten sonra dövünmenin yararı yoktur.”</i>\n"
            "— Mustafa Kemal Atatürk"
        )
        quote.get_style_context().add_class("quote-text")
        left.pack_start(quote, False, False, 0)

        right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        right.set_size_request(260, -1)
        content_box.pack_start(right, False, False, 0)

        quick_title = Gtk.Label()
        quick_title.set_markup("<b>Hızlı Erişim</b>")
        quick_title.set_xalign(0)
        right.pack_start(quick_title, False, False, 0)

        install_btn = Gtk.Button(label="Firefighter Linux Kur")
        install_btn.connect(
            "clicked",
            self.run_command,
            "xfce4-terminal --title='Firefighter Linux Kurulum' --command='bash -lc \"sudo calamares; exec bash\"'"
        )
        right.pack_start(install_btn, False, False, 0)

        sysinfo_btn = Gtk.Button(label="Sistem Bilgisi")
        sysinfo_btn.connect(
            "clicked",
            self.run_command,
            "xfce4-terminal --title='Firefighter Linux Sistem Bilgisi' --command='bash -lc \"echo Firefighter Linux V1.0; echo; lsb_release -a; echo; uname -a; echo; echo Masaustu oturumu: $XDG_CURRENT_DESKTOP; echo; read -p Enter\"'"
        )
        right.pack_start(sysinfo_btn, False, False, 0)

        repo_btn = Gtk.Button(label="Proje Klasörü")
        repo_btn.connect("clicked", self.run_command, "xdg-open /home/fatih/FirefighterLinux")
        right.pack_start(repo_btn, False, False, 0)

        docs_btn = Gtk.Button(label="Dokümantasyon")
        docs_btn.connect(
            "clicked",
            self.open_url,
            "https://github.com/FatihMehmetKocGitHub/FirefighterLinux/tree/main/docs",
        )
        right.pack_start(docs_btn, False, False, 0)

        right.pack_start(Gtk.Separator(), False, False, 8)

        for name, url in LINKS.items():
            btn = Gtk.Button(label=name)
            btn.connect("clicked", self.open_url, url)
            right.pack_start(btn, False, False, 0)

        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        footer.set_margin_start(24)
        footer.set_margin_end(24)
        footer.set_margin_bottom(18)
        outer.pack_start(footer, False, False, 0)

        self.disable_check = Gtk.CheckButton(label="Bir daha gösterme")
        footer.pack_start(self.disable_check, False, False, 0)

        footer.pack_start(Gtk.Label(), True, True, 0)

        close_btn = Gtk.Button(label="Başla")
        close_btn.connect("clicked", self.close_app)
        footer.pack_start(close_btn, False, False, 0)

    def open_url(self, widget, url):
        webbrowser.open(url)

    def run_command(self, widget, command):
        subprocess.Popen(command, shell=True)

    def close_app(self, widget):
        if self.disable_check.get_active():
            os.makedirs(os.path.dirname(DISABLE_FILE), exist_ok=True)
            with open(DISABLE_FILE, "w") as f:
                f.write("disabled\n")
        Gtk.main_quit()


if __name__ == "__main__":
    if os.path.exists(DISABLE_FILE):
        raise SystemExit(0)

    win = WelcomeWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

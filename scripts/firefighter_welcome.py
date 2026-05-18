#!/usr/bin/env python3
import os
import subprocess
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

HOME = os.path.expanduser("~")
MARKER = os.path.join(HOME, ".config", "firefighter-welcome-disabled")

LINKS = {
    "GitHub": "https://github.com/FatihMehmetKocGitHub",
    "Web Sitesi": "https://firefighterlinux.org",
    "KlavunOS": "https://boraklavun.blog/klavunos/",
    "LinkedIn": "https://tr.linkedin.com/in/fatihmehmetkoc",
    "Instagram": "https://www.instagram.com/fatihmehmet_koc/",
    "X": "https://x.com/koc_fatihmehmet",
    "NSosyal": "https://nsosyal.com/fatihmehmetkoc",
}

class FirefighterWelcome(Gtk.Window):
    def __init__(self):
        super().__init__(title="Firefighter Linux v1.0 - Hoş Geldiniz")
        self.set_default_size(820, 620)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(0)

        css = b"""
        window {
            background: #f4f4f4;
        }
        .header {
            background: #111111;
            color: #ffffff;
            padding: 18px;
        }
        .title {
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
        }
        .subtitle {
            font-size: 13px;
            color: #d7d7d7;
        }
        .content {
            background: #ffffff;
            padding: 22px;
        }
        .section-title {
            font-size: 16px;
            font-weight: 700;
            color: #8f171b;
        }
        .body {
            font-size: 13px;
            color: #222222;
        }
        .quote {
            font-size: 12px;
            color: #555555;
            font-style: italic;
        }
        button {
            padding: 7px 12px;
        }
        .danger {
            color: #8f171b;
            font-weight: 700;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(root)

        header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        header.get_style_context().add_class("header")
        root.pack_start(header, False, False, 0)

        title = Gtk.Label(label="Firefighter Linux v1.0")
        title.set_xalign(0)
        title.get_style_context().add_class("title")
        header.pack_start(title, False, False, 0)

        subtitle = Gtk.Label(label="Afet, kriz koordinasyonu ve offline haberleşme için bağımsız Linux projesi")
        subtitle.set_xalign(0)
        subtitle.get_style_context().add_class("subtitle")
        header.pack_start(subtitle, False, False, 0)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        content.set_margin_top(18)
        content.set_margin_bottom(18)
        content.set_margin_start(24)
        content.set_margin_end(24)
        content.get_style_context().add_class("content")
        root.pack_start(content, True, True, 0)

        hello = Gtk.Label()
        hello.set_markup("<b>Merhaba, ben Fatih Mehmet Koç</b>")
        hello.set_xalign(0)
        hello.get_style_context().add_class("body")
        content.pack_start(hello, False, False, 0)

        desc = Gtk.Label(
            label=(
                "Ben bir itfaiyeci ve bilgisayar programcısıyım.\n\n"
                "Firefighter Linux; afet sahası, kriz koordinasyonu, offline haberleşme ve saha kullanımı için "
                "geliştirdiğim bağımsız bir Linux projesidir.\n\n"
                "Bu proje herhangi bir resmi kurum veya kuruluşu temsil etmez."
            )
        )
        desc.set_xalign(0)
        desc.set_line_wrap(True)
        desc.get_style_context().add_class("body")
        content.pack_start(desc, False, False, 0)

        sec = Gtk.Label(label="Öne çıkan amaçlar")
        sec.set_xalign(0)
        sec.get_style_context().add_class("section-title")
        content.pack_start(sec, False, False, 0)

        goals = Gtk.Label(
            label=(
                "• İnternetin olmadığı yerlerde haberleşmeye destek olmak\n"
                "• LoRa / mesh / offline sistemlerle saha koordinasyonunu güçlendirmek\n"
                "• Afet anında bilgi akışını hızlandırmak\n"
                "• Gönüllü ekipler ve kriz masaları için açık kaynak bir temel oluşturmak"
            )
        )
        goals.set_xalign(0)
        goals.set_line_wrap(True)
        goals.get_style_context().add_class("body")
        content.pack_start(goals, False, False, 0)

        feedback = Gtk.Label()
        feedback.set_markup("<b>Geri bildirim vermekten çekinmeyin.</b>\nBu proje, her öneri ve katkıyla daha ileriye taşınacaktır.")
        feedback.set_xalign(0)
        feedback.set_line_wrap(True)
        feedback.get_style_context().add_class("body")
        content.pack_start(feedback, False, False, 0)

        quote = Gtk.Label(
            label=(
                "“Felaket başa gelmeden evvel, koruyucu ve önleyici tedbirleri düşünmek lazımdır.”\n"
                "- Mustafa Kemal Atatürk"
            )
        )
        quote.set_xalign(0)
        quote.set_line_wrap(True)
        quote.get_style_context().add_class("quote")
        content.pack_start(quote, False, False, 0)

        buttons = Gtk.Grid()
        buttons.set_column_spacing(8)
        buttons.set_row_spacing(8)
        content.pack_end(buttons, False, False, 0)

        names = list(LINKS.keys())
        for i, name in enumerate(names):
            btn = Gtk.Button(label=name)
            btn.connect("clicked", self.open_link, LINKS[name])
            buttons.attach(btn, i % 4, i // 4, 1, 1)

        bottom = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        bottom.set_margin_start(24)
        bottom.set_margin_end(24)
        bottom.set_margin_bottom(16)
        root.pack_end(bottom, False, False, 0)

        self.check = Gtk.CheckButton(label="Bir daha gösterme")
        bottom.pack_start(self.check, False, False, 0)

        spacer = Gtk.Box()
        bottom.pack_start(spacer, True, True, 0)

        close = Gtk.Button(label="Kapat")
        close.connect("clicked", self.close_app)
        bottom.pack_end(close, False, False, 0)

        self.connect("destroy", Gtk.main_quit)

    def open_link(self, widget, url):
        subprocess.Popen(["xdg-open", url])

    def close_app(self, widget):
        if self.check.get_active():
            os.makedirs(os.path.dirname(MARKER), exist_ok=True)
            with open(MARKER, "w") as f:
                f.write("disabled\n")
        Gtk.main_quit()

if __name__ == "__main__":
    if os.path.exists(MARKER):
        raise SystemExit(0)
    win = FirefighterWelcome()
    win.show_all()
    Gtk.main()

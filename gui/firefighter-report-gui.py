import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
import sqlite3
import os
import shutil
import time

FFL_DIR = os.path.expanduser("~/.firefighterlinux")
DB = os.path.join(FFL_DIR, "firefighter.db")
PHOTOS_DIR = os.path.join(FFL_DIR, "photos")

class FirefighterGUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Firefighter Linux Report System")

        self.set_border_width(12)
        self.set_default_size(480, 430)

        self.lang = "tr"
        self.photo_path = ""

        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.add(grid)

        self.lang_combo = Gtk.ComboBoxText()
        self.lang_combo.append_text("Türkçe")
        self.lang_combo.append_text("English")
        self.lang_combo.set_active(0)
        self.lang_combo.connect("changed", self.change_language)

        grid.attach(Gtk.Label(label="Dil / Language"), 0, 0, 1, 1)
        grid.attach(self.lang_combo, 1, 0, 1, 1)

        self.type_label = Gtk.Label(label="Olay Türü")
        self.note_label = Gtk.Label(label="Not")
        self.lat_label = Gtk.Label(label="Enlem")
        self.lon_label = Gtk.Label(label="Boylam")
        self.status_label = Gtk.Label(label="Durum")
        self.photo_label = Gtk.Label(label="Fotoğraf: Yok")

        self.type_entry = Gtk.Entry()
        self.note_entry = Gtk.Entry()
        self.lat_entry = Gtk.Entry()
        self.lon_entry = Gtk.Entry()
        self.status_entry = Gtk.Entry()

        grid.attach(self.type_label, 0, 1, 1, 1)
        grid.attach(self.type_entry, 1, 1, 1, 1)

        grid.attach(self.note_label, 0, 2, 1, 1)
        grid.attach(self.note_entry, 1, 2, 1, 1)

        grid.attach(self.lat_label, 0, 3, 1, 1)
        grid.attach(self.lat_entry, 1, 3, 1, 1)

        grid.attach(self.lon_label, 0, 4, 1, 1)
        grid.attach(self.lon_entry, 1, 4, 1, 1)

        grid.attach(self.status_label, 0, 5, 1, 1)
        grid.attach(self.status_entry, 1, 5, 1, 1)

        self.photo_button = Gtk.Button(label="Fotoğraf Seç")
        self.photo_button.connect("clicked", self.choose_photo)
        grid.attach(self.photo_button, 1, 6, 1, 1)

        grid.attach(self.photo_label, 1, 7, 1, 1)

        self.save_button = Gtk.Button(label="Kaydet")
        self.save_button.connect("clicked", self.save_report)
        grid.attach(self.save_button, 1, 8, 1, 1)

        self.map_button = Gtk.Button(label="Haritayı Aç")
        self.map_button.connect("clicked", self.open_map)
        grid.attach(self.map_button, 1, 9, 1, 1)

    def change_language(self, combo):
        text = combo.get_active_text()

        if text == "English":
            self.lang = "en"
            self.type_label.set_text("Type")
            self.note_label.set_text("Note")
            self.lat_label.set_text("Latitude")
            self.lon_label.set_text("Longitude")
            self.status_label.set_text("Status")
            self.photo_button.set_label("Choose Photo")
            self.save_button.set_label("Save Report")
            self.map_button.set_label("Open Map")
            self.set_title("Firefighter Linux Report System")
        else:
            self.lang = "tr"
            self.type_label.set_text("Olay Türü")
            self.note_label.set_text("Not")
            self.lat_label.set_text("Enlem")
            self.lon_label.set_text("Boylam")
            self.status_label.set_text("Durum")
            self.photo_button.set_label("Fotoğraf Seç")
            self.save_button.set_label("Kaydet")
            self.map_button.set_label("Haritayı Aç")
            self.set_title("Firefighter Linux Rapor Sistemi")

    def choose_photo(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Fotoğraf Seç" if self.lang == "tr" else "Choose Photo",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )

        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK
        )

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.photo_path = dialog.get_filename()
            self.photo_label.set_text(os.path.basename(self.photo_path))

        dialog.destroy()

    def save_report(self, widget):
        incident_type = self.type_entry.get_text()
        note = self.note_entry.get_text()

        if not incident_type or not note:
            self.show_message(
                "Hata: Olay türü ve not boş bırakılamaz."
                if self.lang == "tr"
                else "Error: Type and note cannot be empty."
            )
            return

        os.makedirs(FFL_DIR, exist_ok=True)
        os.makedirs(PHOTOS_DIR, exist_ok=True)

        final_photo = ""

        if self.photo_path and os.path.isfile(self.photo_path):
            filename = f"{int(time.time())}-{os.path.basename(self.photo_path)}"
            final_photo = os.path.join(PHOTOS_DIR, filename)
            shutil.copy(self.photo_path, final_photo)

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            note TEXT,
            latitude TEXT,
            longitude TEXT,
            status TEXT,
            photo_path TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cur.execute("""
        INSERT INTO reports
        (type, note, latitude, longitude, status, photo_path)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            incident_type,
            note,
            self.lat_entry.get_text(),
            self.lon_entry.get_text(),
            self.status_entry.get_text(),
            final_photo
        ))

        conn.commit()
        conn.close()

        self.show_message(
            "Kayıt fotoğrafla birlikte kaydedildi."
            if self.lang == "tr"
            else "Report saved with photo."
        )

    def open_map(self, widget):
        os.system("ffl-map &")

    def show_message(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

win = FirefighterGUI()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
import sqlite3
import os
import shutil
import time
import subprocess

FFL_DIR = os.path.expanduser("~/.firefighterlinux")
DB = os.path.join(FFL_DIR, "firefighter.db")
PHOTOS_DIR = os.path.join(FFL_DIR, "photos")


class FirefighterGUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Firefighter Linux Rapor Sistemi")

        self.set_border_width(12)
        self.set_default_size(520, 520)

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
        self.address_label = Gtk.Label(label="Adres")
        self.lat_label = Gtk.Label(label="Enlem")
        self.lon_label = Gtk.Label(label="Boylam")
        self.status_label = Gtk.Label(label="Durum")
        self.photo_label = Gtk.Label(label="Fotoğraf: Yok")

        self.type_entry = Gtk.Entry()
        self.note_entry = Gtk.Entry()
        self.address_entry = Gtk.Entry()
        self.lat_entry = Gtk.Entry()
        self.lon_entry = Gtk.Entry()
        self.status_entry = Gtk.Entry()

        self.type_entry.set_placeholder_text("deprem / yangın / yaralı / sos")
        self.note_entry.set_placeholder_text("Kısa açıklama")
        self.address_entry.set_placeholder_text("Mahalle, sokak, bina vb.")
        self.status_entry.set_placeholder_text("critical / open / closed")

        grid.attach(self.type_label, 0, 1, 1, 1)
        grid.attach(self.type_entry, 1, 1, 1, 1)

        grid.attach(self.note_label, 0, 2, 1, 1)
        grid.attach(self.note_entry, 1, 2, 1, 1)

        grid.attach(self.address_label, 0, 3, 1, 1)
        grid.attach(self.address_entry, 1, 3, 1, 1)

        grid.attach(self.lat_label, 0, 4, 1, 1)
        grid.attach(self.lat_entry, 1, 4, 1, 1)

        grid.attach(self.lon_label, 0, 5, 1, 1)
        grid.attach(self.lon_entry, 1, 5, 1, 1)

        grid.attach(self.status_label, 0, 6, 1, 1)
        grid.attach(self.status_entry, 1, 6, 1, 1)

        self.photo_button = Gtk.Button(label="Fotoğraf Seç")
        self.photo_button.connect("clicked", self.choose_photo)
        grid.attach(self.photo_button, 1, 7, 1, 1)

        grid.attach(self.photo_label, 1, 8, 1, 1)

        self.save_button = Gtk.Button(label="Kaydet")
        self.save_button.connect("clicked", self.save_report)
        grid.attach(self.save_button, 1, 9, 1, 1)

        self.sync_button = Gtk.Button(label="Merkeze Gönder")
        self.sync_button.connect("clicked", self.sync_reports)
        grid.attach(self.sync_button, 1, 10, 1, 1)

        self.map_button = Gtk.Button(label="Haritayı Aç")
        self.map_button.connect("clicked", self.open_map)
        grid.attach(self.map_button, 1, 11, 1, 1)

    def change_language(self, combo):
        text = combo.get_active_text()

        if text == "English":
            self.lang = "en"
            self.type_label.set_text("Type")
            self.note_label.set_text("Note")
            self.address_label.set_text("Address")
            self.lat_label.set_text("Latitude")
            self.lon_label.set_text("Longitude")
            self.status_label.set_text("Status")
            self.photo_button.set_label("Choose Photo")
            self.save_button.set_label("Save Report")
            self.sync_button.set_label("Sync to Central")
            self.map_button.set_label("Open Map")
            self.set_title("Firefighter Linux Report System")
        else:
            self.lang = "tr"
            self.type_label.set_text("Olay Türü")
            self.note_label.set_text("Not")
            self.address_label.set_text("Adres")
            self.lat_label.set_text("Enlem")
            self.lon_label.set_text("Boylam")
            self.status_label.set_text("Durum")
            self.photo_button.set_label("Fotoğraf Seç")
            self.save_button.set_label("Kaydet")
            self.sync_button.set_label("Merkeze Gönder")
            self.map_button.set_label("Haritayı Aç")
            self.set_title("Firefighter Linux Rapor Sistemi")

    def init_db(self):
        os.makedirs(FFL_DIR, exist_ok=True)
        os.makedirs(PHOTOS_DIR, exist_ok=True)

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            note TEXT,
            address TEXT,
            latitude TEXT,
            longitude TEXT,
            status TEXT,
            photo_path TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            synced INTEGER DEFAULT 0
        )
        """)

        existing_columns = [
            row[1] for row in cur.execute("PRAGMA table_info(reports)").fetchall()
        ]

        if "address" not in existing_columns:
            cur.execute("ALTER TABLE reports ADD COLUMN address TEXT DEFAULT ''")

        if "synced" not in existing_columns:
            cur.execute("ALTER TABLE reports ADD COLUMN synced INTEGER DEFAULT 0")

        conn.commit()
        conn.close()

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
        incident_type = self.type_entry.get_text().strip()
        note = self.note_entry.get_text().strip()

        if not incident_type or not note:
            self.show_message(
                "Hata: Olay türü ve not boş bırakılamaz."
                if self.lang == "tr"
                else "Error: Type and note cannot be empty."
            )
            return

        self.init_db()

        final_photo = ""

        if self.photo_path and os.path.isfile(self.photo_path):
            filename = f"{int(time.time())}-{os.path.basename(self.photo_path)}"
            final_photo = os.path.join(PHOTOS_DIR, filename)
            shutil.copy(self.photo_path, final_photo)

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO reports
        (type, note, address, latitude, longitude, status, photo_path, synced)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            incident_type,
            note,
            self.address_entry.get_text().strip(),
            self.lat_entry.get_text().strip(),
            self.lon_entry.get_text().strip(),
            self.status_entry.get_text().strip(),
            final_photo
        ))

        conn.commit()
        conn.close()

        self.show_message(
            "Kayıt kaydedildi. İnternet varsa Merkeze Gönder ile aktarabilirsin."
            if self.lang == "tr"
            else "Report saved. Use Sync to Central if network is available."
        )

        self.clear_form()

    def sync_reports(self, widget):
        try:
            result = subprocess.run(
                ["ffl-auto-sync"],
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            if result.returncode == 0:
                self.show_message(
                    "Senkron tamamlandı:\n" + (output or "Gönderilecek kayıt yok.")
                    if self.lang == "tr"
                    else "Sync completed:\n" + (output or "No records to send.")
                )
            else:
                self.show_message(
                    "Senkron hatası:\n" + (error or output)
                    if self.lang == "tr"
                    else "Sync error:\n" + (error or output)
                )

        except Exception as e:
            self.show_message(
                "Senkron çalıştırılamadı:\n" + str(e)
                if self.lang == "tr"
                else "Sync could not be started:\n" + str(e)
            )

    def clear_form(self):
        self.type_entry.set_text("")
        self.note_entry.set_text("")
        self.address_entry.set_text("")
        self.lat_entry.set_text("")
        self.lon_entry.set_text("")
        self.status_entry.set_text("")
        self.photo_path = ""
        self.photo_label.set_text(
            "Fotoğraf: Yok" if self.lang == "tr" else "Photo: None"
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

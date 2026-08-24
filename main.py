import json
import os
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.metrics import dp, sp

DATA_FILE = "kinderschubser_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "settings": {
            "name": "",
            "personalnummer": "",
            "arbeitsstaette": "",
            "soll_stunden": ""
        },
        "entries": {}
    }

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass

class ModernButton(Button):
    def __init__(self, is_primary=False, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (0.95, 0.96, 0.98, 1)
        self.font_size = sp(14)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(36)
        self.is_primary = is_primary
        with self.canvas.before:
            if self.is_primary:
                Color(0.25, 0.41, 0.88, 1)
            else:
                Color(0.15, 0.18, 0.25, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MainNavigation(AnchorLayout):
    def __init__(self, switch_screen_callback, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.switch_screen_callback = switch_screen_callback
        
        card = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(415), dp(430)), spacing=dp(12), padding=dp(25))
        with card.canvas.before:
            Color(0.11, 0.14, 0.19, 1)
            card.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
        card.bind(pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos), size=lambda i, v: setattr(i.bg_rect, 'size', i.size))
        
        if os.path.exists("logox.png"):
            logo = Image(source="logox.png", size_hint=(None, None), size=(dp(80), dp(80)), pos_hint={'center_x': 0.5})
            card.add_widget(logo)
        
        lbl_title = Label(text="Sabine´s Kinderschubser App", font_size=sp(20), color=(0.95, 0.96, 0.98, 1), bold=True, halign='center', valign='middle', size_hint_y=None, height=dp(36))
        lbl_title.bind(size=lbl_title.setter('text_size'))
        
        card.add_widget(lbl_title)
        card.add_widget(Widget(size_hint_y=None, height=dp(5)))
        
        btn_settings = ModernButton(text="Einstellungen", is_primary=False)
        btn_settings.bind(on_release=lambda x: self.switch_screen_callback("settings"))
        
        btn_time = ModernButton(text="Zeiterfassung", is_primary=False)
        btn_time.bind(on_release=lambda x: self.switch_screen_callback("timesheet"))
        
        btn_overview = ModernButton(text="Übersicht", is_primary=False)
        btn_overview.bind(on_release=lambda x: self.switch_screen_callback("overview"))
        
        btn_report = ModernButton(text="Bericht (Arbeitgeber)", is_primary=True)
        btn_report.bind(on_release=lambda x: self.switch_screen_callback("report"))
        
        card.add_widget(btn_settings)
        card.add_widget(btn_time)
        card.add_widget(btn_overview)
        card.add_widget(btn_report)
        
        self.add_widget(card)

class SettingsView(AnchorLayout):
    def __init__(self, switch_screen_callback, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.switch_screen_callback = switch_screen_callback
        
        data = load_data()
        settings = data.get("settings", {})
        
        card = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(495), dp(370)), spacing=dp(13), padding=dp(23))
        with card.canvas.before:
            Color(0.11, 0.14, 0.19, 1)
            card.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
        card.bind(pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos), size=lambda i, v: setattr(i.bg_rect, 'size', i.size))
        
        lbl_header = Label(text="Einstellungen", font_size=sp(20), color=(0.95, 0.96, 0.98, 1), bold=True, size_hint_y=None, height=dp(36), halign='center', valign='middle')
        lbl_header.bind(size=lbl_header.setter('text_size'))
        card.add_widget(lbl_header)
        
        table_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        table_grid.bind(minimum_height=table_grid.setter('height'))
        
        fields = [
            ("Name", "name"),
            ("Personalnummer", "personalnummer"),
            ("Arbeitsstätte", "arbeitsstaette"),
            ("Soll-Stunden", "soll_stunden")
        ]
        
        self.inputs = {}
        for label_text, key in fields:
            lbl = Label(text=label_text, font_size=sp(14), color=(0.8, 0.83, 0.88, 1), bold=True, size_hint_x=0.45, size_hint_y=None, height=dp(36), halign='left', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            
            txt = TextInput(text=str(settings.get(key, "")), font_size=sp(14), multiline=False, halign='center', size_hint_x=0.55, size_hint_y=None, height=dp(36), background_color=(0.15, 0.18, 0.25, 1), foreground_color=(1, 1, 1, 1), padding=[dp(8), dp(8), dp(8), dp(8)])
            self.inputs[key] = txt
            
            table_grid.add_widget(lbl)
            table_grid.add_widget(txt)
            
        card.add_widget(table_grid)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=dp(13), size_hint_y=None, height=dp(36))
        
        btn_save = ModernButton(text="Speichern", is_primary=True)
        btn_save.bind(on_release=self.save_settings)
        
        btn_back = ModernButton(text="Hauptmenü", is_primary=False)
        btn_back.bind(on_release=lambda x: self.switch_screen_callback("menu"))
        
        btn_layout.add_widget(btn_save)
        btn_layout.add_widget(btn_back)
        
        card.add_widget(btn_layout)
        self.add_widget(card)

    def save_settings(self, instance):
        data = load_data()
        for key, txt_widget in self.inputs.items():
            data["settings"][key] = txt_widget.text.strip()
        save_data(data)

class TimesheetView(AnchorLayout):
    def __init__(self, switch_screen_callback, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.switch_screen_callback = switch_screen_callback
        
        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month
        
        self.min_date = datetime(now.year, now.month, 1) - timedelta(days=92)
        self.max_date = datetime(now.year, now.month, 1) + timedelta(days=122)
        
        card = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(1200), dp(700)), spacing=dp(10), padding=dp(20))
        with card.canvas.before:
            Color(0.11, 0.14, 0.19, 1)
            card.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
        card.bind(pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos), size=lambda i, v: setattr(i.bg_rect, 'size', i.size))
        
        lbl_header = Label(text="Zeiterfassung", font_size=sp(18), color=(0.95, 0.96, 0.98, 1), bold=True, size_hint_y=None, height=dp(30), halign='center', valign='middle')
        lbl_header.bind(size=lbl_header.setter('text_size'))
        card.add_widget(lbl_header)
        
        nav_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(36))
        
        self.btn_prev = Button(text="< Zurück", font_size=sp(12), bold=True, size_hint_x=0.25, background_normal='', background_color=(0.15, 0.18, 0.25, 1), color=(0.95, 0.96, 0.98, 1))
        self.btn_prev.bind(on_release=self.prev_month)
        
        self.lbl_month = Label(text="", font_size=sp(14), bold=True, color=(0.95, 0.96, 0.98, 1), size_hint_x=0.5, halign='center', valign='middle')
        self.lbl_month.bind(size=self.lbl_month.setter('text_size'))
        
        self.btn_next = Button(text="Vor >", font_size=sp(12), bold=True, size_hint_x=0.25, background_normal='', background_color=(0.15, 0.18, 0.25, 1), color=(0.95, 0.96, 0.98, 1))
        self.btn_next.bind(on_release=self.next_month)
        
        nav_layout.add_widget(self.btn_prev)
        nav_layout.add_widget(self.lbl_month)
        nav_layout.add_widget(self.btn_next)
        card.add_widget(nav_layout)
        
        headers_layout = GridLayout(cols=6, spacing=dp(5), size_hint_y=None, height=dp(28))
        headers = ["Datum", "Kommen", "Gehn", "Pause", "Bemerkung", "Stunden"]
        for h in headers:
            headers_layout.add_widget(Label(text=h, font_size=sp(12), bold=True, color=(0.8, 0.83, 0.88, 1), halign='center', valign='middle'))
        card.add_widget(headers_layout)
        
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        
        self.table_content = GridLayout(cols=6, spacing=dp(5), size_hint_y=None)
        self.table_content.bind(minimum_height=self.table_content.setter('height'))
        
        scroll.add_widget(self.table_content)
        card.add_widget(scroll)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=dp(13), size_hint_y=None, height=dp(36))
        
        btn_save = ModernButton(text="Monat Speichern", is_primary=True)
        btn_save.bind(on_release=self.save_timesheet)
        
        btn_back = ModernButton(text="Hauptmenü", is_primary=False)
        btn_back.bind(on_release=lambda x: self.switch_screen_callback("menu"))
        
        btn_layout.add_widget(btn_save)
        btn_layout.add_widget(btn_back)
        
        card.add_widget(btn_layout)
        self.add_widget(card)
        
        self.load_month_data()

    def update_month_label(self):
        months_german = ["", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        self.lbl_month.text = f"{months_german[self.current_month]} {self.current_year}"

    def load_month_data(self):
        self.update_month_label()
        self.table_content.clear_widgets()
        self.inputs = {}
        
        data = load_data()
        entries = data.get("entries", {})
        
        if self.current_month == 12:
            next_m_date = datetime(self.current_year + 1, 1, 1)
        else:
            next_m_date = datetime(self.current_year, self.current_month + 1, 1)
        
        last_day = (next_m_date - timedelta(days=1)).day
        weekdays_german = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        
        for day in range(1, last_day + 1):
            current_date = datetime(self.current_year, self.current_month, day)
            date_str = current_date.strftime("%Y-%m-%d")
            wd_index = current_date.weekday()
            wd_text = weekdays_german[wd_index]
            
            day_data = entries.get(date_str, {"kommen": "", "gehn": "", "pause": "", "bemerkung": ""})
            
            text_color = (0.9, 0.3, 0.3, 1) if wd_index >= 5 else (0.9, 0.9, 0.9, 1)
            
            lbl_date = Label(text=f"{wd_text},\n{day:02d}/{self.current_month:02d}/{self.current_year}", font_size=sp(11), color=text_color, size_hint_y=None, height=dp(36), halign='center', valign='middle')
            lbl_date.bind(size=lbl_date.setter('text_size'))
            
            txt_kommen = TextInput(text=str(day_data.get("kommen", "")), font_size=sp(11), multiline=False, halign='center', size_hint_y=None, height=dp(36), background_color=(0.15, 0.18, 0.25, 1), foreground_color=(1, 1, 1, 1), padding=[dp(4), dp(8), dp(4), dp(4)])
            txt_gehn = TextInput(text=str(day_data.get("gehn", "")), font_size=sp(11), multiline=False, halign='center', size_hint_y=None, height=dp(36), background_color=(0.15, 0.18, 0.25, 1), foreground_color=(1, 1, 1, 1), padding=[dp(4), dp(8), dp(4), dp(4)])
            txt_pause = TextInput(text=str(day_data.get("pause", "")), font_size=sp(11), multiline=False, halign='center', size_hint_y=None, height=dp(36), background_color=(0.15, 0.18, 0.25, 1), foreground_color=(1, 1, 1, 1), padding=[dp(4), dp(8), dp(4), dp(4)])
            txt_bemerkung = TextInput(text=str(day_data.get("bemerkung", "")), font_size=sp(11), multiline=False, halign='center', size_hint_y=None, height=dp(36), background_color=(0.15, 0.18, 0.25, 1), foreground_color=(1, 1, 1, 1), padding=[dp(4), dp(8), dp(4), dp(4)])
            
            lbl_total = Label(text="0.0h", font_size=sp(11), color=(0.8, 0.83, 0.88, 1), size_hint_y=None, height=dp(36), halign='center', valign='middle')
            lbl_total.bind(size=lbl_total.setter('text_size'))
            
            self.inputs[date_str] = {
                "kommen": txt_kommen,
                "gehn": txt_gehn,
                "pause": txt_pause,
                "bemerkung": txt_bemerkung,
                "total": lbl_total
            }
            
            self.table_content.add_widget(lbl_date)
            self.table_content.add_widget(txt_kommen)
            self.table_content.add_widget(txt_gehn)
            self.table_content.add_widget(txt_pause)
            self.table_content.add_widget(txt_bemerkung)
            self.table_content.add_widget(lbl_total)

    def prev_month(self, instance):
        new_m = self.current_month - 1
        new_y = self.current_year
        if new_m < 1:
            new_m = 12
            new_y -= 1
        target_date = datetime(new_y, new_m, 1)
        if target_date >= datetime(self.min_date.year, self.min_date.month, 1):
            self.current_month = new_m
            self.current_year = new_y
            self.load_month_data()

    def next_month(self, instance):
        new_m = self.current_month + 1
        new_y = self.current_year
        if new_m > 12:
            new_m = 1
            new_y += 1
        target_date = datetime(new_y, new_m, 1)
        if target_date <= datetime(self.max_date.year, self.max_date.month, 1):
            self.current_month = new_m
            self.current_year = new_y
            self.load_month_data()

    def save_timesheet(self, instance):
        data = load_data()
        if "entries" not in data:
            data["entries"] = {}
        for date_str, widgets in self.inputs.items():
            data["entries"][date_str] = {
                "kommen": widgets["kommen"].text.strip(),
                "gehn": widgets["gehn"].text.strip(),
                "pause": widgets["pause"].text.strip(),
                "bemerkung": widgets["bemerkung"].text.strip()
            }
        save_data(data)

class OverviewView(AnchorLayout):
    def __init__(self, switch_screen_callback, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.switch_screen_callback = switch_screen_callback
        
        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month
        
        card = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(1200), dp(700)), spacing=dp(10), padding=dp(20))
        with card.canvas.before:
            Color(0.11, 0.14, 0.19, 1)
            card.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
        card.bind(pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos), size=lambda i, v: setattr(i.bg_rect, 'size', i.size))
        
        lbl_header = Label(text="Übersicht & Druck", font_size=sp(18), color=(0.95, 0.96, 0.98, 1), bold=True, size_hint_y=None, height=dp(30), halign='center', valign='middle')
        lbl_header.bind(size=lbl_header.setter('text_size'))
        card.add_widget(lbl_header)
        
        nav_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(36))
        
        self.btn_prev = Button(text="< Zurück", font_size=sp(12), bold=True, size_hint_x=0.25, background_normal='', background_color=(0.15, 0.18, 0.25, 1), color=(0.95, 0.96, 0.98, 1))
        self.btn_prev.bind(on_release=self.prev_month)
        
        self.lbl_month = Label(text="", font_size=sp(14), bold=True, color=(0.95, 0.96, 0.98, 1), size_hint_x=0.5, halign='center', valign='middle')
        self.lbl_month.bind(size=self.lbl_month.setter('text_size'))
        
        self.btn_next = Button(text="Vor >", font_size=sp(12), bold=True, size_hint_x=0.25, background_normal='', background_color=(0.15, 0.18, 0.25, 1), color=(0.95, 0.96, 0.98, 1))
        self.btn_next.bind(on_release=self.next_month)
        
        nav_layout.add_widget(self.btn_prev)
        nav_layout.add_widget(self.lbl_month)
        nav_layout.add_widget(self.btn_next)
        card.add_widget(nav_layout)
        
        preview_box = BoxLayout(orientation='vertical', size_hint=(1, 1), padding=dp(10))
        with preview_box.canvas.before:
            Color(1, 1, 1, 1)
            preview_box.bg_rect = RoundedRectangle(pos=preview_box.pos, size=preview_box.size, radius=[dp(4)])
            Color(0, 0, 0, 1)
            preview_box.border_line = Line(rounded_rectangle=(preview_box.x, preview_box.y, preview_box.width, preview_box.height, dp(4)), width=1.5)
        preview_box.bind(
            pos=lambda i, v: (
                setattr(i.bg_rect, 'pos', i.pos),
                setattr(i.border_line, 'rounded_rectangle', (i.x, i.y, i.width, i.height, dp(4)))
            ),
            size=lambda i, v: (
                setattr(i.bg_rect, 'size', i.size),
                setattr(i.border_line, 'rounded_rectangle', (i.x, i.y, i.width, i.height, dp(4)))
            )
        )
        
        self.preview_info = Label(text="", font_size=sp(12), color=(0, 0, 0, 1), bold=True, size_hint_y=None, height=dp(25), halign='left', valign='middle')
        self.preview_info.bind(size=self.preview_info.setter('text_size'))
        preview_box.add_widget(self.preview_info)
        
        headers_layout = GridLayout(cols=6, spacing=dp(0), size_hint_y=None, height=dp(24))
        headers = ["Datum", "Kommen", "Gehn", "Pause", "Bemerkung", "Stunden"]
        for h in headers:
            cell_box = AnchorLayout(anchor_x='center', anchor_y='center')
            with cell_box.canvas.before:
                Color(0, 0, 0, 1)
                cell_box.border_line = Line(rectangle=(cell_box.x, cell_box.y, cell_box.width, cell_box.height), width=1)
            cell_box.bind(
                pos=lambda i, v: setattr(i.border_line, 'rectangle', (i.x, i.y, i.width, i.height)),
                size=lambda i, v: setattr(i.border_line, 'rectangle', (i.x, i.y, i.width, i.height))
            )
            lbl = Label(text=h, font_size=sp(11), bold=True, color=(0, 0, 0, 1), halign='center', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            cell_box.add_widget(lbl)
            headers_layout.add_widget(cell_box)
        preview_box.add_widget(headers_layout)
        
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        self.print_content = GridLayout(cols=6, spacing=dp(0), size_hint_y=None)
        self.print_content.bind(minimum_height=self.print_content.setter('height'))
        scroll.add_widget(self.print_content)
        preview_box.add_widget(scroll)
        
        card.add_widget(preview_box)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=dp(13), size_hint_y=None, height=dp(36))
        
        btn_print = ModernButton(text="PDF / Drucken", is_primary=True)
        btn_print.bind(on_release=self.generate_pdf_and_print)
        
        btn_back = ModernButton(text="Hauptmenü", is_primary=False)
        btn_back.bind(on_release=lambda x: self.switch_screen_callback("menu"))
        
        btn_layout.add_widget(btn_print)
        btn_layout.add_widget(btn_back)
        
        card.add_widget(btn_layout)
        self.add_widget(card)
        
        self.load_overview_data()

    def update_month_label(self):
        months_german = ["", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        self.lbl_month.text = f"{months_german[self.current_month]} {self.current_year}"

    def load_overview_data(self):
        self.update_month_label()
        self.print_content.clear_widgets()
        
        data = load_data()
        settings = data.get("settings", {})
        entries = data.get("entries", {})
        
        name = settings.get("name", "Unbekannt")
        pers_nr = settings.get("personalnummer", "-")
        soll = settings.get("soll_stunden", "-")
        
        months_german = ["", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        self.preview_info.text = f"Monat: {months_german[self.current_month]} {self.current_year}  |  Name: {name}  |  Pers.-Nr.: {pers_nr}  |  Soll-Stunden: {soll}"
        
        if self.current_month == 12:
            next_m_date = datetime(self.current_year + 1, 1, 1)
        else:
            next_m_date = datetime(self.current_year, self.current_month + 1, 1)
        
        last_day = (next_m_date - timedelta(days=1)).day
        weekdays_german = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        
        for day in range(1, last_day + 1):
            current_date = datetime(self.current_year, self.current_month, day)
            date_str = current_date.strftime("%Y-%m-%d")
            wd_index = current_date.weekday()
            wd_text = weekdays_german[wd_index]
            
            day_data = entries.get(date_str, {"kommen": "", "gehn": "", "pause": "", "bemerkung": ""})
            
            text_color = (0.8, 0, 0, 1) if wd_index >= 5 else (0, 0, 0, 1)
            
            texts = [
                f"{wd_text}, {day:02d}/{self.current_month:02d}/{self.current_year}",
                str(day_data.get("kommen", "")),
                str(day_data.get("gehn", "")),
                str(day_data.get("pause", "")),
                str(day_data.get("bemerkung", "")),
                "0.0h"
            ]
            
            for idx, txt in enumerate(texts):
                cell_box = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=dp(22))
                with cell_box.canvas.before:
                    Color(0, 0, 0, 1)
                    cell_box.border_line = Line(rectangle=(cell_box.x, cell_box.y, cell_box.width, cell_box.height), width=1)
                cell_box.bind(
                    pos=lambda i, v: setattr(i.border_line, 'rectangle', (i.x, i.y, i.width, i.height)),
                    size=lambda i, v: setattr(i.border_line, 'rectangle', (i.x, i.y, i.width, i.height))
                )
                
                c = text_color if idx == 0 else (0, 0, 0, 1)
                lbl = Label(text=txt, font_size=sp(10), color=c, halign='center', valign='middle')
                lbl.bind(size=lbl.setter('text_size'))
                cell_box.add_widget(lbl)
                self.print_content.add_widget(cell_box)

    def prev_month(self, instance):
        new_m = self.current_month - 1
        new_y = self.current_year
        if new_m < 1:
            new_m = 12
            new_y -= 1
        self.current_month = new_m
        self.current_year = new_y
        self.load_overview_data()

    def next_month(self, instance):
        new_m = self.current_month + 1
        new_y = self.current_year
        if new_m > 12:
            new_m = 1
            new_y += 1
        self.current_month = new_m
        self.current_year = new_y
        self.load_overview_data()

    def generate_pdf_and_print(self, instance):
        months_german = ["", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        filename = f"Zeiterfassung_{months_german[self.current_month]}_{self.current_year}.html"
        
        data = load_data()
        settings = data.get("settings", {})
        entries = data.get("entries", {})
        
        name = settings.get("name", "")
        pers_nr = settings.get("personalnummer", "")
        arbeitsstaette = settings.get("arbeitsstaette", "")
        soll = settings.get("soll_stunden", "")
        
        if self.current_month == 12:
            next_m_date = datetime(self.current_year + 1, 1, 1)
        else:
            next_m_date = datetime(self.current_year, self.current_month + 1, 1)
        last_day = (next_m_date - timedelta(days=1)).day
        weekdays_german = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        
        rows_html = ""
        for day in range(1, last_day + 1):
            current_date = datetime(self.current_year, self.current_month, day)
            date_str = current_date.strftime("%Y-%m-%d")
            wd_index = current_date.weekday()
            wd_text = weekdays_german[wd_index]
            
            day_data = entries.get(date_str, {"kommen": "", "gehn": "", "pause": "", "bemerkung": ""})
            
            is_weekend = wd_index >= 5
            color_style = "color: red;" if is_weekend else ""
            
            rows_html += f"""
            <tr>
                <td style="text-align: center; {color_style}">{wd_text}, {day:02d}/{self.current_month:02d}/{self.current_year}</td>
                <td style="text-align: center;">{day_data.get("kommen", "")}</td>
                <td style="text-align: center;">{day_data.get("gehn", "")}</td>
                <td style="text-align: center;">{day_data.get("pause", "")}</td>
                <td style="text-align: center;">{day_data.get("bemerkung", "")}</td>
                <td style="text-align: center;">0.0h</td>
            </tr>
            """
            
        html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Zeiterfassung - {months_german[self.current_month]} {self.current_year}</title>
    <style>
        @page {{ size: A4 portrait; margin: 10mm; }}
        body {{ font-family: Arial, sans-serif; font-size: 11pt; color: #000; background: #fff; margin: 0; padding: 0; }}
        .container {{ width: 100%; max-width: 190mm; margin: auto; }}
        h2 {{ text-align: center; margin-bottom: 5px; font-size: 16pt; }}
        .info-box {{ display: flex; justify-content: space-between; margin-bottom: 15px; font-size: 10pt; border-bottom: 1px solid #000; padding-bottom: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
        th, td {{ border: 1px solid #000; padding: 4px 6px; font-size: 10pt; }}
        th {{ background-color: #f2f2f2; text-align: center; }}
    </style>
</head>
<body onload="window.print()">
    <div class="container">
        <h2>Zeiterfassung - Monat: {months_german[self.current_month]} {self.current_year}</h2>
        <div class="info-box">
            <span><strong>Name:</strong> {name}</span>
            <span><strong>Personalnummer:</strong> {pers_nr}</span>
            <span><strong>Arbeitsstätte:</strong> {arbeitsstaette}</span>
            <span><strong>Soll-Stunden:</strong> {soll}</span>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Datum</th>
                    <th>Kommen</th>
                    <th>Gehn</th>
                    <th>Pause</th>
                    <th>Bemerkung</th>
                    <th>Stunden</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            os.startfile(filename)
        except Exception as e:
            print(f"Fehler beim Öffnen: {e}")

class EmployerReportView(AnchorLayout):
    def __init__(self, switch_screen_callback, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.switch_screen_callback = switch_screen_callback
        
        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month
        self.show_remark = True
        
        card = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(1200), dp(700)), spacing=dp(10), padding=dp(20))
        with card.canvas.before:
            Color(0.11, 0.14, 0.19, 1)
            card.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
        card.bind(pos=lambda i, v: setattr(i.bg_rect, 'pos', i.pos), size=lambda i, v: setattr(i.bg_rect, 'size', i.size))
        
        lbl_header = Label(text="Arbeitgeber-Bericht & Druck", font_size=sp(18), color=(0.95, 0.96, 0.98, 1), bold=True, size_hint_y=None, height=dp(30), halign='center', valign='middle')
        lbl_header.bind(size=lbl_header.setter('text_size'))
        card.add_widget(lbl_header)
        
        top_bar = BoxLayout(orientation='horizontal', spacing=dp(15), size_hint_y=None, height=dp(36))
        
        self.btn_prev = Button(text="< Zurück", font_size=sp(12), bold=True, size_hint_x=0.2, background_normal='', background_color=(0.15, 0.18, 0.25, 1), color=(0.95, 0.96, 0.98, 1))
        self.btn_prev.bind(on_release=self.prev_month)
        
        self.lbl_month = Label(text="", font_size=sp(14), bold=True, color=(0.95, 0.96, 0.98, 1), size_hint_x=0.4, halign='center', valign='middle')
        self.lbl_month.bind(size=self.lbl_month.setter('text_size'))
        
        self.btn_next = Button(text="Vor >", font_size=sp(12), bold=True, size_hint_x=0.2, background_normal='', background_color=(0.15, 0.18, 0.25, 1), color=(0.95, 0.96, 0.98, 1))
        self.btn_next.bind(on_release=self.next_month)
        
        self.btn_toggle_remark = Button(text="Bemerkung: EIN", font_size=sp(12), bold=True, size_hint_x=0.2, background_normal='', background_color=(0.25, 0.41, 0.88, 1), color=(0.95, 0.96, 0.98, 1))
        self.btn_toggle_remark.bind(on_release=self.toggle_remark)
        
        top_bar.add_widget(self.btn_prev)
        top_bar.add_widget(self.lbl_month)
        top_bar.add_widget(self.btn_next)
        top_bar.add_widget(self.btn_toggle_remark)
        card.add_widget(top_bar)
        
        preview_box = BoxLayout(orientation='vertical', size_hint=(1, 1), padding=dp(10))
        with preview_box.canvas.before:
            Color(1, 1, 1, 1)
            preview_box.bg_rect = RoundedRectangle(pos=preview_box.pos, size=preview_box.size, radius=[dp(4)])
            Color(0, 0, 0, 1)
            preview_box.border_line = Line(rounded_rectangle=(preview_box.x, preview_box.y, preview_box.width, preview_box.height, dp(4)), width=1.5)
        preview_box.bind(
            pos=lambda i, v: (
                setattr(i.bg_rect, 'pos', i.pos),
                setattr(i.border_line, 'rounded_rectangle', (i.x, i.y, i.width, i.height, dp(4)))
            ),
            size=lambda i, v: (
                setattr(i.bg_rect, 'size', i.size),
                setattr(i.border_line, 'rounded_rectangle', (i.x, i.y, i.width, i.height, dp(4)))
            )
        )
        
        self.preview_info = Label(text="", font_size=sp(12), color=(0, 0, 0, 1), bold=True, size_hint_y=None, height=dp(25), halign='left', valign='middle')
        self.preview_info.bind(size=self.preview_info.setter('text_size'))
        preview_box.add_widget(self.preview_info)
        
        self.headers_layout = GridLayout(cols=6, spacing=dp(0), size_hint_y=None, height=dp(24))
        preview_box.add_widget(self.headers_layout)
        
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        self.print_content = GridLayout(cols=6, spacing=dp(0), size_hint_y=None)
        self.print_content.bind(minimum_height=self.print_content.setter('height'))
        scroll.add_widget(self.print_content)
        preview_box.add_widget(scroll)
        
        card.add_widget(preview_box)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=dp(13), size_hint_y=None, height=dp(36))
        
        btn_print = ModernButton(text="PDF / Drucken", is_primary=True)
        btn_print.bind(on_release=self.generate_pdf_and_print)
        
        btn_back = ModernButton(text="Hauptmenü", is_primary=False)
        btn_back.bind(on_release=lambda x: self.switch_screen_callback("menu"))
        
        btn_layout.add_widget(btn_print)
        btn_layout.add_widget(btn_back)
        
        card.add_widget(btn_layout)
        self.add_widget(card)
        
        self.load_report_data()

    def toggle_remark(self, instance):
        self.show_remark = not self.show_remark
        if self.show_remark:
            self.btn_toggle_remark.text = "Bemerkung: EIN"
            self.btn_toggle_remark.background_color = (0.25, 0.41, 0.88, 1)
        else:
            self.btn_toggle_remark.text = "Bemerkung: AUS"
            self.btn_toggle_remark.background_color = (0.15, 0.18, 0.25, 1)
        self.load_report_data()

    def update_month_label(self):
        months_german = ["", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        self.lbl_month.text = f"{months_german[self.current_month]} {self.current_year}"

    def load_report_data(self):
        self.update_month_label()
        self.headers_layout.clear_widgets()
        self.print_content.clear_widgets()
        
        if self.show_remark:
            headers = ["Datum", "Kommen", "Gehn", "Pause", "Bemerkung", "Stunden"]
            cols_count = 6
        else:
            headers = ["Datum", "Kommen", "Gehn", "Pause", "Stunden"]
            cols_count = 5
            
        self.headers_layout.cols = cols_count
        self.print_content.cols = cols_count
        
        for h in headers:
            cell_box = AnchorLayout(anchor_x='center', anchor_y='center')
            with cell_box.canvas.before:
                Color(0, 0, 0, 1)
                cell_box.border_line = Line(rectangle=(cell_box.x, cell_box.y, cell_box.width, cell_box.height), width=1)
            cell_box.bind(
                pos=lambda i, v: setattr(i.border_line, 'rectangle', (i.x, i.y, i.width, i.height)),
                size=lambda i, v: setattr(i.border_line, 'rectangle', (i.x, i.y, i.width, i.height))
            )
            lbl = Label(text=h, font_size=sp(11), bold=True, color=(0, 0, 0, 1), halign='center', valign='middle')
            lbl.bind(size=lbl.setter('text_size'))
            cell_box.add_widget(lbl)
            self.headers_layout.add_widget(cell_box)
            
        data = load_data()
        settings = data.get("settings", {})
        entries = data.get("entries", {})
        
        name = settings.get("name", "Unbekannt")
        pers_nr = settings.get("personalnummer", "-")
        soll = settings.get("soll_stunden", "-")
        
        months_german = ["", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        self.preview_info.text = f"Monat: {months_german[self.current_month]} {self.current_year}  |  Name: {name}  |  Pers.-Nr.: {pers_nr}  |  Soll-Stunden: {soll}"
        
        if self.current_month == 12:
            next_m_date = datetime(self.current_year + 1, 1, 1)
        else:
            next_m_date = datetime(self.current_year, self.current_month + 1, 1)
        
        last_day = (next_m_date - timedelta(days=1)).day
        weekdays_german = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        
        for day in range(1, last_day + 1):
            current_date = datetime(self.current_year, self.current_month, day)
            date_str = current_date.strftime("%Y-%m-%d")
            wd_index = current_date.weekday()
            wd_text = weekdays_german[wd_index]
            
            day_data = entries.get(date_str, {"kommen": "", "gehn": "", "pause": "", "bemerkung": ""})
            text_color = (0.8, 0, 0, 1) if wd_index >= 5 else (0, 0, 0, 1)
            
            if self.show_remark:
                texts = [
                    f"{wd_text}, {day:02d}/{self.current_month:02d}/{self.current_year}",
                    str(day_data.get("kommen", "")),
                    str(day_data.get("gehn", "")),
                    str(day_data.get("pause", "")),
                    str(day_data.get("bemerkung", "")),
                    "0.0h"
                ]
            else:
                texts = [
                    f"{wd_text}, {day:02d}/{self.current_month:02d}/{self.current_year}",
                    str(day_data.get("kommen", "")),
                    str(day_data.get("gehn", "")),
                    str(day_data.get("pause", "")),
                    "0.0h"
                ]
            
            for idx, txt in enumerate(texts):
                cell_box = AnchorLayout(anchor_x='center', anchor_y='center', size_hint_y=None, height=dp(22))
                with cell_box.canvas.before:
                    Color(0, 0, 0, 1)
                    cell_box.border_line = Line(rectangle=(cell_box.x, cell_box.y, cell_box.width, cell_box.height), width=1)
                cell_box.bind(
                    pos=lambda i, v: setattr(i.border_line, 'rectangle', (i.x, i.y, i.width, i.height)),
                    size=lambda i, v: setattr(i.border_line, 'rectangle', (i.x, i.y, i.width, i.height))
                )
                
                c = text_color if idx == 0 else (0, 0, 0, 1)
                lbl = Label(text=txt, font_size=sp(10), color=c, halign='center', valign='middle')
                lbl.bind(size=lbl.setter('text_size'))
                cell_box.add_widget(lbl)
                self.print_content.add_widget(cell_box)

    def prev_month(self, instance):
        new_m = self.current_month - 1
        new_y = self.current_year
        if new_m < 1:
            new_m = 12
            new_y -= 1
        self.current_month = new_m
        self.current_year = new_y
        self.load_report_data()

    def next_month(self, instance):
        new_m = self.current_month + 1
        new_y = self.current_year
        if new_m > 12:
            new_m = 1
            new_y += 1
        self.current_month = new_m
        self.current_year = new_y
        self.load_report_data()

    def generate_pdf_and_print(self, instance):
        months_german = ["", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        filename = f"Arbeitgeber_Bericht_{months_german[self.current_month]}_{self.current_year}.html"
        
        data = load_data()
        settings = data.get("settings", {})
        entries = data.get("entries", {})
        
        name = settings.get("name", "")
        pers_nr = settings.get("personalnummer", "")
        arbeitsstaette = settings.get("arbeitsstaette", "")
        soll = settings.get("soll_stunden", "")
        
        if self.current_month == 12:
            next_m_date = datetime(self.current_year + 1, 1, 1)
        else:
            next_m_date = datetime(self.current_year, self.current_month + 1, 1)
        last_day = (next_m_date - timedelta(days=1)).day
        weekdays_german = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        
        rows_html = ""
        for day in range(1, last_day + 1):
            current_date = datetime(self.current_year, self.current_month, day)
            date_str = current_date.strftime("%Y-%m-%d")
            wd_index = current_date.weekday()
            wd_text = weekdays_german[wd_index]
            
            day_data = entries.get(date_str, {"kommen": "", "gehn": "", "pause": "", "bemerkung": ""})
            is_weekend = wd_index >= 5
            color_style = "color: red;" if is_weekend else ""
            
            if self.show_remark:
                rows_html += f"""
                <tr>
                    <td style="text-align: center; {color_style}">{wd_text}, {day:02d}/{self.current_month:02d}/{self.current_year}</td>
                    <td style="text-align: center;">{day_data.get("kommen", "")}</td>
                    <td style="text-align: center;">{day_data.get("gehn", "")}</td>
                    <td style="text-align: center;">{day_data.get("pause", "")}</td>
                    <td style="text-align: center;">{day_data.get("bemerkung", "")}</td>
                    <td style="text-align: center;">0.0h</td>
                </tr>
                """
            else:
                rows_html += f"""
                <tr>
                    <td style="text-align: center; {color_style}">{wd_text}, {day:02d}/{self.current_month:02d}/{self.current_year}</td>
                    <td style="text-align: center;">{day_data.get("kommen", "")}</td>
                    <td style="text-align: center;">{day_data.get("gehn", "")}</td>
                    <td style="text-align: center;">{day_data.get("pause", "")}</td>
                    <td style="text-align: center;">0.0h</td>
                </tr>
                """
                
        if self.show_remark:
            th_remark = "<th>Bemerkung</th>"
        else:
            th_remark = ""
            
        html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Arbeitgeber-Bericht - {months_german[self.current_month]} {self.current_year}</title>
    <style>
        @page {{ size: A4 portrait; margin: 10mm; }}
        body {{ font-family: Arial, sans-serif; font-size: 11pt; color: #000; background: #fff; margin: 0; padding: 0; }}
        .container {{ width: 100%; max-width: 190mm; margin: auto; }}
        h2 {{ text-align: center; margin-bottom: 5px; font-size: 16pt; }}
        .info-box {{ display: flex; justify-content: space-between; margin-bottom: 15px; font-size: 10pt; border-bottom: 1px solid #000; padding-bottom: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 5px; }}
        th, td {{ border: 1px solid #000; padding: 4px 6px; font-size: 10pt; }}
        th {{ background-color: #f2f2f2; text-align: center; }}
    </style>
</head>
<body onload="window.print()">
    <div class="container">
        <h2>Arbeitgeber-Bericht - Monat: {months_german[self.current_month]} {self.current_year}</h2>
        <div class="info-box">
            <span><strong>Name:</strong> {name}</span>
            <span><strong>Personalnummer:</strong> {pers_nr}</span>
            <span><strong>Arbeitsstätte:</strong> {arbeitsstaette}</span>
            <span><strong>Soll-Stunden:</strong> {soll}</span>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Datum</th>
                    <th>Kommen</th>
                    <th>Gehn</th>
                    <th>Pause</th>
                    {th_remark}
                    <th>Stunden</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            os.startfile(filename)
        except Exception as e:
            print(f"Fehler beim Öffnen: {e}")

class RootManager(BoxLayout):
    def __init__(self, **kwargs):
        self.orientation = 'vertical'
        super().__init__(**kwargs)
        self.show_screen("menu")

    def show_screen(self, name):
        self.clear_widgets()
        if name == "menu":
            self.add_widget(MainNavigation(self.show_screen))
        elif name == "settings":
            self.add_widget(SettingsView(self.show_screen))
        elif name == "timesheet":
            self.add_widget(TimesheetView(self.show_screen))
        elif name == "overview":
            self.add_widget(OverviewView(self.show_screen))
        elif name == "report":
            self.add_widget(EmployerReportView(self.show_screen))

class KinderschubserApp(App):
    def build(self):
        Window.clearcolor = (0.06, 0.08, 0.11, 1)
        Window.size = (1280, 800)
        return RootManager()

if __name__ == '__main__':
    KinderschubserApp().run()
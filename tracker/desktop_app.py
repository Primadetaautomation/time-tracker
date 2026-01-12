#!/usr/bin/env python3
"""
Tijdregistratie Desktop App
Een moderne desktop applicatie voor het bijhouden van je werkuren.

Features:
- Real-time activity tracking
- Project management
- Handmatige invoer
- Dagelijkse/wekelijkse statistieken
- CSV export
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import csv
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import platform

# Import de enhanced tracker
from activity_tracker_enhanced import (
    EnhancedActivityTracker,
    get_active_window_info_enhanced,
    get_idle_time,
    ACTIVITY_LOG,
    DATA_DIR
)

# Thema instellen
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Data bestanden
PROJECTS_FILE = DATA_DIR / "projects.json"
MANUAL_ENTRIES_FILE = DATA_DIR / "manual_entries.json"


class TimeTrackerApp(ctk.CTk):
    """Hoofdapplicatie voor tijdregistratie."""

    def __init__(self):
        super().__init__()

        # Window setup
        self.title("⏱️ Tijdregistratie")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Data
        self.projects = self.load_projects()
        self.manual_entries = self.load_manual_entries()
        self.tracker = EnhancedActivityTracker()

        # Tracking state
        self.tracking_active = False
        self.tracking_thread = None
        self.current_activity = None
        self.session_start = None

        # Timer state
        self.timer_running = False
        self.timer_start = None
        self.timer_project = None

        # Hourly check state
        self.hourly_check_id = None
        self.check_interval_ms = 60 * 60 * 1000  # 1 uur in milliseconden

        # Build UI
        self.create_widgets()
        self.update_stats()

        # Start activity monitor (read-only, toont wat je doet)
        self.start_activity_monitor()

        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_projects(self):
        """Laad projecten."""
        if PROJECTS_FILE.exists():
            try:
                with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return [
            {"id": "1", "name": "Algemeen", "color": "#3498db", "rate": 0},
            {"id": "2", "name": "Klant A", "color": "#27ae60", "rate": 75},
            {"id": "3", "name": "Klant B", "color": "#e74c3c", "rate": 85},
        ]

    def save_projects(self):
        """Sla projecten op."""
        with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.projects, f, indent=2, ensure_ascii=False)

    def load_manual_entries(self):
        """Laad handmatige entries."""
        if MANUAL_ENTRIES_FILE.exists():
            try:
                with open(MANUAL_ENTRIES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save_manual_entries(self):
        """Sla handmatige entries op."""
        with open(MANUAL_ENTRIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.manual_entries, f, indent=2, ensure_ascii=False)

    def create_widgets(self):
        """Maak alle UI elementen."""
        # Main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.create_sidebar()

        # Main content
        self.create_main_content()

    def create_sidebar(self):
        """Maak de sidebar met navigatie en projecten."""
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(4, weight=1)

        # Logo/Title
        title = ctk.CTkLabel(
            sidebar,
            text="⏱️ Tijdregistratie",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Current activity display
        self.activity_frame = ctk.CTkFrame(sidebar)
        self.activity_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(
            self.activity_frame,
            text="Nu actief:",
            font=ctk.CTkFont(size=12)
        ).pack(padx=10, pady=(10, 0), anchor="w")

        self.current_app_label = ctk.CTkLabel(
            self.activity_frame,
            text="Wachten...",
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=200
        )
        self.current_app_label.pack(padx=10, pady=(5, 10), anchor="w")

        # Timer section
        timer_frame = ctk.CTkFrame(sidebar)
        timer_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkLabel(
            timer_frame,
            text="Timer",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(padx=10, pady=(10, 5))

        self.timer_display = ctk.CTkLabel(
            timer_frame,
            text="00:00:00",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.timer_display.pack(padx=10, pady=5)

        # Project dropdown voor timer
        self.timer_project_var = ctk.StringVar(value="Selecteer project...")
        self.timer_project_dropdown = ctk.CTkComboBox(
            timer_frame,
            values=[p["name"] for p in self.projects],
            variable=self.timer_project_var,
            width=200
        )
        self.timer_project_dropdown.pack(padx=10, pady=5)

        # Timer buttons
        timer_btn_frame = ctk.CTkFrame(timer_frame, fg_color="transparent")
        timer_btn_frame.pack(padx=10, pady=10)

        self.start_btn = ctk.CTkButton(
            timer_btn_frame,
            text="▶️ Start",
            command=self.start_timer,
            width=90,
            fg_color="#27ae60",
            hover_color="#2ecc71"
        )
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ctk.CTkButton(
            timer_btn_frame,
            text="⏹️ Stop",
            command=self.stop_timer,
            width=90,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)

        # Projects section
        projects_label = ctk.CTkLabel(
            sidebar,
            text="Projecten",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        projects_label.grid(row=3, column=0, padx=20, pady=(20, 5), sticky="w")

        # Projects list
        self.projects_frame = ctk.CTkScrollableFrame(sidebar, height=200)
        self.projects_frame.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
        self.update_projects_list()

        # Add project button
        add_project_btn = ctk.CTkButton(
            sidebar,
            text="+ Nieuw Project",
            command=self.add_project_dialog,
            fg_color="transparent",
            border_width=1
        )
        add_project_btn.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        # Auto tracking toggle
        self.auto_track_var = ctk.BooleanVar(value=False)
        auto_track_switch = ctk.CTkSwitch(
            sidebar,
            text="Auto-tracking",
            variable=self.auto_track_var,
            command=self.toggle_auto_tracking
        )
        auto_track_switch.grid(row=6, column=0, padx=20, pady=10, sticky="w")

        # Auto-pauze optie (vraagt elk uur of je nog bezig bent)
        self.auto_pause_var = ctk.BooleanVar(value=True)
        auto_pause_check = ctk.CTkCheckBox(
            sidebar,
            text="Uurlijkse check",
            variable=self.auto_pause_var,
            font=ctk.CTkFont(size=12)
        )
        auto_pause_check.grid(row=7, column=0, padx=30, pady=(0, 10), sticky="w")

        # Always on top optie
        self.always_on_top_var = ctk.BooleanVar(value=False)
        always_on_top_check = ctk.CTkCheckBox(
            sidebar,
            text="Altijd bovenop",
            variable=self.always_on_top_var,
            command=self.toggle_always_on_top,
            font=ctk.CTkFont(size=12)
        )
        always_on_top_check.grid(row=8, column=0, padx=20, pady=(5, 10), sticky="w")

    def toggle_always_on_top(self):
        """Toggle always on top mode."""
        self.attributes('-topmost', self.always_on_top_var.get())

    def create_main_content(self):
        """Maak het hoofdcontent gebied."""
        main = ctk.CTkFrame(self)
        main.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(2, weight=1)

        # Stats section
        self.create_stats_section(main)

        # Manual entry section
        self.create_manual_entry_section(main)

        # Entries table
        self.create_entries_section(main)

    def create_stats_section(self, parent):
        """Maak statistieken sectie."""
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Vandaag
        self.stat_today = self.create_stat_card(stats_frame, "Vandaag", "0.0 uur", 0)

        # Deze week
        self.stat_week = self.create_stat_card(stats_frame, "Deze Week", "0.0 uur", 1)

        # Deze maand
        self.stat_month = self.create_stat_card(stats_frame, "Deze Maand", "0.0 uur", 2)

        # Totaal bedrag
        self.stat_amount = self.create_stat_card(stats_frame, "Bedrag (maand)", "€0.00", 3)

    def create_stat_card(self, parent, title, value, column):
        """Maak een statistiek kaart."""
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=column, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(padx=15, pady=(15, 5))

        label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label.pack(padx=15, pady=(0, 15))

        return label

    def create_manual_entry_section(self, parent):
        """Maak handmatige invoer sectie."""
        entry_frame = ctk.CTkFrame(parent)
        entry_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        ctk.CTkLabel(
            entry_frame,
            text="Handmatige Invoer",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=5, padx=15, pady=(15, 10), sticky="w")

        # Project
        ctk.CTkLabel(entry_frame, text="Project:").grid(row=1, column=0, padx=(15, 5), pady=5)
        self.entry_project = ctk.CTkComboBox(
            entry_frame,
            values=[p["name"] for p in self.projects],
            width=150
        )
        self.entry_project.grid(row=1, column=1, padx=5, pady=5)

        # Datum
        ctk.CTkLabel(entry_frame, text="Datum:").grid(row=1, column=2, padx=(15, 5), pady=5)
        self.entry_date = ctk.CTkEntry(entry_frame, width=120, placeholder_text="YYYY-MM-DD")
        self.entry_date.grid(row=1, column=3, padx=5, pady=5)
        self.entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Uren
        ctk.CTkLabel(entry_frame, text="Uren:").grid(row=2, column=0, padx=(15, 5), pady=5)
        self.entry_hours = ctk.CTkEntry(entry_frame, width=80, placeholder_text="1.5")
        self.entry_hours.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Beschrijving
        ctk.CTkLabel(entry_frame, text="Beschrijving:").grid(row=2, column=2, padx=(15, 5), pady=5)
        self.entry_desc = ctk.CTkEntry(entry_frame, width=250, placeholder_text="Wat heb je gedaan?")
        self.entry_desc.grid(row=2, column=3, padx=5, pady=5)

        # Add button
        add_btn = ctk.CTkButton(
            entry_frame,
            text="Toevoegen",
            command=self.add_manual_entry,
            width=100
        )
        add_btn.grid(row=2, column=4, padx=15, pady=5)

    def create_entries_section(self, parent):
        """Maak entries tabel sectie."""
        entries_frame = ctk.CTkFrame(parent)
        entries_frame.grid(row=2, column=0, sticky="nsew")
        entries_frame.grid_columnconfigure(0, weight=1)
        entries_frame.grid_rowconfigure(1, weight=1)

        # Header met export knop
        header = ctk.CTkFrame(entries_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Geregistreerde Uren",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        export_btn = ctk.CTkButton(
            header,
            text="📥 Export CSV",
            command=self.export_csv,
            width=120
        )
        export_btn.grid(row=0, column=1, sticky="e")

        # Entries list
        self.entries_list = ctk.CTkScrollableFrame(entries_frame)
        self.entries_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.entries_list.grid_columnconfigure(0, weight=1)

        self.update_entries_list()

    def update_projects_list(self):
        """Update de projectenlijst in de sidebar."""
        for widget in self.projects_frame.winfo_children():
            widget.destroy()

        for project in self.projects:
            frame = ctk.CTkFrame(self.projects_frame)
            frame.pack(fill="x", pady=2)

            color_box = ctk.CTkLabel(
                frame,
                text="●",
                font=ctk.CTkFont(size=16),
                text_color=project["color"],
                width=20
            )
            color_box.pack(side="left", padx=(10, 5))

            name_label = ctk.CTkLabel(
                frame,
                text=project["name"],
                font=ctk.CTkFont(size=13)
            )
            name_label.pack(side="left", padx=5, fill="x", expand=True)

            if project.get("rate", 0) > 0:
                rate_label = ctk.CTkLabel(
                    frame,
                    text=f"€{project['rate']}/u",
                    font=ctk.CTkFont(size=11),
                    text_color="gray"
                )
                rate_label.pack(side="right", padx=10)

    def update_entries_list(self):
        """Update de entries lijst."""
        for widget in self.entries_list.winfo_children():
            widget.destroy()

        # Combineer auto-tracked en handmatige entries
        all_entries = []

        # Laad auto-tracked entries
        if ACTIVITY_LOG.exists():
            try:
                with open(ACTIVITY_LOG, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f, delimiter=';')
                    for row in reader:
                        all_entries.append({
                            'date': row['Datum'],
                            'hours': float(row.get('Duur (uren)', 0) or 0),
                            'project': row.get('Project', '') or 'Auto',
                            'description': f"{row['Applicatie']} - {row.get('Venstertitel', '')[:30]}",
                            'source': 'auto',
                            'category': row.get('Categorie', '')
                        })
            except Exception as e:
                print(f"Error loading auto entries: {e}")

        # Voeg handmatige entries toe
        for entry in self.manual_entries:
            all_entries.append({
                'date': entry['date'],
                'hours': float(entry['hours']),
                'project': entry['project'],
                'description': entry.get('description', ''),
                'source': 'manual'
            })

        # Sorteer op datum (nieuwste eerst)
        all_entries.sort(key=lambda x: x['date'], reverse=True)

        # Toon laatste 50 entries
        for entry in all_entries[:50]:
            self.create_entry_row(entry)

        if not all_entries:
            ctk.CTkLabel(
                self.entries_list,
                text="Nog geen uren geregistreerd",
                text_color="gray"
            ).pack(pady=20)

    def create_entry_row(self, entry):
        """Maak een entry rij."""
        row = ctk.CTkFrame(self.entries_list)
        row.pack(fill="x", pady=2)
        row.grid_columnconfigure(2, weight=1)

        # Datum
        date_label = ctk.CTkLabel(
            row,
            text=entry['date'],
            font=ctk.CTkFont(size=12),
            width=100
        )
        date_label.grid(row=0, column=0, padx=10, pady=8)

        # Uren
        hours_label = ctk.CTkLabel(
            row,
            text=f"{entry['hours']:.2f}u",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=60
        )
        hours_label.grid(row=0, column=1, padx=5, pady=8)

        # Project
        project_label = ctk.CTkLabel(
            row,
            text=entry['project'] or '-',
            font=ctk.CTkFont(size=12),
            width=100
        )
        project_label.grid(row=0, column=2, padx=5, pady=8, sticky="w")

        # Beschrijving
        desc_label = ctk.CTkLabel(
            row,
            text=entry.get('description', '')[:50] or '-',
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        desc_label.grid(row=0, column=3, padx=5, pady=8, sticky="w")

        # Source indicator
        source_text = "🤖" if entry.get('source') == 'auto' else "✍️"
        source_label = ctk.CTkLabel(
            row,
            text=source_text,
            font=ctk.CTkFont(size=12),
            width=30
        )
        source_label.grid(row=0, column=4, padx=10, pady=8)

    def update_stats(self):
        """Update statistieken."""
        today = datetime.now().strftime('%Y-%m-%d')
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')
        month_start = datetime.now().strftime('%Y-%m-01')

        hours_today = 0
        hours_week = 0
        hours_month = 0
        amount_month = 0

        # Tel handmatige entries
        for entry in self.manual_entries:
            entry_date = entry['date']
            hours = float(entry['hours'])

            if entry_date == today:
                hours_today += hours
            if entry_date >= week_start:
                hours_week += hours
            if entry_date >= month_start:
                hours_month += hours
                # Bereken bedrag
                project = next((p for p in self.projects if p['name'] == entry['project']), None)
                if project:
                    amount_month += hours * project.get('rate', 0)

        # Tel auto-tracked entries
        if ACTIVITY_LOG.exists():
            try:
                with open(ACTIVITY_LOG, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f, delimiter=';')
                    for row in reader:
                        entry_date = row['Datum']
                        hours = float(row.get('Duur (uren)', 0) or 0)

                        if entry_date == today:
                            hours_today += hours
                        if entry_date >= week_start:
                            hours_week += hours
                        if entry_date >= month_start:
                            hours_month += hours
            except:
                pass

        # Update labels
        self.stat_today.configure(text=f"{hours_today:.1f} uur")
        self.stat_week.configure(text=f"{hours_week:.1f} uur")
        self.stat_month.configure(text=f"{hours_month:.1f} uur")
        self.stat_amount.configure(text=f"€{amount_month:.2f}")

    def start_timer(self):
        """Start de timer."""
        project_name = self.timer_project_var.get()
        if project_name == "Selecteer project..." or not project_name:
            messagebox.showwarning("Waarschuwing", "Selecteer eerst een project!")
            return

        self.timer_running = True
        self.timer_start = datetime.now()
        self.timer_project = project_name

        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.timer_project_dropdown.configure(state="disabled")

        self.update_timer_display()

    def stop_timer(self):
        """Stop de timer en sla op."""
        if not self.timer_running:
            return

        self.timer_running = False
        duration = (datetime.now() - self.timer_start).total_seconds()
        hours = duration / 3600

        if hours >= 0.01:  # Minimaal ~30 seconden
            self.manual_entries.append({
                'id': str(int(time.time() * 1000)),
                'date': self.timer_start.strftime('%Y-%m-%d'),
                'hours': round(hours, 2),
                'project': self.timer_project,
                'description': f"Timer sessie",
                'start_time': self.timer_start.strftime('%H:%M:%S'),
                'end_time': datetime.now().strftime('%H:%M:%S')
            })
            self.save_manual_entries()
            self.update_entries_list()
            self.update_stats()

        self.timer_display.configure(text="00:00:00")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.timer_project_dropdown.configure(state="normal")

    def update_timer_display(self):
        """Update timer display."""
        if self.timer_running:
            elapsed = (datetime.now() - self.timer_start).total_seconds()
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.timer_display.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.after(1000, self.update_timer_display)

    def add_manual_entry(self):
        """Voeg handmatige entry toe."""
        try:
            project = self.entry_project.get()
            date = self.entry_date.get()
            hours = float(self.entry_hours.get())
            description = self.entry_desc.get()

            if not project or not date or hours <= 0:
                messagebox.showwarning("Waarschuwing", "Vul alle velden correct in!")
                return

            self.manual_entries.append({
                'id': str(int(time.time() * 1000)),
                'date': date,
                'hours': hours,
                'project': project,
                'description': description
            })
            self.save_manual_entries()

            # Reset form
            self.entry_hours.delete(0, 'end')
            self.entry_desc.delete(0, 'end')

            self.update_entries_list()
            self.update_stats()

            messagebox.showinfo("Succes", f"{hours} uur toegevoegd aan {project}")

        except ValueError:
            messagebox.showerror("Fout", "Voer een geldig aantal uren in (bijv. 1.5)")

    def add_project_dialog(self):
        """Open dialoog voor nieuw project."""
        dialog = ctk.CTkInputDialog(
            text="Naam van het nieuwe project:",
            title="Nieuw Project"
        )
        name = dialog.get_input()

        if name:
            new_id = str(max([int(p['id']) for p in self.projects], default=0) + 1)
            self.projects.append({
                'id': new_id,
                'name': name,
                'color': '#3498db',
                'rate': 0
            })
            self.save_projects()
            self.update_projects_list()

            # Update dropdowns
            project_names = [p["name"] for p in self.projects]
            self.timer_project_dropdown.configure(values=project_names)
            self.entry_project.configure(values=project_names)

    def export_csv(self):
        """Exporteer naar CSV."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"tijdregistratie_{datetime.now().strftime('%Y-%m-%d')}.csv"
        )

        if not filename:
            return

        try:
            # Verzamel alle entries (handmatig + auto-tracked)
            all_entries = []

            # Handmatige entries
            for entry in self.manual_entries:
                project = next((p for p in self.projects if p['name'] == entry['project']), None)
                rate = project.get('rate', 0) if project else 0
                amount = float(entry['hours']) * rate

                all_entries.append({
                    'date': entry['date'],
                    'project': entry['project'],
                    'hours': float(entry['hours']),
                    'description': entry.get('description', ''),
                    'rate': rate,
                    'amount': round(amount, 2),
                    'source': 'Handmatig'
                })

            # Auto-tracked entries
            if ACTIVITY_LOG.exists():
                with open(ACTIVITY_LOG, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f, delimiter=';')
                    for row in reader:
                        hours = float(row.get('Duur (uren)', 0) or 0)
                        project_name = row.get('Project', '') or 'Auto'

                        # Gebruik tarief/bedrag uit CSV als beschikbaar, anders lookup
                        if 'Tarief' in row and row['Tarief']:
                            rate = float(row['Tarief'])
                            amount = float(row.get('Bedrag', 0) or 0)
                        else:
                            project = next((p for p in self.projects if p['name'] == project_name), None)
                            rate = project.get('rate', 0) if project else 0
                            amount = round(hours * rate, 2)

                        all_entries.append({
                            'date': row['Datum'],
                            'project': project_name,
                            'hours': hours,
                            'description': f"{row['Applicatie']} - {row.get('Venstertitel', '')[:50]}",
                            'rate': rate,
                            'amount': amount,
                            'source': 'Auto'
                        })

            if not all_entries:
                messagebox.showwarning("Geen data", "Er zijn geen uren om te exporteren.")
                return

            # Sorteer op datum
            all_entries.sort(key=lambda x: x['date'])

            # Schrijf CSV
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(['Datum', 'Project', 'Uren', 'Beschrijving', 'Tarief', 'Bedrag', 'Bron'])

                for entry in all_entries:
                    writer.writerow([
                        entry['date'],
                        entry['project'],
                        entry['hours'],
                        entry['description'],
                        entry['rate'],
                        entry['amount'],
                        entry['source']
                    ])

            total_hours = sum(e['hours'] for e in all_entries)
            total_amount = sum(e['amount'] for e in all_entries)

            messagebox.showinfo(
                "Succes",
                f"Geëxporteerd naar:\n{filename}\n\n"
                f"Totaal: {total_hours:.2f} uur\n"
                f"Bedrag: €{total_amount:.2f}"
            )

        except Exception as e:
            messagebox.showerror("Fout", f"Export mislukt: {e}")

    def start_activity_monitor(self):
        """Start achtergrond activiteit monitor."""
        def monitor():
            while True:
                try:
                    info = get_active_window_info_enhanced()
                    app = info.get('app_name', 'Unknown')
                    title = info.get('window_title', '')[:40]
                    url = info.get('url', '')

                    if url:
                        display = f"{app}\n{url[:35]}..."
                    elif title:
                        display = f"{app}\n{title}"
                    else:
                        display = app

                    # Update label in main thread
                    self.after(0, lambda d=display: self.current_app_label.configure(text=d))

                except Exception as e:
                    pass

                time.sleep(2)

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

    def toggle_auto_tracking(self):
        """Toggle automatische tracking."""
        if self.auto_track_var.get():
            # Haal het geselecteerde project op
            project_name = self.timer_project_var.get()
            if project_name == "Selecteer project...":
                messagebox.showwarning(
                    "Geen project",
                    "Selecteer eerst een project voordat je auto-tracking start."
                )
                self.auto_track_var.set(False)
                return

            # Zoek het project en tarief
            project_rate = 0
            for p in self.projects:
                if p['name'] == project_name:
                    project_rate = p.get('rate', 0)
                    break

            self.tracking_active = True
            self.session_start = datetime.now()
            messagebox.showinfo(
                "Auto-tracking",
                f"Automatische tracking gestart!\n\n"
                f"Project: {project_name}\n"
                f"Tarief: €{project_rate}/uur\n\n"
                f"Alle activiteit wordt nu gelogd."
            )

            def track():
                # Maak tracker met geselecteerd project en tarief
                tracker = EnhancedActivityTracker(
                    project_name=project_name,
                    project_rate=project_rate
                )
                while self.tracking_active:
                    tracker.track_once()
                    time.sleep(5)

            self.tracking_thread = threading.Thread(target=track, daemon=True)
            self.tracking_thread.start()

            # Disable project selector tijdens tracking
            self.timer_project_dropdown.configure(state="disabled")

            # Start uurlijkse check als ingeschakeld
            if self.auto_pause_var.get():
                self.start_hourly_check()
        else:
            self.stop_hourly_check()
            self.tracking_active = False
            self.timer_project_dropdown.configure(state="normal")
            self.update_entries_list()
            self.update_stats()
            messagebox.showinfo("Auto-tracking", "Automatische tracking gestopt.")

    def start_hourly_check(self):
        """Start de uurlijkse check timer."""
        self.stop_hourly_check()  # Stop bestaande timer
        self.hourly_check_id = self.after(self.check_interval_ms, self.do_hourly_check)

    def stop_hourly_check(self):
        """Stop de uurlijkse check timer."""
        if self.hourly_check_id:
            self.after_cancel(self.hourly_check_id)
            self.hourly_check_id = None

    def do_hourly_check(self):
        """Voer de uurlijkse check uit - vraag of gebruiker nog bezig is."""
        if not self.tracking_active:
            return

        # Bereken hoelang er al gewerkt is
        if self.session_start:
            elapsed = datetime.now() - self.session_start
            hours = elapsed.total_seconds() / 3600
            elapsed_str = f"{int(hours)}u {int((hours % 1) * 60)}m"
        else:
            elapsed_str = "onbekend"

        # Toon dialoog
        response = messagebox.askyesno(
            "⏰ Nog aan het werk?",
            f"Je bent al {elapsed_str} aan het werk.\n\n"
            f"Ben je nog steeds bezig?\n\n"
            f"• Ja = Doorgaan met tracking\n"
            f"• Nee = Pauzeer tracking",
            icon='question'
        )

        if response:
            # Ja - doorgaan, plan volgende check
            if self.auto_pause_var.get() and self.tracking_active:
                self.hourly_check_id = self.after(self.check_interval_ms, self.do_hourly_check)
        else:
            # Nee - pauzeer tracking
            self.auto_track_var.set(False)
            self.toggle_auto_tracking()
            messagebox.showinfo(
                "Gepauzeerd",
                "Auto-tracking is gepauzeerd.\n\n"
                "Zet de schakelaar weer aan om door te gaan."
            )

    def on_close(self):
        """Handle window close."""
        if self.timer_running:
            if messagebox.askyesno("Timer actief", "De timer loopt nog. Wil je stoppen en de tijd opslaan?"):
                self.stop_timer()

        self.stop_hourly_check()
        self.tracking_active = False
        self.destroy()


def main():
    """Start de applicatie."""
    app = TimeTrackerApp()
    app.mainloop()


if __name__ == "__main__":
    main()

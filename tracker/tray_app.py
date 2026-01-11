#!/usr/bin/env python3
"""
System Tray Applicatie voor Tijdregistratie
Werkt op Windows en macOS

Makkelijk switchen tussen projecten vanuit de menubalk/systray.

Vereisten:
    pip install pystray pillow

macOS:
    pip install rumps  (alternatief, specifiek voor macOS)
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from datetime import datetime

# Data directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

PROJECTS_FILE = DATA_DIR / "projects.json"
TIMER_FILE = DATA_DIR / "timer_state.json"
ENTRIES_FILE = DATA_DIR / "entries.json"


class TimeTrackerTray:
    """System Tray applicatie voor tijdregistratie."""

    def __init__(self):
        self.projects = self.load_projects()
        self.entries = self.load_entries()
        self.current_project = None
        self.timer_start = None
        self.timer_running = False
        self.timer_thread = None

        # Herstel timer state als die actief was
        self.restore_timer_state()

    def load_projects(self):
        """Laad projecten uit bestand."""
        if PROJECTS_FILE.exists():
            try:
                with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        # Default projecten
        default = [
            {"id": "1", "name": "Project A", "color": "#3498db"},
            {"id": "2", "name": "Project B", "color": "#27ae60"},
            {"id": "3", "name": "Intern", "color": "#95a5a6"},
        ]
        self.save_projects(default)
        return default

    def save_projects(self, projects=None):
        """Sla projecten op."""
        if projects is None:
            projects = self.projects
        with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=2, ensure_ascii=False)

    def load_entries(self):
        """Laad time entries uit bestand."""
        if ENTRIES_FILE.exists():
            try:
                with open(ENTRIES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save_entries(self):
        """Sla entries op."""
        with open(ENTRIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, indent=2, ensure_ascii=False)

    def save_timer_state(self):
        """Sla huidige timer state op."""
        state = {
            "running": self.timer_running,
            "project_id": self.current_project["id"] if self.current_project else None,
            "start_time": self.timer_start.isoformat() if self.timer_start else None
        }
        with open(TIMER_FILE, 'w') as f:
            json.dump(state, f)

    def restore_timer_state(self):
        """Herstel timer state na herstart."""
        if TIMER_FILE.exists():
            try:
                with open(TIMER_FILE, 'r') as f:
                    state = json.load(f)

                if state.get("running") and state.get("project_id"):
                    # Vind project
                    for p in self.projects:
                        if p["id"] == state["project_id"]:
                            self.current_project = p
                            break

                    if self.current_project and state.get("start_time"):
                        self.timer_start = datetime.fromisoformat(state["start_time"])
                        self.timer_running = True
            except:
                pass

    def start_timer(self, project):
        """Start timer voor een project."""
        # Stop huidige timer als die loopt
        if self.timer_running:
            self.stop_timer()

        self.current_project = project
        self.timer_start = datetime.now()
        self.timer_running = True
        self.save_timer_state()

        print(f"Timer gestart voor: {project['name']}")

    def stop_timer(self):
        """Stop de timer en sla entry op."""
        if not self.timer_running or not self.current_project:
            return

        end_time = datetime.now()
        duration_seconds = (end_time - self.timer_start).total_seconds()
        hours = duration_seconds / 3600

        # Voeg entry toe
        entry = {
            "id": str(int(time.time() * 1000)),
            "project_id": self.current_project["id"],
            "project_name": self.current_project["name"],
            "date": self.timer_start.strftime("%Y-%m-%d"),
            "start_time": self.timer_start.strftime("%H:%M:%S"),
            "end_time": end_time.strftime("%H:%M:%S"),
            "hours": round(hours, 2),
            "description": ""
        }

        self.entries.append(entry)
        self.save_entries()

        print(f"Timer gestopt: {hours:.2f} uur geregistreerd voor {self.current_project['name']}")

        self.timer_running = False
        self.current_project = None
        self.timer_start = None
        self.save_timer_state()

    def get_timer_display(self):
        """Haal huidige timer waarde op als string."""
        if not self.timer_running or not self.timer_start:
            return "00:00:00"

        elapsed = (datetime.now() - self.timer_start).total_seconds()
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_today_hours(self):
        """Bereken totaal uren vandaag."""
        today = datetime.now().strftime("%Y-%m-%d")
        total = sum(e["hours"] for e in self.entries if e["date"] == today)

        # Tel lopende timer mee
        if self.timer_running and self.timer_start:
            if self.timer_start.strftime("%Y-%m-%d") == today:
                elapsed_hours = (datetime.now() - self.timer_start).total_seconds() / 3600
                total += elapsed_hours

        return total


def run_pystray():
    """Start de tray app met pystray (cross-platform)."""
    try:
        import pystray
        from PIL import Image, ImageDraw
    except ImportError:
        print("Installeer vereiste packages:")
        print("  pip install pystray pillow")
        sys.exit(1)

    tracker = TimeTrackerTray()

    def create_icon_image(color="#3498db"):
        """Maak een simpel icoon."""
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Teken een klok-achtig icoon
        margin = 4
        draw.ellipse([margin, margin, size-margin, size-margin],
                     fill=color, outline='white')

        # Wijzers
        center = size // 2
        draw.line([center, center, center, margin + 12], fill='white', width=3)
        draw.line([center, center, center + 12, center], fill='white', width=2)

        return image

    def on_start_project(project):
        """Callback voor project selectie."""
        def callback(icon, item):
            tracker.start_timer(project)
            update_menu(icon)
        return callback

    def on_stop_timer(icon, item):
        """Stop huidige timer."""
        tracker.stop_timer()
        update_menu(icon)

    def on_quit(icon, item):
        """Sluit applicatie."""
        if tracker.timer_running:
            tracker.stop_timer()
        icon.stop()

    def update_menu(icon):
        """Update het menu met huidige status."""
        menu_items = []

        # Status
        if tracker.timer_running:
            status = f"⏱️ {tracker.current_project['name']}: {tracker.get_timer_display()}"
            menu_items.append(pystray.MenuItem(status, None, enabled=False))
            menu_items.append(pystray.MenuItem("⏹️ Stop Timer", on_stop_timer))
            menu_items.append(pystray.Menu.SEPARATOR)

        # Vandaag totaal
        today_hours = tracker.get_today_hours()
        menu_items.append(pystray.MenuItem(f"Vandaag: {today_hours:.1f}u", None, enabled=False))
        menu_items.append(pystray.Menu.SEPARATOR)

        # Projecten
        menu_items.append(pystray.MenuItem("Start project:", None, enabled=False))
        for project in tracker.projects:
            prefix = "▶️ " if tracker.current_project and tracker.current_project["id"] == project["id"] else "  "
            menu_items.append(pystray.MenuItem(
                f"{prefix}{project['name']}",
                on_start_project(project)
            ))

        menu_items.append(pystray.Menu.SEPARATOR)
        menu_items.append(pystray.MenuItem("Afsluiten", on_quit))

        icon.menu = pystray.Menu(*menu_items)

    # Timer update thread
    def timer_update_loop(icon):
        """Update menu elke seconde als timer loopt."""
        while icon.visible:
            if tracker.timer_running:
                update_menu(icon)
            time.sleep(1)

    # Maak icoon
    icon_image = create_icon_image()
    icon = pystray.Icon(
        "TimeTracker",
        icon_image,
        "Tijdregistratie"
    )

    update_menu(icon)

    # Start timer update thread
    timer_thread = threading.Thread(target=timer_update_loop, args=(icon,), daemon=True)
    timer_thread.start()

    print("Tijdregistratie actief in system tray")
    print("Klik op het icoon om projecten te selecteren")

    icon.run()


def run_rumps():
    """Start de tray app met rumps (macOS specifiek, betere integratie)."""
    try:
        import rumps
    except ImportError:
        print("rumps niet gevonden, gebruik pystray fallback")
        run_pystray()
        return

    tracker = TimeTrackerTray()

    class TimeTrackerApp(rumps.App):
        def __init__(self):
            super().__init__("⏱️", quit_button=None)
            self.timer = rumps.Timer(self.update_display, 1)
            self.timer.start()
            self.build_menu()

        def build_menu(self):
            """Bouw het menu op."""
            menu_items = []

            # Status
            if tracker.timer_running:
                self.title = f"⏱️ {tracker.get_timer_display()}"
                menu_items.append(rumps.MenuItem(
                    f"📍 {tracker.current_project['name']}",
                    callback=None
                ))
                menu_items.append(rumps.MenuItem("⏹️ Stop Timer", callback=self.stop_timer))
                menu_items.append(rumps.separator)
            else:
                self.title = "⏱️"

            # Vandaag totaal
            today_hours = tracker.get_today_hours()
            menu_items.append(rumps.MenuItem(f"Vandaag: {today_hours:.1f}u", callback=None))
            menu_items.append(rumps.separator)

            # Projecten submenu
            projects_menu = rumps.MenuItem("Start project")
            for project in tracker.projects:
                item = rumps.MenuItem(project['name'], callback=self.start_project)
                item._project = project
                projects_menu.add(item)
            menu_items.append(projects_menu)

            menu_items.append(rumps.separator)
            menu_items.append(rumps.MenuItem("Afsluiten", callback=self.quit_app))

            self.menu.clear()
            for item in menu_items:
                self.menu.add(item)

        def start_project(self, sender):
            """Start timer voor geselecteerd project."""
            project = sender._project
            tracker.start_timer(project)
            self.build_menu()

        def stop_timer(self, sender):
            """Stop huidige timer."""
            tracker.stop_timer()
            self.build_menu()

        def update_display(self, timer):
            """Update display elke seconde."""
            if tracker.timer_running:
                self.title = f"⏱️ {tracker.get_timer_display()}"

        def quit_app(self, sender):
            """Sluit app af."""
            if tracker.timer_running:
                tracker.stop_timer()
            rumps.quit_application()

    TimeTrackerApp().run()


def main():
    """Hoofdfunctie - kies beste implementatie voor platform."""
    import platform

    system = platform.system()

    if system == "Darwin":
        # Probeer rumps eerst (betere macOS integratie)
        try:
            import rumps
            run_rumps()
        except ImportError:
            run_pystray()
    else:
        run_pystray()


if __name__ == "__main__":
    main()

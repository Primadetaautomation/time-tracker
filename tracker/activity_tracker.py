#!/usr/bin/env python3
"""
Activity Tracker voor Tijdregistratie
Werkt op Windows en macOS

Houdt automatisch bij:
- Actieve applicatie
- Actieve window titel
- Tijdstip en duur

Vereisten:
    pip install pynput psutil

macOS extra:
    - Geef Terminal/Python toegang in Systeemvoorkeuren > Privacy > Toegankelijkheid

Windows extra:
    pip install pywin32
"""

import os
import sys
import json
import time
import platform
from datetime import datetime, timedelta
from pathlib import Path
import csv

# Detecteer besturingssysteem
SYSTEM = platform.system()

# Data directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Activity log bestand
ACTIVITY_LOG = DATA_DIR / "activity_log.csv"
CONFIG_FILE = DATA_DIR / "config.json"


def get_active_window_info():
    """
    Haal informatie op over het actieve venster.
    Retourneert: (app_name, window_title)
    """
    try:
        if SYSTEM == "Darwin":  # macOS
            return get_active_window_macos()
        elif SYSTEM == "Windows":
            return get_active_window_windows()
        else:  # Linux
            return get_active_window_linux()
    except Exception as e:
        print(f"Error getting window info: {e}")
        return ("Unknown", "Unknown")


def get_active_window_macos():
    """Haal actieve window info op macOS."""
    try:
        from AppKit import NSWorkspace
        from Quartz import (
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID,
            kCGWindowOwnerName,
            kCGWindowName,
            kCGWindowLayer
        )

        # Huidige actieve applicatie
        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.frontmostApplication()
        app_name = active_app.localizedName() if active_app else "Unknown"

        # Window titel (meer complex op macOS)
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)

        for window in window_list:
            if window.get(kCGWindowOwnerName) == app_name:
                if window.get(kCGWindowLayer, 0) == 0:
                    title = window.get(kCGWindowName, "")
                    if title:
                        return (app_name, title)

        return (app_name, "")

    except ImportError:
        # Fallback met osascript
        import subprocess
        try:
            script = '''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
                set frontAppTitle to ""
                try
                    tell process frontApp
                        set frontAppTitle to name of window 1
                    end tell
                end try
                return frontApp & "|" & frontAppTitle
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script],
                                   capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                parts = result.stdout.strip().split("|", 1)
                return (parts[0], parts[1] if len(parts) > 1 else "")
        except:
            pass
        return ("Unknown", "Unknown")


def get_active_window_windows():
    """Haal actieve window info op Windows."""
    try:
        import win32gui
        import win32process
        import psutil

        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        try:
            process = psutil.Process(pid)
            app_name = process.name()
        except:
            app_name = "Unknown"

        window_title = win32gui.GetWindowText(hwnd)

        return (app_name, window_title)

    except ImportError:
        print("Installeer pywin32: pip install pywin32")
        return ("Unknown", "Unknown")


def get_active_window_linux():
    """Haal actieve window info op Linux."""
    try:
        import subprocess

        # Probeer met xdotool
        result = subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'],
                               capture_output=True, text=True, timeout=2)
        window_title = result.stdout.strip() if result.returncode == 0 else "Unknown"

        result = subprocess.run(['xdotool', 'getactivewindow', 'getwindowpid'],
                               capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            import psutil
            try:
                process = psutil.Process(int(result.stdout.strip()))
                app_name = process.name()
            except:
                app_name = "Unknown"
        else:
            app_name = "Unknown"

        return (app_name, window_title)

    except Exception as e:
        return ("Unknown", "Unknown")


class ActivityTracker:
    """Houdt activiteit bij en logt naar CSV."""

    def __init__(self):
        self.config = self.load_config()
        self.current_app = None
        self.current_title = None
        self.current_start = None
        self.running = False

    def load_config(self):
        """Laad configuratie."""
        default_config = {
            "interval_seconds": 5,
            "min_duration_seconds": 30,
            "rules": []  # [{"pattern": "klantnaam", "project": "Project X"}]
        }

        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return {**default_config, **json.load(f)}
            except:
                pass

        # Sla default config op
        self.save_config(default_config)
        return default_config

    def save_config(self, config=None):
        """Sla configuratie op."""
        if config is None:
            config = self.config
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

    def add_rule(self, pattern, project):
        """Voeg een automatische toewijzingsregel toe."""
        self.config["rules"].append({
            "pattern": pattern.lower(),
            "project": project
        })
        self.save_config()

    def match_project(self, app_name, window_title):
        """Match window info met een project op basis van regels."""
        search_text = f"{app_name} {window_title}".lower()

        for rule in self.config["rules"]:
            if rule["pattern"] in search_text:
                return rule["project"]

        return None

    def log_activity(self, app_name, window_title, start_time, end_time):
        """Log activiteit naar CSV bestand."""
        duration = (end_time - start_time).total_seconds()

        # Skip korte activiteiten
        if duration < self.config["min_duration_seconds"]:
            return

        project = self.match_project(app_name, window_title)

        # Voeg header toe als bestand niet bestaat
        write_header = not ACTIVITY_LOG.exists()

        with open(ACTIVITY_LOG, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            if write_header:
                writer.writerow(['Datum', 'Starttijd', 'Eindtijd', 'Duur (sec)',
                                'Applicatie', 'Venstertitel', 'Project'])

            writer.writerow([
                start_time.strftime('%Y-%m-%d'),
                start_time.strftime('%H:%M:%S'),
                end_time.strftime('%H:%M:%S'),
                int(duration),
                app_name,
                window_title[:200],  # Limiet op titel lengte
                project or ''
            ])

    def track_once(self):
        """Voer één tracking check uit."""
        app_name, window_title = get_active_window_info()
        now = datetime.now()

        # Check of activiteit is veranderd
        if app_name != self.current_app or window_title != self.current_title:
            # Log vorige activiteit als die bestond
            if self.current_app and self.current_start:
                self.log_activity(
                    self.current_app,
                    self.current_title or "",
                    self.current_start,
                    now
                )

            # Start nieuwe activiteit
            self.current_app = app_name
            self.current_title = window_title
            self.current_start = now

    def run(self):
        """Start de tracking loop."""
        self.running = True
        print(f"Activity Tracker gestart op {SYSTEM}")
        print(f"Logging naar: {ACTIVITY_LOG}")
        print(f"Interval: {self.config['interval_seconds']} seconden")
        print("Druk Ctrl+C om te stoppen\n")

        try:
            while self.running:
                self.track_once()
                time.sleep(self.config["interval_seconds"])
        except KeyboardInterrupt:
            # Log laatste activiteit
            if self.current_app and self.current_start:
                self.log_activity(
                    self.current_app,
                    self.current_title or "",
                    self.current_start,
                    datetime.now()
                )
            print("\nTracker gestopt.")

    def stop(self):
        """Stop de tracking loop."""
        self.running = False


def get_daily_summary(date=None):
    """Genereer samenvatting voor een specifieke dag."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    if not ACTIVITY_LOG.exists():
        print("Geen activity log gevonden.")
        return

    # Lees en filter log
    activities = {}
    total_seconds = 0

    with open(ACTIVITY_LOG, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['Datum'] == date:
                app = row['Applicatie']
                duration = int(row['Duur (sec)'])
                project = row.get('Project', '')

                key = project if project else app
                activities[key] = activities.get(key, 0) + duration
                total_seconds += duration

    # Print samenvatting
    print(f"\n=== Activiteit Samenvatting voor {date} ===\n")

    if not activities:
        print("Geen activiteiten gelogd.")
        return

    # Sorteer op duur
    sorted_activities = sorted(activities.items(), key=lambda x: x[1], reverse=True)

    for name, seconds in sorted_activities:
        hours = seconds / 3600
        percentage = (seconds / total_seconds) * 100 if total_seconds > 0 else 0
        print(f"{name:40} {hours:6.2f}u ({percentage:5.1f}%)")

    print(f"\n{'Totaal':40} {total_seconds/3600:6.2f}u")


def main():
    """Hoofdfunctie."""
    import argparse

    parser = argparse.ArgumentParser(description='Activity Tracker voor Tijdregistratie')
    subparsers = parser.add_subparsers(dest='command', help='Commando\'s')

    # Start command
    start_parser = subparsers.add_parser('start', help='Start tracking')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Toon dagelijkse samenvatting')
    summary_parser.add_argument('--date', '-d', help='Datum (YYYY-MM-DD)', default=None)

    # Add rule command
    rule_parser = subparsers.add_parser('add-rule', help='Voeg toewijzingsregel toe')
    rule_parser.add_argument('pattern', help='Tekst om te zoeken')
    rule_parser.add_argument('project', help='Project naam')

    # List rules command
    list_parser = subparsers.add_parser('list-rules', help='Toon alle regels')

    args = parser.parse_args()

    tracker = ActivityTracker()

    if args.command == 'start':
        tracker.run()
    elif args.command == 'summary':
        get_daily_summary(args.date)
    elif args.command == 'add-rule':
        tracker.add_rule(args.pattern, args.project)
        print(f"Regel toegevoegd: '{args.pattern}' -> '{args.project}'")
    elif args.command == 'list-rules':
        print("\nHuidige regels:")
        for rule in tracker.config["rules"]:
            print(f"  '{rule['pattern']}' -> '{rule['project']}'")
        if not tracker.config["rules"]:
            print("  (geen regels)")
    else:
        # Default: start tracking
        tracker.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Enhanced Activity Tracker voor Gedetailleerde Tijdregistratie
Werkt op macOS (Windows support beschikbaar)

Verbeterde tracking:
- Browser URL tracking (Chrome, Safari, Firefox, Edge)
- Email details (Mail.app subject, afzender)
- Idle detection
- Gedetailleerde CSV output

Vereisten:
    pip install pynput psutil

macOS extra:
    - Geef Terminal/Python toegang in Systeemvoorkeuren > Privacy > Toegankelijkheid
    - Voor browser URL: ook Automation toegang nodig
"""

import os
import sys
import json
import time
import platform
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import csv

# Detecteer besturingssysteem
SYSTEM = platform.system()

# Data directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Enhanced activity log bestand
ACTIVITY_LOG = DATA_DIR / "activity_log_detailed.csv"
CONFIG_FILE = DATA_DIR / "config.json"
IDLE_THRESHOLD = 300  # 5 minuten idle = pauze


def run_applescript(script):
    """Voer AppleScript uit en retourneer resultaat."""
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        pass
    return None


def get_active_window_info_enhanced():
    """
    Haal uitgebreide informatie op over het actieve venster.
    Retourneert: dict met app_name, window_title, url, email_details, etc.
    """
    info = {
        'app_name': 'Unknown',
        'window_title': '',
        'url': '',
        'email_subject': '',
        'email_from': '',
        'category': 'other'
    }

    if SYSTEM != "Darwin":
        # Fallback voor andere systemen
        basic_info = get_active_window_basic()
        info['app_name'] = basic_info[0]
        info['window_title'] = basic_info[1]
        return info

    try:
        # Basis info via AppleScript
        script = '''
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
            set frontAppTitle to ""
            try
                tell process frontApp
                    set frontAppTitle to name of window 1
                end tell
            end try
            return frontApp & "|||" & frontAppTitle
        end tell
        '''
        result = run_applescript(script)
        if result:
            parts = result.split("|||", 1)
            info['app_name'] = parts[0]
            info['window_title'] = parts[1] if len(parts) > 1 else ""

        # Browser-specifieke URL tracking
        app_lower = info['app_name'].lower()

        if 'chrome' in app_lower or 'google chrome' in app_lower:
            info['url'] = get_chrome_url()
            info['category'] = categorize_url(info['url'])

        elif 'safari' in app_lower:
            info['url'] = get_safari_url()
            info['category'] = categorize_url(info['url'])

        elif 'firefox' in app_lower:
            info['url'] = get_firefox_url()
            info['category'] = categorize_url(info['url'])

        elif 'edge' in app_lower or 'microsoft edge' in app_lower:
            info['url'] = get_edge_url()
            info['category'] = categorize_url(info['url'])

        elif 'mail' in app_lower:
            email_info = get_mail_details()
            info['email_subject'] = email_info.get('subject', '')
            info['email_from'] = email_info.get('from', '')
            info['category'] = 'email'

        elif 'outlook' in app_lower:
            info['category'] = 'email'

        elif any(x in app_lower for x in ['code', 'visual studio', 'cursor', 'sublime', 'atom', 'vim', 'pycharm', 'intellij', 'xcode']):
            info['category'] = 'development'

        elif any(x in app_lower for x in ['slack', 'teams', 'zoom', 'discord', 'whatsapp', 'telegram', 'messages']):
            info['category'] = 'communication'

        elif any(x in app_lower for x in ['word', 'excel', 'powerpoint', 'pages', 'numbers', 'keynote', 'google docs', 'google sheets']):
            info['category'] = 'documents'

        elif any(x in app_lower for x in ['finder', 'explorer', 'terminal', 'iterm']):
            info['category'] = 'system'

    except Exception as e:
        print(f"Error getting enhanced window info: {e}")

    return info


def get_chrome_url():
    """Haal actieve URL op uit Google Chrome."""
    script = '''
    tell application "Google Chrome"
        if (count of windows) > 0 then
            return URL of active tab of front window
        end if
    end tell
    '''
    return run_applescript(script) or ""


def get_safari_url():
    """Haal actieve URL op uit Safari."""
    script = '''
    tell application "Safari"
        if (count of windows) > 0 then
            return URL of current tab of front window
        end if
    end tell
    '''
    return run_applescript(script) or ""


def get_firefox_url():
    """Haal actieve URL op uit Firefox (via window titel, Firefox blokkeert AppleScript)."""
    # Firefox beveiligt URL access, we gebruiken window titel
    return ""


def get_edge_url():
    """Haal actieve URL op uit Microsoft Edge."""
    script = '''
    tell application "Microsoft Edge"
        if (count of windows) > 0 then
            return URL of active tab of front window
        end if
    end tell
    '''
    return run_applescript(script) or ""


def get_mail_details():
    """Haal details op uit Apple Mail."""
    details = {'subject': '', 'from': ''}

    script = '''
    tell application "Mail"
        try
            set theMessages to selection
            if (count of theMessages) > 0 then
                set theMessage to item 1 of theMessages
                set theSubject to subject of theMessage
                set theSender to sender of theMessage
                return theSubject & "|||" & theSender
            end if
        end try
    end tell
    '''
    result = run_applescript(script)
    if result:
        parts = result.split("|||", 1)
        details['subject'] = parts[0] if parts else ""
        details['from'] = parts[1] if len(parts) > 1 else ""

    return details


def categorize_url(url):
    """Categoriseer een URL naar type activiteit."""
    if not url:
        return 'browsing'

    url_lower = url.lower()

    # Email services
    if any(x in url_lower for x in ['mail.google.com', 'outlook.live.com', 'outlook.office', 'mail.yahoo', 'protonmail']):
        return 'email'

    # Social media
    if any(x in url_lower for x in ['linkedin.com', 'facebook.com', 'twitter.com', 'x.com', 'instagram.com']):
        return 'social_media'

    # Development
    if any(x in url_lower for x in ['github.com', 'gitlab.com', 'stackoverflow.com', 'docs.', 'developer.']):
        return 'development'

    # Video/Entertainment
    if any(x in url_lower for x in ['youtube.com', 'netflix.com', 'spotify.com', 'twitch.tv']):
        return 'entertainment'

    # Nieuws
    if any(x in url_lower for x in ['news.', 'nos.nl', 'nu.nl', 'reddit.com', 'hackernews']):
        return 'news'

    # Meetings
    if any(x in url_lower for x in ['zoom.us', 'teams.microsoft.com', 'meet.google.com']):
        return 'meeting'

    # CRM/Business tools
    if any(x in url_lower for x in ['salesforce.com', 'hubspot.com', 'pipedrive.com', 'notion.so', 'asana.com', 'trello.com', 'monday.com']):
        return 'business_tools'

    return 'browsing'


def get_active_window_basic():
    """Fallback basis window info."""
    try:
        from AppKit import NSWorkspace
        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.frontmostApplication()
        app_name = active_app.localizedName() if active_app else "Unknown"
        return (app_name, "")
    except:
        return ("Unknown", "")


def get_idle_time():
    """Haal idle tijd op in seconden (macOS)."""
    if SYSTEM != "Darwin":
        return 0

    try:
        # Gebruik ioreg om idle tijd te krijgen
        result = subprocess.run(
            ['ioreg', '-c', 'IOHIDSystem'],
            capture_output=True,
            text=True,
            timeout=2
        )
        for line in result.stdout.split('\n'):
            if 'HIDIdleTime' in line:
                # Waarde is in nanoseconden
                idle_ns = int(line.split('=')[-1].strip())
                return idle_ns / 1_000_000_000
    except:
        pass
    return 0


class EnhancedActivityTracker:
    """Verbeterde activity tracker met gedetailleerde logging."""

    def __init__(self):
        self.config = self.load_config()
        self.current_activity = None
        self.current_start = None
        self.running = False
        self.last_active_time = datetime.now()
        self.is_idle = False

    def load_config(self):
        """Laad configuratie."""
        default_config = {
            "interval_seconds": 5,
            "min_duration_seconds": 30,
            "idle_threshold_seconds": 300,
            "track_urls": True,
            "track_email_details": True,
            "rules": []  # [{"pattern": "klantnaam", "project": "Project X"}]
        }

        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return {**default_config, **json.load(f)}
            except:
                pass

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

    def match_project(self, activity):
        """Match activiteit met een project op basis van regels."""
        search_text = " ".join([
            activity.get('app_name', ''),
            activity.get('window_title', ''),
            activity.get('url', ''),
            activity.get('email_subject', ''),
            activity.get('email_from', '')
        ]).lower()

        for rule in self.config["rules"]:
            if rule["pattern"] in search_text:
                return rule["project"]

        return None

    def activity_changed(self, new_activity):
        """Check of de activiteit significant is veranderd."""
        if self.current_activity is None:
            return True

        # Vergelijk de belangrijkste velden
        for key in ['app_name', 'window_title', 'url']:
            if self.current_activity.get(key) != new_activity.get(key):
                return True

        return False

    def log_activity(self, activity, start_time, end_time):
        """Log activiteit naar CSV bestand."""
        duration = (end_time - start_time).total_seconds()

        # Skip korte activiteiten
        if duration < self.config["min_duration_seconds"]:
            return

        project = self.match_project(activity)

        # Voeg header toe als bestand niet bestaat
        write_header = not ACTIVITY_LOG.exists()

        with open(ACTIVITY_LOG, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            if write_header:
                writer.writerow([
                    'Datum', 'Starttijd', 'Eindtijd', 'Duur (sec)', 'Duur (uren)',
                    'Applicatie', 'Venstertitel', 'URL', 'Categorie',
                    'Email Subject', 'Email Van', 'Project', 'Was Idle'
                ])

            hours = round(duration / 3600, 2)

            writer.writerow([
                start_time.strftime('%Y-%m-%d'),
                start_time.strftime('%H:%M:%S'),
                end_time.strftime('%H:%M:%S'),
                int(duration),
                hours,
                activity.get('app_name', ''),
                activity.get('window_title', '')[:200],
                activity.get('url', '')[:500],
                activity.get('category', ''),
                activity.get('email_subject', '')[:200],
                activity.get('email_from', '')[:100],
                project or '',
                'Ja' if self.is_idle else 'Nee'
            ])

    def track_once(self):
        """Voer één tracking check uit."""
        # Check idle status
        idle_seconds = get_idle_time()
        now = datetime.now()

        if idle_seconds > self.config.get("idle_threshold_seconds", 300):
            if not self.is_idle:
                # Net idle geworden - log huidige activiteit
                if self.current_activity and self.current_start:
                    self.log_activity(
                        self.current_activity,
                        self.current_start,
                        now
                    )
                self.is_idle = True
                self.current_activity = None
                self.current_start = None
                print(f"[{now.strftime('%H:%M:%S')}] Idle gedetecteerd")
            return

        # Niet meer idle
        if self.is_idle:
            self.is_idle = False
            self.last_active_time = now
            print(f"[{now.strftime('%H:%M:%S')}] Actief")

        # Haal nieuwe activiteit op
        new_activity = get_active_window_info_enhanced()

        # Check of activiteit is veranderd
        if self.activity_changed(new_activity):
            # Log vorige activiteit als die bestond
            if self.current_activity and self.current_start:
                self.log_activity(
                    self.current_activity,
                    self.current_start,
                    now
                )

            # Start nieuwe activiteit
            self.current_activity = new_activity
            self.current_start = now

            # Print status
            app = new_activity.get('app_name', 'Unknown')
            title = new_activity.get('window_title', '')[:50]
            url = new_activity.get('url', '')

            if url:
                print(f"[{now.strftime('%H:%M:%S')}] {app} - {url[:60]}")
            else:
                print(f"[{now.strftime('%H:%M:%S')}] {app} - {title}")

    def run(self):
        """Start de tracking loop."""
        self.running = True
        print("=" * 60)
        print("Enhanced Activity Tracker Gestart")
        print("=" * 60)
        print(f"Platform: {SYSTEM}")
        print(f"Logging naar: {ACTIVITY_LOG}")
        print(f"Interval: {self.config['interval_seconds']} seconden")
        print(f"Idle threshold: {self.config.get('idle_threshold_seconds', 300)} seconden")
        print(f"URL tracking: {'Aan' if self.config.get('track_urls', True) else 'Uit'}")
        print("=" * 60)
        print("Druk Ctrl+C om te stoppen\n")

        try:
            while self.running:
                self.track_once()
                time.sleep(self.config["interval_seconds"])
        except KeyboardInterrupt:
            # Log laatste activiteit
            if self.current_activity and self.current_start:
                self.log_activity(
                    self.current_activity,
                    self.current_start,
                    datetime.now()
                )
            print("\n" + "=" * 60)
            print("Tracker gestopt.")
            print(f"Data opgeslagen in: {ACTIVITY_LOG}")
            print("=" * 60)

    def stop(self):
        """Stop de tracking loop."""
        self.running = False


def get_daily_summary(date=None):
    """Genereer uitgebreide samenvatting voor een specifieke dag."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    if not ACTIVITY_LOG.exists():
        print("Geen activity log gevonden.")
        return

    # Lees en filter log
    by_project = {}
    by_category = {}
    by_app = {}
    total_seconds = 0

    with open(ACTIVITY_LOG, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['Datum'] == date:
                duration = int(row['Duur (sec)'])
                project = row.get('Project', '') or 'Geen project'
                category = row.get('Categorie', '') or 'Overig'
                app = row['Applicatie']

                by_project[project] = by_project.get(project, 0) + duration
                by_category[category] = by_category.get(category, 0) + duration
                by_app[app] = by_app.get(app, 0) + duration
                total_seconds += duration

    # Print samenvatting
    print(f"\n{'=' * 60}")
    print(f"ACTIVITEIT SAMENVATTING - {date}")
    print(f"{'=' * 60}\n")

    if not by_app:
        print("Geen activiteiten gelogd.")
        return

    # Per project
    print("PER PROJECT:")
    print("-" * 40)
    for name, seconds in sorted(by_project.items(), key=lambda x: x[1], reverse=True):
        hours = seconds / 3600
        percentage = (seconds / total_seconds) * 100
        print(f"  {name:30} {hours:6.2f}u ({percentage:5.1f}%)")

    # Per categorie
    print("\nPER CATEGORIE:")
    print("-" * 40)
    for name, seconds in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        hours = seconds / 3600
        percentage = (seconds / total_seconds) * 100
        print(f"  {name:30} {hours:6.2f}u ({percentage:5.1f}%)")

    # Per applicatie (top 10)
    print("\nTOP 10 APPLICATIES:")
    print("-" * 40)
    sorted_apps = sorted(by_app.items(), key=lambda x: x[1], reverse=True)[:10]
    for name, seconds in sorted_apps:
        hours = seconds / 3600
        percentage = (seconds / total_seconds) * 100
        print(f"  {name:30} {hours:6.2f}u ({percentage:5.1f}%)")

    print(f"\n{'=' * 60}")
    print(f"TOTAAL: {total_seconds/3600:.2f} uur")
    print(f"{'=' * 60}\n")


def main():
    """Hoofdfunctie."""
    import argparse

    parser = argparse.ArgumentParser(description='Enhanced Activity Tracker')
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

    tracker = EnhancedActivityTracker()

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

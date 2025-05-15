import ui
import requests
from bs4 import BeautifulSoup
import threading
import time
import re

REFRESH_INTERVAL = 300  # seconds (5 minutes)

class NHSMonitorApp:
    def __init__(self):
        self.refresh_timer = None

        # Create main view with fixed larger size
        self.main_view = ui.View(frame=(0, 0, 800, 600))
        self.main_view.name = "🩺 NHS A&E & UTC Waiting Times"
        self.main_view.background_color = '#f7f9fc'

        # Create title label
        self.title_label = ui.Label()
        self.title_label.text = "NHS North Cumbria Waiting Times"
        self.title_label.font = ('Helvetica-Bold', 18)
        self.title_label.text_color = '#222'
        self.main_view.add_subview(self.title_label)

        # Create countdown label
        self.countdown_label = ui.Label()
        self.countdown_label.font = ('Helvetica', 11)
        self.countdown_label.text_color = '#666'
        self.main_view.add_subview(self.countdown_label)

        # Create text views for A&E and UTC
        self.left_text = ui.TextView()
        self.left_text.font = ('Helvetica', 12)
        self.left_text.background_color = 'white'
        self.left_text.text_color = '#222222'
        self.left_text.editable = False
        self.main_view.add_subview(self.left_text)

        self.right_text = ui.TextView()
        self.right_text.font = ('Helvetica', 12)
        self.right_text.background_color = 'white'
        self.right_text.text_color = '#222222'
        self.right_text.editable = False
        self.main_view.add_subview(self.right_text)

        # Responsive layout
        def layout(sender):
            w, h = sender.width, sender.height
            self.title_label.frame = (20, 20, w - 40, 40)
            self.countdown_label.frame = (20, 70, w - 40, 30)
            self.left_text.frame = (20, 110, w / 2 - 30, h - 150)
            self.right_text.frame = (w / 2 + 10, 110, w / 2 - 30, h - 150)

        self.main_view.layout = layout
        layout(self.main_view)  # Force layout immediately so UI fills the window

        # Start the app
        self.refresh_data()
        self.start_auto_refresh()

    def simplify_name(self, full_name):
        name = re.sub(r"(,.*)?\s*24hrs", "", full_name, flags=re.IGNORECASE).strip()

        if "Penrith Community Hospital" in name:
            name = "Penrith Community Hospital"
        elif "Keswick Community Hospital" in name:
            name = "Keswick Community Hospital"

        return name

    def fetch_data(self):
        url = "https://www.ncic.nhs.uk/waiting/ncic-live-emergencytimes.html"
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            tables = soup.find_all("tbody")
            if not tables or len(tables) < 2:
                return None, "⚠️ Could not find A&E and UTC tables on the page."

            results = {"A&E Departments": [], "Urgent Treatment Centres": []}
            labels = list(results.keys())

            for idx, table in enumerate(tables[:2]):
                rows = table.find_all("tr")

                for i, row in enumerate(rows):
                    cols = row.find_all("td")
                    if len(cols) < 4:
                        continue

                    department = cols[0].get_text(separator=" ", strip=True)
                    simplified_name = self.simplify_name(department)

                    patients = cols[1].get_text(strip=True)
                    wait_time = cols[2].get_text(strip=True)
                    arrivals = cols[3].get_text(strip=True)

                    entry_lines = []

                    # Add blank lines for spacing
                    if simplified_name == "West Cumberland Hospital":
                        entry_lines.append("\n")
                    if simplified_name == "Keswick Community Hospital":
                        entry_lines.append("\n")

                    # Prepare hospital name line (with icon)
                    hospital_line = f"🏥 {simplified_name}"
                    entry_lines.append(hospital_line)
                    entry_lines.append(f"   • Patients in department: {patients}")
                    entry_lines.append(f"   • Average wait: {wait_time}")
                    entry_lines.append(f"   • Arrivals last hour: {arrivals}")

                    results[labels[idx]].append((entry_lines, simplified_name))

            return results, None

        except Exception as e:
            return None, f"❌ Error fetching data: {e}"

    def refresh_data(self):
        for text_widget in [self.left_text, self.right_text]:
            text_widget.text = "🔄 Fetching latest data...\n\n"

        results, error = self.fetch_data()

        if error:
            self.left_text.text = error
            self.right_text.text = error
        else:
            # Insert A&E Departments
            self.left_text.text = "A&E Departments\n\n"
            for entry, hosp_name in results["A&E Departments"]:
                for line in entry:
                    self.left_text.text += line + "\n"
                self.left_text.text += "\n"

            # Insert UTC
            self.right_text.text = "Urgent Treatment Centres\n\n"
            for entry, hosp_name in results["Urgent Treatment Centres"]:
                for line in entry:
                    self.right_text.text += line + "\n"
                self.right_text.text += "\n"

    def countdown_and_refresh(self):
        for remaining in range(REFRESH_INTERVAL, 0, -1):
            mins, secs = divmod(remaining, 60)
            self.countdown_label.text = f"⏳ Next refresh in: {mins:02d}:{secs:02d}"
            time.sleep(1)
        self.refresh_data()
        self.start_auto_refresh()

    def start_auto_refresh(self):
        if self.refresh_timer:
            self.refresh_timer.cancel()
        self.refresh_timer = threading.Timer(REFRESH_INTERVAL, self.countdown_and_refresh)
        self.refresh_timer.start()

# Start the app with larger window
app = NHSMonitorApp()
app.main_view.present('sheet')
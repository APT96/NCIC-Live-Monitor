import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import threading
import time
import re

REFRESH_INTERVAL = 300  # seconds (5 minutes)

class NHSMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🩺 NHS A&E & UTC Waiting Times")
        self.root.geometry("1000x600")  # larger window
        self.root.configure(bg="#f7f9fc")

        self.title_label = tk.Label(root, text="NHS North Cumbria Waiting Times",
                                    font=("Segoe UI", 18, "bold"),
                                    bg="#f7f9fc",
                                    fg="#222")
        self.title_label.pack(pady=(15, 10))

        self.countdown_label = tk.Label(root, text="", font=("Segoe UI", 11),
                                        bg="#f7f9fc", fg="#666")
        self.countdown_label.pack()

        self.paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned.pack(expand=True, fill="both", padx=20, pady=15)

        self.left_frame = ttk.Frame(self.paned, padding=10)
        self.paned.add(self.left_frame, weight=1)

        self.right_frame = ttk.Frame(self.paned, padding=10)
        self.paned.add(self.right_frame, weight=1)

        self.left_text = tk.Text(self.left_frame, wrap=tk.WORD,
                                 font=("Segoe UI", 12),
                                 bg="#ffffff", fg="#222222",
                                 relief="solid", borderwidth=1,
                                 spacing3=6, cursor="arrow")
        self.left_scroll = ttk.Scrollbar(self.left_frame, orient=tk.VERTICAL, command=self.left_text.yview)
        self.left_text.configure(yscrollcommand=self.left_scroll.set)
        self.left_text.pack(side=tk.LEFT, expand=True, fill="both")
        self.left_scroll.pack(side=tk.RIGHT, fill="y")

        self.right_text = tk.Text(self.right_frame, wrap=tk.WORD,
                                  font=("Segoe UI", 12),
                                  bg="#ffffff", fg="#222222",
                                  relief="solid", borderwidth=1,
                                  spacing3=6, cursor="arrow")
        self.right_scroll = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.right_text.yview)
        self.right_text.configure(yscrollcommand=self.right_scroll.set)
        self.right_text.pack(side=tk.LEFT, expand=True, fill="both")
        self.right_scroll.pack(side=tk.RIGHT, fill="y")

        # Define tags
        for text_widget in (self.left_text, self.right_text):
            text_widget.tag_configure("header", font=("Segoe UI", 14, "bold"), foreground="#004080", spacing3=10)
            text_widget.tag_configure("normal", font=("Segoe UI", 12), spacing3=6)
            # New tag for bold + underline hospital names
            text_widget.tag_configure("highlighted_hospital", font=("Segoe UI", 12, "bold", "underline"), spacing3=6)
            text_widget.config(state="disabled")

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

                    # Control separator line
                    # Remove separator line after Penrith Community Hospital in UTC
                    if simplified_name not in ["Cumberland Infirmary", "West Cumberland Hospital",
                                               "Penrith Community Hospital", "Keswick Community Hospital"]:
                        # Also avoid line after last row
                        if i < len(rows) - 1:
                            entry_lines.append("-" * 60)

                    results[labels[idx]].append((entry_lines, simplified_name))

            return results, None

        except Exception as e:
            return None, f"❌ Error fetching data: {e}"

    def refresh_data(self):
        for text_widget in (self.left_text, self.right_text):
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, "🔄 Fetching latest data...\n\n")
            text_widget.config(state="disabled")

        results, error = self.fetch_data()

        for text_widget in (self.left_text, self.right_text):
            text_widget.config(state="normal")
            text_widget.delete("1.0", tk.END)

        if error:
            self.left_text.insert(tk.END, error)
            self.right_text.insert(tk.END, error)
        else:
            # Insert A&E Departments
            self.left_text.insert(tk.END, "A&E Departments\n\n", "header")
            for entry, hosp_name in results["A&E Departments"]:
                for line in entry:
                    # Highlight hospital names
                    if line.startswith("🏥 "):
                        # Highlight those 4 hospitals
                        if hosp_name in ["Cumberland Infirmary", "West Cumberland Hospital",
                                         "Penrith Community Hospital", "Keswick Community Hospital"]:
                            self.left_text.insert(tk.END, line + "\n", "highlighted_hospital")
                        else:
                            self.left_text.insert(tk.END, line + "\n", "normal")
                    elif line.startswith("-"*5):
                        # skip any line with dashes (shouldn't exist here but just in case)
                        continue
                    else:
                        self.left_text.insert(tk.END, line + "\n", "normal")
                self.left_text.insert(tk.END, "\n")

            # Insert UTC
            self.right_text.insert(tk.END, "Urgent Treatment Centres\n\n", "header")
            for entry, hosp_name in results["Urgent Treatment Centres"]:
                for line in entry:
                    if line.startswith("🏥 "):
                        if hosp_name in ["Cumberland Infirmary", "West Cumberland Hospital",
                                         "Penrith Community Hospital", "Keswick Community Hospital"]:
                            self.right_text.insert(tk.END, line + "\n", "highlighted_hospital")
                        else:
                            self.right_text.insert(tk.END, line + "\n", "normal")
                    elif line.startswith("-"*5):
                        # Skip line after Penrith Community Hospital
                        if hosp_name == "Penrith Community Hospital":
                            continue
                        else:
                            self.right_text.insert(tk.END, line + "\n", "normal")
                    else:
                        self.right_text.insert(tk.END, line + "\n", "normal")
                self.right_text.insert(tk.END, "\n")

        for text_widget in (self.left_text, self.right_text):
            text_widget.config(state="disabled")

    def countdown_and_refresh(self):
        for remaining in range(REFRESH_INTERVAL, 0, -1):
            mins, secs = divmod(remaining, 60)
            self.countdown_label.config(text=f"⏳ Next refresh in: {mins:02d}:{secs:02d}")
            time.sleep(1)
        self.refresh_data()
        self.start_auto_refresh()

    def start_auto_refresh(self):
        threading.Thread(target=self.countdown_and_refresh, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = NHSMonitorApp(root)
    root.mainloop()


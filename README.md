🩺 NCIC Live A&E Monitor

This is a Python application that allows you to view live data of the amount of patients in A&E and the latest waiting times, at NCIC facilities. The data is scraped from the ncic.nhs.uk waiting times page and displayed in a user-friendly GUI.


## Features

    Real-time Data: Displays the latest A&E and UTC waiting times for NCIC hospitals

    Auto-refresh: The app automatically refreshes data every 5 minutes with a countdown timer.

    Customizable UI: The interface is split into two sections for A&E and UTC departments, with hospital names highlighted for clarity.

    Data Fetching: Uses BeautifulSoup to scrape HTML tables from the NHS website, parsing the relevant data on patients, wait times, and arrivals.

Requirements

To run this application, you need to have the following Python libraries installed:

    requests

    beautifulsoup4

    tkinter (usually comes pre-installed with Python)

You can install the required libraries using pip:

pip install requests beautifulsoup4

Python Version

This script is compatible with Python 3.x.

How to Run

    Clone this repository to your local machine.


    Navigate to the directory:


    Run the script linux.py




The app should now open and display the current NHS waiting times for A&E and UTC departments in North Cumbria.

How It Works
GUI Components

    Title and Countdown: Displays the app title and a countdown timer showing the time remaining until the next data refresh.

    Two Panels: One panel shows A&E departments, and the other shows Urgent Treatment Centres (UTC).

    Hospital Information: Each hospital entry includes:

        Hospital name (with an icon)

        Number of patients currently in the department

        Average wait time

        Number of arrivals in the last hour

Data Fetching

The fetch_data() method scrapes the NHS page and extracts data from HTML tables using BeautifulSoup. This data is then formatted and displayed in the GUI.
Auto Refresh

The app refreshes the data every 5 minutes using a background thread, with a countdown timer indicating the time remaining until the next refresh.
Simplifying Hospital Names

The simplify_name() method is used to standardize and clean up hospital names, ensuring that any extra details (such as "24hrs") are removed for consistency.
Example Screenshot

Troubleshooting

    App doesn't load: Ensure that all required libraries are installed. Run pip install requests beautifulsoup4.

    No data appears: The data is fetched from the live NHS website, so ensure you have an internet connection and the website is accessible.

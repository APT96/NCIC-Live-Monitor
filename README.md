🩺 NCIC Live A&E Monitor

This is a Python application that allows you to view live data of the amount of patients in A&E and the latest waiting times, at North Cumbria Integrated Care (NCIC) facilities. The data is scraped from the ncic.nhs.uk waiting times page and displayed in a user-friendly GUI.


## Features

    Real-time Data: Displays the latest A&E and UTC waiting times for NCIC hospitals

    Auto-refresh: The app automatically refreshes data every 5 minutes with a countdown timer.

    Customizable UI: The interface is split into two sections for A&E and UTC departments, with hospital names highlighted for clarity.

    Data Fetching: Uses BeautifulSoup to scrape HTML tables from the NHS website, parsing the relevant data on patients, wait times, and arrivals.

## Requirements

To run this application, you need to have the following Python libraries installed:

    requests

    beautifulsoup4

    tkinter (usually comes pre-installed with Python)

You can install the required libraries using pip:

pip install requests beautifulsoup4

Python Version

This script is compatible with Python 3.x.

## How to Run

### Linux
   - Clone this repository to your local machine.

   - Navigate to the directory:

   - Run the script linux.py

### Windows

    - Download and run the windows.exe file

### iOS / iPadOS

    - Download the ios.py script and run it in Pythonista


## Troubleshooting

   - App doesn't load: Ensure that all required libraries are installed. Run pip install requests beautifulsoup4.

   - No data appears: The data is fetched from the live NHS website, so ensure you have an internet connection and the website is accessible.

## License

This project uses data sourced from the NHS website and is made available under the <a href="https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/">Open Government License</a>

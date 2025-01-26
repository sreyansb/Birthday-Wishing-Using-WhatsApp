# WhatsApp-Automation
WhatsApp automation using Selenium Python to wish people on their birthdays stored in TSV(tab separated values) files.

The file is **birthday.py** which automates WhatsApp Web using Selenium Python. Makes use of tsv files to store the events(birthdays/anniversaries).

Requirements:
 * Selenium for Python(pip install selenium)
 * chrome driver - can be downloaded from [https://chromedriver.chromium.org/downloads](here) based on your version of google chrome

For MacOS:
* On the chromedriver, we need to also run: `xattr -d com.apple.quarantine chromedriver`
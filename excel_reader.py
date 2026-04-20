# STEP 1: Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# STEP 3: Fetch webpage (THIS IS WHERE IT GOES)
url = "https://www.svvv.edu.in/Teaching-staff.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

# Check response
if response.status_code != 200:
    print("❌ Failed to fetch webpage")
    exit()

print("✅ Page fetched successfully!")

# STEP 4: Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# STEP 5: Extract full text from webpage
full_text = soup.get_text(separator="\n")

# Split into lines
lines = full_text.split("\n")


# STEP 6: Extract faculty names
names = []

for line in lines:
    line = line.strip()

    if line.startswith("Dr.") or line.startswith("Prof."):

        # Remove unwanted details
        line = re.sub(r'\(.*?\)', '', line)
        line = re.sub(r'Ph\.?D.*', '', line)
        line = re.sub(r'M\.?Tech.*', '', line)
        line = re.sub(r'B\.?Tech.*', '', line)

        line = line.strip()

        if 5 < len(line) < 60:
            names.append(line)

            # STEP 7: Clean data
names = list(set(names))
names.sort()

# STEP 8: Save to Excel
df = pd.DataFrame(names, columns=["Faculty Name"])

df.to_excel("faculty.xlsx", index=False)

print("✅ faculty.xlsx created successfully!")
print("📊 Total Faculty Found:", len(names))
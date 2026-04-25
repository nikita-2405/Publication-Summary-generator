import pandas as pd
from scholarly import scholarly
import requests
import time
import re
import threading
import os

# ================================
# LOAD DATA
# ================================
df = pd.read_excel("faculty.xlsx")

# If file already exists → resume
if os.path.exists("publications.xlsx"):
    existing_df = pd.read_excel("publications.xlsx")
    done_names = set(existing_df["Faculty Name"])
    all_data = existing_df.to_dict("records")
    print("🔁 Resuming... already done:", len(done_names))
else:
    done_names = set()
    all_data = []

# ================================
# CLEAN NAME
# ================================
def clean_name(name):
    name = re.sub(r'(Dr\.?|Prof\.?)', '', name)
    name = re.sub(r'[^a-zA-Z\s]', '', name)
    return name.strip()

# ================================
# DBLP
# ================================
def fetch_dblp(name):
    results = []
    try:
        url = f"https://dblp.org/search/publ/api?q={name}&format=json"
        response = requests.get(url, timeout=5)
        data = response.json()
        hits = data["result"]["hits"]["hit"]

        for item in hits[:3]:
            info = item.get("info", {})
            results.append({
                "Faculty Name": name,
                "Year": info.get("year", "N/A"),
                "Title": info.get("title", "N/A"),
                "Venue": info.get("venue", "DBLP"),
                "Source": "DBLP"
            })
    except:
        print("DBLP failed:", name)

    return results

# ================================
# GOOGLE SCHOLAR (SAFE)
# ================================
def fetch_scholar_safe(name, timeout=5):
    results = []

    def worker():
        try:
            search_query = scholarly.search_pubs(name)
            for i, pub in enumerate(search_query):
                results.append({
                    "Faculty Name": name,
                    "Year": pub['bib'].get('pub_year', 'N/A'),
                    "Title": pub['bib'].get('title', 'N/A'),
                    "Venue": "Unknown",
                    "Source": "Google Scholar"
                })
                if i == 1:
                    break
        except:
            pass

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("⏩ Scholar skipped:", name)
        return []

    return results

# ================================
# MAIN LOOP (ALL FACULTY)
# ================================
for name in df["Faculty Name"]:

    cname = clean_name(name)

    if cname in done_names:
        continue

    print(f"\n🔍 Processing: {cname}")

    # DBLP
    all_data.extend(fetch_dblp(cname))

    # Scholar
    all_data.extend(fetch_scholar_safe(cname))

    # SAVE AFTER EACH FACULTY ✅
    temp_df = pd.DataFrame(all_data)
    temp_df.to_excel("publications.xlsx", index=False)

    print("💾 Saved progress")

    time.sleep(3)  # avoid blocking

print("\n✅ ALL FACULTY PROCESSED")
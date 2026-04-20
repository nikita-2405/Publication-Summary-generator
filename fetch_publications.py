import pandas as pd
from scholarly import scholarly
import time

# Load faculty list
df = pd.read_excel("faculty.xlsx")

all_data = []

# Loop through faculty names
for name in df["Faculty Name"]:

    base_name = name.replace("Dr.", "").replace("Prof.", "").strip()

    # Try multiple name variations
    search_names = [
        base_name,
        base_name + " SVVV",
        base_name + " Indore"
    ]

    found = False

    for search_name in search_names:
        print(f"\n🔍 Searching for: {search_name}")

        try:
            search_query = scholarly.search_author(search_name)

            try:
                author = next(search_query)
            except StopIteration:
                continue

            author = scholarly.fill(author)
            publications = author.get('publications', [])

            if not publications:
                continue

            for pub in publications[:3]:
                pub = scholarly.fill(pub)

                title = pub['bib'].get('title', 'N/A')
                year = pub['bib'].get('pub_year', 'N/A')
                venue = pub['bib'].get('venue', 'N/A')

                print(f"{year} - {title}")

                all_data.append({
                    "Faculty Name": base_name,
                    "Year": year,
                    "Title": title,
                    "Venue": venue
                })

            found = True
            break

        except Exception as e:
            print("❌ Error:", str(e))
            continue

    if not found:
        print("❌ No author/publications found")

    time.sleep(3)

# ✅ ALWAYS CREATE FILE (IMPORTANT FIX)
result_df = pd.DataFrame(all_data)
result_df.to_excel("publications.xlsx", index=False)

if result_df.empty:
    print("⚠️ No data found, but publications.xlsx created")
else:
    print("✅ publications.xlsx created successfully!")
from scholarly import scholarly

try:
    search_query = scholarly.search_author("Abhishek Sharma")
    author = next(search_query)
    author = scholarly.fill(author)

    print("✅ Found:", author['name'])

except Exception as e:
    print("❌ Error:", e)
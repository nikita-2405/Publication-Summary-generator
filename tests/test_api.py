def classify(row):
    venue = str(row.get("Venue", "")).lower()
    source = str(row.get("Source", "")).lower()

    if "google scholar" in source:
        return "Journal"

    if "dblp" in source:
        return "Conference"

    if any(k in venue for k in ["journal", "elsevier", "springer"]):
        return "Journal"

    if any(k in venue for k in ["conference", "conf", "ieee"]):
        return "Conference"

    return "Other"


def test_classify_journal():
    row = {
        "Venue": "Elsevier Journal",
        "Source": "Google Scholar"
    }

    result = classify(row)

    assert result == "Journal"


def test_classify_conference():
    row = {
        "Venue": "IEEE Conference",
        "Source": "DBLP"
    }

    result = classify(row)

    assert result == "Conference"
import streamlit as st
import pandas as pd

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="Publication Summary Generator", layout="wide")

# ===============================
# HEADER
# ===============================
st.title("📊 Publication Summary Generator")
st.write("Upload your publication file to view dashboard")

# ===============================
# FILE UPLOAD
# ===============================
uploaded_file = st.file_uploader("Upload publications.xlsx", type=["xlsx"])

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    # Clean column names
    df.columns = [col.strip() for col in df.columns]

    # Ensure Source column exists
    if "Source" not in df.columns:
        df["Source"] = "Unknown"

    # ===============================
    # 🔥 FINAL CLASSIFICATION (FIXED)
    # ===============================
    def classify(row):
        venue = str(row.get("Venue", "")).lower()
        source = str(row.get("Source", "")).lower()

        # PRIORITY 1: SOURCE
        if "google scholar" in source:
            return "Journal"

        if "dblp" in source:
            return "Conference"

        # PRIORITY 2: VENUE KEYWORDS
        if any(k in venue for k in ["journal", "elsevier", "springer"]):
            return "Journal"

        if any(k in venue for k in ["conference", "conf", "ieee"]):
            return "Conference"

        return "Other"

    # Apply classification
    df["Type"] = df.apply(classify, axis=1)

    # Convert Year
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    # ===============================
    # 🔍 DEBUG (VERY IMPORTANT)
    # ===============================
    st.subheader("🔍 Debug Info")

    st.write("Columns:", df.columns.tolist())
    st.write("Source Distribution:", df["Source"].value_counts())
    st.write("Type Distribution:", df["Type"].value_counts())

    # ===============================
    # DASHBOARD
    # ===============================
    st.header("📈 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Publications", len(df))
    col2.metric("Journal Papers", len(df[df["Type"] == "Journal"]))
    col3.metric("Conference Papers", len(df[df["Type"] == "Conference"]))

    # ===============================
    # YEAR FILTER
    # ===============================
    st.subheader("📅 Filter by Year")

    min_year = int(df["Year"].min())
    max_year = int(df["Year"].max())

    year_range = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))

    df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

    # ===============================
    # JOURNAL TABLE
    # ===============================
    st.subheader("📄 Journal Publications")

    journal_df = df_filtered[df_filtered["Type"] == "Journal"]

    if journal_df.empty:
        st.warning("No Journal Publications Found")
    else:
        st.dataframe(journal_df)

    # ===============================
    # CONFERENCE TABLE
    # ===============================
    st.subheader("📄 Conference Publications")

    conf_df = df_filtered[df_filtered["Type"] == "Conference"]

    if conf_df.empty:
        st.warning("No Conference Publications Found")
    else:
        st.dataframe(conf_df)

    # ===============================
    # RAW DATA (OPTIONAL)
    # ===============================
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df_filtered)

    # ===============================
    # DOWNLOAD
    # ===============================
    st.download_button(
        "📥 Download Filtered Data",
        df_filtered.to_csv(index=False),
        "filtered_publications.csv",
        "text/csv"
    )

else:
    st.info("👆 Upload publications.xlsx to see dashboard")
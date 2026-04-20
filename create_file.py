import pandas as pd

data = [
    ["A Sharma", 2023, "AI in Healthcare", "IEEE Journal"],
    ["A Sharma", 2022, "Machine Learning Model", "Springer Conference"],
    ["A Sharma", 2021, "Deep Learning Study", "Elsevier Journal"],

    ["R Singh", 2023, "Data Mining Techniques", "IEEE Conference"],
    ["R Singh", 2022, "Big Data Analysis", "Elsevier Journal"],

    ["Anjali Gupta", 2021, "Cloud Computing Research", "Springer Journal"],
    ["Anjali Gupta", 2020, "IoT Applications", "IEEE Conference"]
]

df = pd.DataFrame(data, columns=["Faculty Name", "Year", "Title", "Venue"])

df.to_excel("publications.xlsx", index=False)

print("✅ Proper publications.xlsx created!")
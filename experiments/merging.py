import pandas as pd

# Load the data
data = pd.read_csv("data/main.csv")
reviews = pd.read_csv("data/main_short.csv")

# Drop the 'caption' column from the reviews dataframe
if "caption" in reviews.columns:
    reviews = reviews.drop(columns=["caption"])

reviews = reviews.drop(columns=["review", "region"])
# Merge the dataframes on the 'name' column
merged = pd.merge(data, reviews, on="name", how="left")

# Drop duplicate rows based on the 'name' column, keeping only the first match
merged = merged.drop_duplicates(subset="name", keep="first")

# Save the merged dataframe to a new csv file
merged.to_csv("merged_long.csv", index=False)

# importing libraries
import pandas as pd
import os
from datetime import datetime

# STEP 1 — Load JSON file
# we assume only one JSON file in data/ folder for simplicity
data_folder = "data"

# get JSON filename (latest trends file)
json_files = [f for f in os.listdir(data_folder) if f.startswith("trends_") and f.endswith(".json")]
json_files.sort()  # sort to get the latest one last
json_file = os.path.join(data_folder, json_files[-1])  # latest file

# load JSON into Pandas DataFrame
df = pd.read_json(json_file)

print(f"Loaded {len(df)} stories from {json_file}")

# STEP 2 — Clean the Data

# 2a — Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2b — Remove rows with missing critical values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 2c — Ensure score and num_comments are integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)  # fill missing num_comments with 0

# 2d — Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 2e — Strip extra spaces from title
df["title"] = df["title"].str.strip()

# STEP 3 — Save as CSV
output_file = os.path.join(data_folder, "trends_clean.csv")
df.to_csv(output_file, index=False)

print(f"Saved {len(df)} rows to {output_file}")

# Quick summary: number of stories per category
print("\nStories per category:")
print(df["category"].value_counts())
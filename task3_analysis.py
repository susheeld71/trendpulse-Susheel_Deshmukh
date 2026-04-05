# importing libraries
import pandas as pd
import numpy as np
import os

# STEP 1 — Load the cleaned CSV from Task 2
data_file = os.path.join("data", "trends_clean.csv")
df = pd.read_csv(data_file)

print(f"Loaded data: {df.shape}")  # show number of rows and columns
print("\nFirst 5 rows:")
print(df.head())

# Calculate overall averages
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()
print(f"\nAverage score   : {avg_score:.0f}")
print(f"Average comments: {avg_comments:.0f}")

# STEP 2 — Basic analysis with NumPy
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print(f"Mean score   : {mean_score:.0f}")
print(f"Median score : {median_score:.0f}")
print(f"Std deviation: {std_score:.0f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# Which category has the most stories
most_cat = df["category"].value_counts().idxmax()
most_cat_count = df["category"].value_counts().max()
print(f"\nMost stories in: {most_cat} ({most_cat_count} stories)")

# Story with the most comments
max_comments_idx = df["num_comments"].idxmax()
most_commented_story = df.loc[max_comments_idx, "title"]
most_comments = df.loc[max_comments_idx, "num_comments"]
print(f"\nMost commented story: \"{most_commented_story}\" — {most_comments} comments")

# STEP 3 — Add new columns
# Engagement = num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if score > average score, else False
df["is_popular"] = df["score"] > avg_score

# STEP 4 — Save the result
output_file = os.path.join("data", "trends_analysed.csv")
df.to_csv(output_file, index=False)
print(f"\nSaved to {output_file}")
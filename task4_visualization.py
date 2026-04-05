# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import os

# STEP 1 — Load the analysed CSV from Task 3
data_file = os.path.join("data", "trends_analysed.csv")
df = pd.read_csv(data_file)

# Create outputs folder if it doesn't exist
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

# -------------------------------
# STEP 2 — Chart 1: Top 10 Stories by Score
# -------------------------------
# Sort stories by score descending and take top 10
top_stories = df.sort_values(by="score", ascending=False).head(10)

# Shorten titles longer than 50 characters
top_stories["short_title"] = top_stories["title"].apply(lambda x: x if len(x) <= 50 else x[:47] + "...")

plt.figure(figsize=(10,6))
plt.barh(top_stories["short_title"], top_stories["score"], color="skyblue")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()  # highest score on top
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "chart1_top_stories.png"))
plt.close()  # close the figure to avoid overlap

# -------------------------------
# STEP 3 — Chart 2: Stories per Category
# -------------------------------
category_counts = df["category"].value_counts()

plt.figure(figsize=(8,6))
colors = ["skyblue", "orange", "green", "red", "purple"]
plt.bar(category_counts.index, category_counts.values, color=colors)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "chart2_categories.png"))
plt.close()

# -------------------------------
# STEP 4 — Chart 3: Score vs Num_comments
# -------------------------------
# Separate popular vs non-popular stories
popular = df[df["is_popular"] == True]
non_popular = df[df["is_popular"] == False]

plt.figure(figsize=(8,6))
plt.scatter(popular["score"], popular["num_comments"], color="red", label="Popular", alpha=0.7)
plt.scatter(non_popular["score"], non_popular["num_comments"], color="blue", label="Not Popular", alpha=0.7)
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "chart3_scatter.png"))
plt.close()

# -------------------------------
# BONUS — Dashboard (combine charts)
# -------------------------------
fig, axes = plt.subplots(1, 3, figsize=(20,6))

# Chart 1: Top stories horizontal bar
axes[0].barh(top_stories["short_title"], top_stories["score"], color="skyblue")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")
axes[0].invert_yaxis()
axes[0].set_title("Top 10 Stories")

# Chart 2: Stories per category
axes[1].bar(category_counts.index, category_counts.values, color=colors)
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].set_title("Stories per Category")

# Chart 3: Scatter plot
axes[2].scatter(popular["score"], popular["num_comments"], color="red", label="Popular", alpha=0.7)
axes[2].scatter(non_popular["score"], non_popular["num_comments"], color="blue", label="Not Popular", alpha=0.7)
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].set_title("Score vs Comments")
axes[2].legend()

fig.suptitle("TrendPulse Dashboard", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(output_folder, "dashboard.png"))
plt.close()

print(f"Charts saved to {output_folder}/")
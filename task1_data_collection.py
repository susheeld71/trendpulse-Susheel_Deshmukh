# importing required libraries
import requests     # used to call API
import json         # to save data in json file
import time         # to use sleep
import os           # to create folder
from datetime import datetime   # to get current date and time


# API links
top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
item_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# header (given in question)
headers = {"User-Agent": "TrendPulse/1.0"}


# categories and keywords
# we will check if title contains these words
categories = {
    "technology": ["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["nfl","nba","fifa","sport","game","team","player","league","championship"],
    "science": ["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment": ["movie","film","music","netflix","game","book","show","award","streaming"]
}


# list to store all stories
all_data = []

# keeping count of each category (max 25)
count = {
    "technology":0,
    "worldnews":0,
    "sports":0,
    "science":0,
    "entertainment":0
}


# function to find category based on title
def find_category(title):
    title = title.lower()   # converting to lowercase for easy matching

    # checking each category
    for cat in categories:
        for word in categories[cat]:
            if word in title:
                return cat   # return category if match found

    return None   # if nothing matches


# STEP 1: get top story ids
try:
    res = requests.get(top_url, headers=headers)
    ids = res.json()[:500]   # taking first 500 ids
except:
    print("error while fetching top stories")
    exit()


# STEP 2: loop through each story id
for i in ids:

    try:
        r = requests.get(item_url.format(i), headers=headers)
        story = r.json()
    except:
        print("error in story", i)
        continue   # skip this story

    # skip if story is empty or has no title
    if story is None or "title" not in story:
        continue

    # find category
    cat = find_category(story["title"])

    # store only if category found and limit not reached
    if cat is not None and count[cat] < 25:

        # extracting required fields
        one = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": cat,
            "score": story.get("score",0),
            "num_comments": story.get("descendants",0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # adding to list
        all_data.append(one)

        # increasing count
        count[cat] += 1

        # stop if all categories reached 25
        if (count["technology"]>=25 and count["worldnews"]>=25 and 
            count["sports"]>=25 and count["science"]>=25 and 
            count["entertainment"]>=25):
            break


# sleep for 2 seconds (as given in instructions)
time.sleep(2)


# STEP 3: save data into json file

# create data folder if not exists
if not os.path.exists("data"):
    os.mkdir("data")

# file name with date
fname = "data/trends_" + datetime.now().strftime("%Y%m%d") + ".json"

# writing json file
with open(fname, "w") as f:
    json.dump(all_data, f, indent=4)

# final output message
print("Collected", len(all_data), "stories. Saved to", fname)
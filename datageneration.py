# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 19:25:13 2026

@author: nupur
"""

import pandas as pd
import random  #It helps generate random numbers, pick random items, or shuffle data.
from faker import Faker #This library is used to create fake data like names, addresses, emails, etc.
from datetime import datetime, timedelta  #datetime is used to work with dates and time, while timedelta helps add or subtract time (like days or hours).



fake = Faker()

#  Expanded topics (more realistic news coverage) Total topic : 20
#A list of 20 news categories like AI, elections, cricket, etc.
#The code will randomly pick one topic for each news article.

topics = [
    "Artificial Intelligence", "Elections", "Stock Market", "Cricket",
    "Climate Change", "Global Economy", "Healthcare", "Education",
    "Cybersecurity", "Space Exploration", "Cryptocurrency",
    "Technology Innovation", "Inflation", "Jobs Market",
    "Social Media", "Electric Vehicles", "Government Policy",
    "International Relations", "Startup Ecosystem", "AI Regulation"
]

#  More realistic news sources
#A list of words like “growth”, “impact”, etc.
#These are used to make the news content sound more meaningful and realistic.

sources = [
    "BBC News", "CNN", "Reuters", "Al Jazeera", "The Hindu",
    "Times of India", "NDTV", "Bloomberg", "The Guardian",
    "Washington Post", "India Today", "Economic Times"
]

#  Keywords pool (to make content richer)
#Generates a random date between two given dates.
#It uses timedelta and random.randint() to pick a random number of days.
keywords = [
    "growth", "impact", "rise", "decline", "global trends",
    "policy changes", "market shift", "innovation",
    "concerns", "opportunities", "analysis", "reports"
]

def random_date(start, end): #Defines the time range for your fake news data. All generated dates will fall between these two.
    return start + timedelta(days=random.randint(0, (end - start).days))

start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 4, 1)

data = []

for i in range(300):  #  Runs 300 times to create 300 news articles.Each loop generates one complete news record.
    topic = random.choice(topics)
    keyword = random.choice(keywords) #Randomly selects a topic and a keyword from the lists.This makes each news item different.

    title = f"{topic}: {fake.sentence(nb_words=6)}" #Creates a fake news headline. It combines the topic with a randomly generated sentence.

    content = (
        f"{topic} is showing significant {keyword} in recent reports. "
        f"{fake.paragraph(nb_sentences=4)} "
        f"Experts suggest that the current situation may influence global markets and policies."
    )
#Builds a paragraph for the news article.It mixes topic + keyword + fake paragraph + a realistic closing line.
    
    date = random_date(start_date, end_date) #Assigns a random date and a random news source to each article.
    source = random.choice(sources)

    data.append([date, title, content, source]) #Adds each news record (date, title, content, source) into the data list.

# Create DataFrame
df = pd.DataFrame(data, columns=["date", "title", "content", "source"])

# Save dataset
df.to_csv("news_dataset.csv", index=False)

print("Enhanced dataset created successfully!")

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 19:25:13 2026

@author: nupur
"""

import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# 📌 Expanded topics (more realistic news coverage)
topics = [
    "Artificial Intelligence", "Elections", "Stock Market", "Cricket",
    "Climate Change", "Global Economy", "Healthcare", "Education",
    "Cybersecurity", "Space Exploration", "Cryptocurrency",
    "Technology Innovation", "Inflation", "Jobs Market",
    "Social Media", "Electric Vehicles", "Government Policy",
    "International Relations", "Startup Ecosystem", "AI Regulation"
]

# 📰 More realistic news sources
sources = [
    "BBC News", "CNN", "Reuters", "Al Jazeera", "The Hindu",
    "Times of India", "NDTV", "Bloomberg", "The Guardian",
    "Washington Post", "India Today", "Economic Times"
]

# 🧠 Keywords pool (to make content richer)
keywords = [
    "growth", "impact", "rise", "decline", "global trends",
    "policy changes", "market shift", "innovation",
    "concerns", "opportunities", "analysis", "reports"
]

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 4, 1)

data = []

for i in range(300):  # increased dataset size
    topic = random.choice(topics)
    keyword = random.choice(keywords)

    title = f"{topic}: {fake.sentence(nb_words=6)}"

    content = (
        f"{topic} is showing significant {keyword} in recent reports. "
        f"{fake.paragraph(nb_sentences=4)} "
        f"Experts suggest that the current situation may influence global markets and policies."
    )

    date = random_date(start_date, end_date)
    source = random.choice(sources)

    data.append([date, title, content, source])

# Create DataFrame
df = pd.DataFrame(data, columns=["date", "title", "content", "source"])

# Save dataset
df.to_csv("news_dataset.csv", index=False)

print("Enhanced dataset created successfully!")
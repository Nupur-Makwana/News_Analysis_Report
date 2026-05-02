from flask import Flask, render_template, request, jsonify
import pandas as pd
import re
import json
from collections import Counter
import os

app = Flask(__name__)

# ── Load & preprocess data once ──────────────────────────────────────────────
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "news_dataset.csv"))
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
df["title"]   = df["title"].str.lower()
df["content"] = df["content"].str.lower()
df["source"]  = df["source"].str.lower()

STOP_WORDS = set("""
a about above after again against all am an and any are aren't as at be because been
before being below between both but by can't cannot could couldn't did didn't do does
doesn't doing don't down during each few for from further get got had hadn't has hasn't
have haven't having he he'd he'll he's her here here's hers herself him himself his
how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more
most mustn't my myself no nor not of off on once only or other ought our ours ourselves
out over own same shan't she she'd she'll she's should shouldn't so some such than that
that's the their theirs them themselves then there there's these they they'd they'll
they're they've this those through to too under until up very was wasn't we we'd we'll
we're we've were weren't what what's when when's where where's which while who who's
whom why why's will with won't would wouldn't you you'd you'll you're you've your yours
yourself yourselves s t re ll ve d m
""".split())

def clean_text(text):
    text = re.sub(r"[^a-zA-Z ]", "", str(text))
    words = text.lower().split()
    return " ".join(w for w in words if w not in STOP_WORDS and len(w) > 2)

df["clean_title"]   = df["title"].apply(clean_text)
df["clean_content"] = df["content"].apply(clean_text)
df["final_text"]    = df["clean_title"] + " " + df["clean_content"]
df["month"]         = df["date"].dt.to_period("M").astype(str)

# ── Precompute stats ──────────────────────────────────────────────────────────
all_words = " ".join(df["final_text"])
word_freq = Counter(all_words.split())
top50 = word_freq.most_common(50)

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    sources    = sorted(df["source"].unique().tolist())
    date_min   = df["date"].min().strftime("%Y-%m-%d")
    date_max   = df["date"].max().strftime("%Y-%m-%d")
    total_arts = len(df)
    total_src  = len(sources)
    date_range = f"{df['date'].min().strftime('%b %Y')} – {df['date'].max().strftime('%b %Y')}"
    return render_template("index.html",
                           sources=sources,
                           date_min=date_min,
                           date_max=date_max,
                           total_arts=total_arts,
                           total_src=total_src,
                           date_range=date_range)

@app.route("/api/top-words")
def top_words():
    n = int(request.args.get("n", 20))
    data = word_freq.most_common(n)
    return jsonify({"words": [w for w,_ in data], "counts": [c for _,c in data]})

@app.route("/api/trend")
def trend():
    keyword = request.args.get("keyword", "").strip().lower()
    if not keyword:
        return jsonify({"error": "No keyword"}), 400

    temp = df.copy()
    temp["kcount"] = temp["final_text"].apply(lambda x: x.count(keyword))
    by_date = temp.groupby(temp["date"].dt.date)["kcount"].sum().reset_index()
    by_date.columns = ["date", "count"]
    by_date["date"] = by_date["date"].astype(str)

    by_month = temp.groupby("month")["kcount"].sum().reset_index()
    by_month.columns = ["month", "count"]

    total_mentions = int(temp["kcount"].sum())
    articles_with  = int((temp["kcount"] > 0).sum())
    peak_date_row  = by_date.loc[by_date["count"].idxmax()] if not by_date.empty else None
    peak_date      = str(peak_date_row["date"]) if peak_date_row is not None else "N/A"
    peak_val       = int(peak_date_row["count"]) if peak_date_row is not None else 0

    # source breakdown
    src_counts = {}
    for src in df["source"].unique():
        s = temp[temp["source"] == src]["kcount"].sum()
        if s > 0:
            src_counts[src] = int(s)
    src_counts = dict(sorted(src_counts.items(), key=lambda x: -x[1]))

    return jsonify({
        "keyword": keyword,
        "daily": {"dates": by_date["date"].tolist(), "counts": by_date["count"].tolist()},
        "monthly": {"months": by_month["month"].tolist(), "counts": by_month["count"].tolist()},
        "stats": {
            "total_mentions": total_mentions,
            "articles_with_keyword": articles_with,
            "peak_date": peak_date,
            "peak_value": peak_val,
            "coverage_pct": round(articles_with / len(df) * 100, 1)
        },
        "source_breakdown": src_counts
    })

@app.route("/api/heatmap")
def heatmap():
    keywords = request.args.get("keywords", "ai,economy,cricket,health,technology")
    kws = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    temp = df.copy()
    for k in kws:
        temp[k] = temp["final_text"].apply(lambda x: x.split().count(k))
    heat = temp.groupby("month")[kws].sum().reset_index()
    return jsonify({
        "months": heat["month"].tolist(),
        "keywords": kws,
        "matrix": heat[kws].values.tolist()
    })

@app.route("/api/dataset-stats")
def dataset_stats():
    return jsonify({
        "total_articles": len(df),
        "sources": df["source"].value_counts().to_dict(),
        "date_range": {
            "start": df["date"].min().strftime("%Y-%m-%d"),
            "end":   df["date"].max().strftime("%Y-%m-%d")
        },
        "top_words": [{"word": w, "count": c} for w,c in top50[:30]]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5050)

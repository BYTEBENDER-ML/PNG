import pandas as pd

def recommend_topic(performance_df):
    weak_topics = performance_df[performance_df['score'] < 50]['topic']
    return list(weak_topics.unique())

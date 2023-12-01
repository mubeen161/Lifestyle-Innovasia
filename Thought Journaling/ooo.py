import streamlit as st
from datetime import datetime
import json
import os
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

class Journal:
    def __init__(self):
        self.entries = []

    def add_entry(self, timestamp, entry_text):
        entry = {"timestamp": timestamp, "entry_text": entry_text}
        self.entries.append(entry)

    def view_entries(self):
        st.header("Journal Entries")
        for index, entry in enumerate(self.entries, start=1):
            timestamp = entry["timestamp"]
            entry_text = entry["entry_text"]
            st.write(f"{index}. {timestamp}\n{entry_text}\n")
            st.button(f"Delete Entry {index}", key=f"delete_{index}", on_click=self.delete_entry, args=(index-1,))
            st.write("------")

    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            deleted_entry = self.entries.pop(index)
            st.write("Entry deleted:")
            st.write(deleted_entry)
        else:
            st.write("Invalid entry index.")

    def sentiment_analysis(self):
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for entry in self.entries:
            entry_text = entry["entry_text"]
            blob = TextBlob(entry_text)
            polarity = blob.sentiment.polarity

            if polarity > 0.2:
                positive_count += 1
            elif polarity < -0.2:
                negative_count += 1
            else:
                neutral_count += 1
        
        return positive_count, negative_count, neutral_count

    def generate_word_cloud(self):
        all_text = " ".join([entry["entry_text"] for entry in self.entries])
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Word Cloud of Journal Entries")
        st.pyplot()

def main():
    st.title("Your Digital Journaling System")

    if "journal" not in st.session_state:
        st.session_state.journal = Journal()

    entry_text = st.text_area("Enter your journal entry:")
    timestamp = datetime.now().strftime("%m-%d %H:%M")

    if st.button("Add Entry"):
        st.session_state.journal.add_entry(timestamp, entry_text)
        st.success("Entry added!")

    if st.button("View Entries"):
        st.session_state.journal.view_entries()
    st.write("Saved Entries:")
    entries_table = []
    for index, entry in enumerate(st.session_state.journal.entries, start=1):
        timestamp = entry["timestamp"]
        entry_text = entry["entry_text"]
        entries_table.append((index, timestamp, entry_text))
    st.table(entries_table)

    search_term = st.text_input("Search Entry:")
    filtered_entries = [
        (index, timestamp, entry_text)
        for index, (index, timestamp, entry_text) in enumerate(entries_table, start=1)
        if search_term.lower() in entry_text.lower()
    ]
    if search_term:
        st.write("Filtered Entries:")
        st.table(filtered_entries)
    if st.button("Sentiment Analysis"):
        positive_count, negative_count, neutral_count = st.session_state.journal.sentiment_analysis()
        # st.write("Sentiment Analysis:")
        # st.write(f"Positive entries: {positive_count}")
        # st.write(f"Negative entries: {negative_count}")
        # st.write(f"Neutral entries: {neutral_count}")
        
        # Data visualization for sentiment analysis
        sentiment_df = pd.DataFrame({
            'Sentiment': ['Positive', 'Negative', 'Neutral'],
            'Count': [positive_count, negative_count, neutral_count]
        })
        st.bar_chart(sentiment_df.set_index('Sentiment'))
    if st.button("Generate Word Cloud"):
        st.session_state.journal.generate_word_cloud()

if __name__ == '__main__':
    main()

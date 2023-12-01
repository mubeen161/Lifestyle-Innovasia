import json
import os
from datetime import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

class Journal:
    def __init__(self, journal_type):
        self.journal_type = journal_type
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def save_entries(self):
        data = {
            "journal_type": self.journal_type,
            "entries": self.entries
        }
        filename = f"{self.journal_type}_journal.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Entries saved!")

    def load_entries(self):
        filename = f"{self.journal_type}_journal.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                self.entries = data["entries"]
                print("Entries loaded!")
        else:
            print("No journal entries found.")

    def view_entries(self, selected_date=None):
        if not selected_date:
            selected_date = input("Enter the date (YYYY-MM-DD) to view entries (leave empty to view all): ")
        
        if selected_date:
            selected_entries = [entry for entry in self.entries if entry["timestamp"].startswith(selected_date)]
            if selected_entries:
                for index, entry in enumerate(selected_entries):
                    timestamp = entry["timestamp"]
                    entry_text = entry["entry_text"]
                    print(f"{index + 1}. {timestamp}\n{entry_text}\n")
            else:
                print("No entries found for the selected date.")
        else:
            for index, entry in enumerate(self.entries):
                timestamp = entry["timestamp"]
                entry_text = entry["entry_text"]
                print(f"{index + 1}. {timestamp}\n{entry_text}\n")

    def visualize_sentiment_analysis(self):
        positive_count, negative_count, neutral_count = self.sentiment_analysis()

        labels = ["Positive", "Negative", "Neutral"]
        values = [positive_count, negative_count, neutral_count]
        colors = ["green", "red", "gray"]

        plt.bar(labels, values, color=colors)
        plt.title("Sentiment Analysis")
        plt.ylabel("Number of Entries")
        plt.show()

    def search_entries(self, keyword):
        matching_entries = []
        for entry in self.entries:
            if keyword.lower() in entry["entry_text"].lower():
                matching_entries.append(entry)
        if matching_entries:
            print("Matching entries:")
            for index, entry in enumerate(matching_entries):
                timestamp = entry["timestamp"]
                entry_text = entry["entry_text"]
                print(f"{index + 1}. {timestamp}\n{entry_text}\n")
        else:
            print("No matching entries found.")

    def edit_entry(self, index, new_text):
        if 0 <= index < len(self.entries):
            self.entries[index]["entry_text"] = new_text
            print("Entry edited.")
        else:
            print("Invalid entry index.")

    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            deleted_entry = self.entries.pop(index)
            print("Entry deleted:")
            print(deleted_entry)
        else:
            print("Invalid entry index.")

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
        all_text = ""
        for entry in self.entries:
            all_text += entry["entry_text"] + " "
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Word Cloud of Journal Entries")
        plt.show()

class DashboardUI:
    @staticmethod
    def display_visualizations(journal):
        journal.visualize_sentiment_analysis()

        tag_counts = {}
        for entry in journal.entries:
            tags = entry.get("tags", [])
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        tag_df = pd.DataFrame.from_dict(tag_counts, orient="index", columns=["Count"])
        tag_df.plot(kind="bar", title="Tag Distribution")

        ratings = [entry.get("rating", 0) for entry in journal.entries]
        rating_df = pd.DataFrame(ratings, columns=["Rating"])
        rating_df["Rating"].value_counts().sort_index().plot(kind="bar", title="Rating Distribution")

        plt.show()

def main():
    print("Welcome to your digital journaling system!")
    journal_type = input("Enter journal type (mood/thought): ").lower()

    if journal_type not in ["mood", "thought"]:
        print("Invalid journal type.")
        return

    journal = Journal(journal_type)

    while True:
        print("\nMenu:")
        print("1. Add entry")
        print("2. View entries")
        print("3. Search entries")
        print("4. Edit entry")
        print("5. Delete entry")
        print("6. Sentiment analysis")
        print("7. Generate word cloud")
        print("8. Save entries")
        print("9. Load entries")
        print("10. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            entry_text = input("Enter your journal entry: ")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = {"timestamp": timestamp, "entry_text": entry_text}
            if journal_type == "mood":
                positive_mood = input("Enter your positive mood: ")
                negative_mood = input("Enter your negative mood: ")
                entry["positive_mood"] = positive_mood
                entry["negative_mood"] = negative_mood
            journal.add_entry(entry)
        elif choice == "2":
            journal.view_entries()
        elif choice == "3":
            keyword = input("Enter keyword to search: ")
            journal.search_entries(keyword)
        elif choice == "4":
            index = int(input("Enter the index of the entry to edit: ")) - 1
            new_text = input("Enter the new text: ")
            journal.edit_entry(index, new_text)
        elif choice == "5":
            index = int(input("Enter the index of the entry to delete: ")) - 1
            journal.delete_entry(index)
        elif choice == "6":
            positive_count, negative_count, neutral_count = journal.sentiment_analysis()
            print("Sentiment Analysis:")
            print(f"Positive entries: {positive_count}")
            print(f"Negative entries: {negative_count}")
            print(f"Neutral entries: {neutral_count}")
        elif choice == "7":
            journal.generate_word_cloud()
        elif choice == "8":
            journal.save_entries()
        elif choice == "9":
            journal.load_entries()
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()

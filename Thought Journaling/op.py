import streamlit as st
from datetime import datetime
import json
import os

class Journal:
    def __init__(self):
        self.entries = []

    def add_entry(self, timestamp, entry_text):
        entry = {"timestamp": timestamp, "entry_text": entry_text}
        self.entries.append(entry)


    def save_entries(self):
        data = {
            "entries": self.entries
        }
        filename = "journal_entries.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        st.write("Entries saved!")

    def load_entries(self):
        filename = "journal_entries.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
                self.entries = data["entries"]
                st.write("Entries loaded!")
        else:
            st.write("No journal entries found.")
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

if __name__ == '__main__':
    main()

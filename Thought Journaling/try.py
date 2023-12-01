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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Add Entry"):
        st.session_state.journal.add_entry(timestamp, entry_text)
        st.success("Entry added!")

    if st.button("View Entries"):
        st.session_state.journal.view_entries()



if __name__ == '__main__':
    main()

# Personal Library Manager with Streamlit

import json
import streamlit as st # type: ignore
import os

# Save library to a text file
def save_library(library):
    with open("library.txt", "w") as file:
        json.dump(library, file, indent=4)

# Load library from a text file
def load_library():
    if os.path.exists("library.txt"):
        with open("library.txt", "r") as file:
            return json.load(file)
    return []


# Load library data
library = load_library()

genres = ["Fiction", "Non-Fiction", "Mystery", "Fantasy", "Science Fiction", "Biography", "History", "Other"]

st.set_page_config(layout="wide", page_title="Personal Library Manager")
st.title("📚 Personal Library Manager")

with st.sidebar:
    st.header("📌 Menu")
    menu_option = st.radio("Select an option", ["Add a Book", "Remove a Book", "Search Books", "Display All Books", "Library Statistics"])

# Add a book
if menu_option == "Add a Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, step=1)
    genre = st.selectbox("Genre", genres)
    read_status = st.checkbox("Read")
    
    if st.button("Add Book"):
        if title and author and year and genre:
            existing_book = next((book for book in library if book["Title"].lower() == title.lower()), None)
            if existing_book:
                st.error("A book with this title already exists!")
            else:
                library.append({"Title": title, "Author": author, "Year": year, "Genre": genre, "Read": read_status})
                save_library(library)
                st.success(f"Book '{title}' added!")
                
        else:
            st.error("Please fill in all fields.")

# Remove a book
elif menu_option == "Remove a Book":
    st.header("🗑️ Remove a Book")
    book_to_remove = st.selectbox("Select a book", [book["Title"] for book in library] + ["None"], index=len(library))
    if book_to_remove != "None" and st.button("Remove Book"):
        library = [book for book in library if book["Title"] != book_to_remove]
        save_library(library)
        st.success(f"Book '{book_to_remove}' removed!")
      
    
    if st.button("Remove All Books"):
        library.clear()
        save_library(library)
        st.success("All books removed!")
        st.rerun()

# Search books
elif menu_option == "Search Books":
    st.header("🔍 Search Books")
    search_query = st.text_input("Enter title or author:", placeholder="Start typing to see suggestions...")
    suggestions = [book["Title"] for book in library if search_query.lower() in book["Title"].lower()] + \
                  [book["Author"] for book in library if search_query.lower() in book["Author"].lower()]
    
    if search_query:
        matches = [book for book in library if search_query.lower() in book["Title"].lower() or search_query.lower() in book["Author"].lower()]
        if matches:
            st.write("### Suggested Matches:")
            st.selectbox("Suggestions", options=suggestions, index=0 if suggestions else None)
            for book in matches:
                st.write(f"**{book['Title']}** by {book['Author']} ({book['Year']}) - {'✅ Read' if book['Read'] else '❌ Unread'}")
        else:
            st.warning("No matches found.")

# Display all books
elif menu_option == "Display All Books":
    st.header("📖 All Books")
    if library:
        for book in library:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{book['Title']}** by {book['Author']} ({book['Year']}) - {'✅ Read' if book['Read'] else '❌ Unread'}")
            with col2:
                if not book['Read'] and st.button(f"Mark as Read", key=book['Title']):
                    book['Read'] = True
                    save_library(library)
                    st.rerun()
    else:
        st.info("Library is empty.")

# Display statistics
elif menu_option == "Library Statistics":
    st.header("📊 Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["Read"])
    if total_books > 0:
        st.write(f"- **Total Books:** {total_books}")
        st.write(f"- **Books Read:** {read_books} ({(read_books / total_books) * 100:.2f}%)")
    else:
        st.info("Library is empty.")

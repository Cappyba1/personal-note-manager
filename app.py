import os
import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import markdown
import uuid
from datetime import datetime

# Initialize paths
NOTES_DIR = os.path.join(os.path.dirname(__file__), "Notes")
CHROMA_DIR = os.path.join(NOTES_DIR, "chroma_db")
os.makedirs(NOTES_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

# Initialize Phi-3 model
llm = Ollama(model="phi3")

# Initialize embeddings and ChromaDB
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

# Function to save note as Markdown
def save_note(title, content, tags=None):
    # Check for duplicate note by title and content
    for file in os.listdir(NOTES_DIR):
        if file.endswith(".md"):
            with open(os.path.join(NOTES_DIR, file), "r") as f:
                existing_content = f.read()
                metadata = extract_metadata(existing_content)
                existing_title = metadata.get("title", "")
                # Extract content after header
                content_start = existing_content.find("# ") + len("# " + existing_title) + 2
                existing_body = existing_content[content_start:].strip()
                if existing_title == title and existing_body == content:
                    st.warning(f"Note with title '{title}' and identical content already exists.")
                    return metadata.get("id")

    if not tags:
        tags = infer_tags(content)

    # Normalize and flatten tags
    tags = [tag.strip().lower() for tag in tags]
    tags_str = ", ".join(tags)

    note_id = str(uuid.uuid4())
    date = datetime.now().strftime("%Y-%m-%d")
    header = f"---\nid: {note_id}\ndate: {date}\ntags: {tags_str}\n---\n"
    note_content = header + f"# {title}\n\n{content}"

    file_path = os.path.join(NOTES_DIR, f"{note_id}.md")
    with open(file_path, "w") as f:
        f.write(note_content)

    # Index in ChromaDB with flattened tags
    vectorstore.add_texts(
        [content],
        metadatas=[{"id": note_id, "title": title, "tags": tags_str}]
    )

    return note_id

# Function to infer tags using Phi-3
def infer_tags(content):
    prompt = f"Read the following note and suggest up to 3 concise, relevant tags (lowercase, no numbers or special characters, separated by commas):\n\n{content}\n\nTags:"
    response = llm(prompt)
    raw_tags = response.split(",")
    # Clean tags: remove numbers, special characters, and extra spaces
    tags = [''.join(c for c in tag.strip().lower() if c.isalnum() or c == ' ') for tag in raw_tags if tag.strip()]
    tags = [tag.replace(" ", "-") for tag in tags]  # Replace spaces with hyphens
    return tags[:3] # Limit to 3 tags

# Function to search notes
def search_notes(query, mode="semantic"):
    if mode == "semantic":
        try:
            # Ensure ChromaDB is properly initialized
            vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
            results = vectorstore.similarity_search_with_score(query, k=5)
            return [(res[0].metadata, res[0].page_content, res[1]) for res in results]
        except Exception as e:
            st.error(f"Semantic search error: {e}")
            return []
    else:
        # Keyword search
        matches = []
        for file in os.listdir(NOTES_DIR):
            if file.endswith(".md"):
                with open(os.path.join(NOTES_DIR, file), "r") as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        metadata = extract_metadata(content)
                        matches.append((metadata, content))
        return matches

# Function to extract metadata from Markdown
def extract_metadata(content):
    lines = content.split("\n")
    metadata = {}
    if lines and lines[0] == "---":
        try:
            i = 1
            while i < len(lines) and lines[i] != "---":
                if ": " in lines[i]:
                    key, value = lines[i].split(": ", 1)
                    metadata[key.strip()] = value.strip()
                i += 1
        except Exception as e:
            print(f"Metadata parsing error: {e}")
    return metadata

# Streamlit UI
st.set_page_config(page_title="Note Manager", layout="wide", initial_sidebar_state="expanded")
st.title("Personal Note Management System")
st.sidebar.header("Options")

# Create new note
with st.sidebar.form("new_note"):
    st.write("Create Note")
    title = st.text_input("Title")
    content = st.text_area("Content")
    submitted = st.form_submit_button("Save")
    if submitted and title and content:
        note_id = save_note(title, content)
        st.success(f"Note saved with ID: {note_id}")

# Search notes
search_query = st.text_input("Search Notes")
search_mode = st.radio("Search Mode", ["Semantic", "Keyword"])
if search_query:
    results = search_notes(search_query, mode=search_mode.lower())
    for metadata, content, *score in results:
        st.subheader(metadata.get("title", "Untitled"))
        st.write(f"Tags: {metadata.get('tags', 'None')}")
        st.markdown(content, unsafe_allow_html=True)
        if score:
            st.write(f"Similarity Score: {score[0]:.2f}")

# Review untagged notes
if st.sidebar.button("Review Untagged Notes"):
    untagged = []
    for file in os.listdir(NOTES_DIR):
        if file.endswith(".md"):
            with open(os.path.join(NOTES_DIR, file), "r") as f:
                content = f.read()
                metadata = extract_metadata(content)
                if not metadata.get("tags") or metadata["tags"] == "None":
                    untagged.append((metadata, content))
    if untagged:
        st.write("Untagged Notes:")
        for metadata, content in untagged:
            st.subheader(metadata.get("title", "Untitled"))
            st.markdown(content, unsafe_allow_html=True)
    else:
        st.write("No untagged notes found.")

# Instructions for GitHub
if __name__ == "__main__":
    st.write("Run this app with: `streamlit run app.py`")
    st.write("Setup instructions in README.md")

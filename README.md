# Usage

- Create notes with auto-tagging.
- Search semantically or by keyword.
- Review untagged notes: `python scripts/review_notes.py`
- See `sample/sample_note.md` for note format.

## Notes Storage

- Notes are stored in `personal-note-manager/Notes`.
- The `chroma_db` subfolder is excluded from the repository.

## Setup Instructions

1. **Install Prerequisites**:
   - Python 3.11+: <https://www.python.org/downloads/>
   - Ollama: <https://ollama.com/download/windows>
   - GitHub Desktop: <https://desktop.github.com/>
   - Run: `ollama pull phi3`
2. **Clone the Repository**:
   - Use GitHub Desktop to clone `<https://github.com/yourusername/personal-note-manager>`.

3. **Set Up Virtual Environment**:
```markdown
4. **Set Up Virtual Environment**:

   ```bash
   cd personal-note-manager
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt .
   ```

## Running the  App

 ```bash
  ollama serve 
  streamlit run app.py
  ```
Open http://localhost:8501.

### Usage

 Create notes with auto-tagging.
 Search semantically or by keyword.
 Review untagged notes: python Scripts/review_notes.py
 Notes are stored in personal-note-manager/Notes.
 See Notes/sample_note.md for note format (if included).
 Notes Storage
 Notes are stored in personal-note-manager/Notes.
 The chroma_db subfolder (search index) is excluded from the repository.

### Requirements
 Python 3.11+
 Git
 Ollama with Phi-3 model (ollama pull phi3)
 Windows 11, 16GB RAM, NVIDIA GPU (RTX 4060 recommended)
 Dependencies (in requirements.txt):
 streamlit==1.45.0
 langchain==3.25
 langchain-community==0.3.23
 ollama==0.1.9
 chromadb==1.0.8
 sentence-transformers==4.1.0
 Markdown==3.6
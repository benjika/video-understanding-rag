# 🎥 Video Understanding App (FastAPI + Gradio + pgvector + Gemini)

This project lets you upload a video, analyze it using Google's Gemini LLM, extract semantic highlights, store them in PostgreSQL with `pgvector`, and chat with the content via a Gradio UI.

---

## 🚀 Features

- ✅ Upload videos via Gradio
- 🤖 Use Google Gemini to extract semantic video highlights and summaries
- 🧠 Save and search LLM-generated highlights using vector similarity (pgvector)
- 💬 Chat with video content using semantic search
- 🐳 Fully Dockerized setup

---

## 🗂️ Project Structure

app/  
├── main.py # FastAPI entry  
├── api/  
│ └── routes.py # API endpoints  
│ └── schemas.py # Pydantic models  
├── db/  
│ └── db_manager.py # Postgres + pgvector integration  
├── video_llm/  
│ └── llm_video_manager.py # Gemini LLM logic  
├── front/  
│ ├── front_main.py # Gradio UI with tabs  
│ ├── front_db_chat.py # Chat tab  
│ ├── front_video_loader.py # Upload tab  
├── video/ # Uploaded videos (volume-mounted)  


---

## 🧰 Tech Stack

- 🧬 **FastAPI** — backend API
- 🤖 **Google Generative AI (Gemini)** — for LLM-based video understanding and chat
- 🔍 **pgvector + PostgreSQL** — vector storage and search
- 🎛 **Gradio** — clean, tabbed frontend
- 🐳 **Docker** + `docker-compose` — easy deployment

---

## 🧪 How to Run

### 1. Clone the project

```bash
git clone https://github.com/benjika/video-understanding-rag.git
cd video-understanding-rag
```

### 2. Add your .env file:

```bash
GOOGLE_API_KEY=your_google_api_key
POSTGRES_DB=video_understanding_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=db
POSTGRES_PORT=5432
API_URL=http://app:8000/
```

## 3. Build and run with Docker:
```bash
docker-compose up --build
```

Access  
- The app will be available at [http://localhost:8000/gradio/](http://localhost:8000/gradio/)
- The Gradio UI is served at the root path.
> **Note:**  
> On the very first startup, it may take a few minutes for Gradio and the backend to build and initialize. Please be patient while the containers are being prepared.

---

Example Workflow  
1. Upload an .mp4 video via Gradio  
2. Google Gemini extracts highlights + summary  
3. Highlights saved to PostgreSQL using pgvector embeddings  
4. Ask questions like:  
    - "What happened in the beginning?"  
    - "Was there any speech?"  
5. Gradio shows an LLM-generated answer based on similar highlights  

---

## Notes

- Make sure your `GOOGLE_API_KEY` is valid for Gemini LLM.
- The database is persisted in the `pgdata` Docker volume.

---

📜 License  
MIT © 2025 Benny Katz
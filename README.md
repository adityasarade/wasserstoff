# Document Research & Theme Identification Chatbot

An interactive research assistant that lets you:
1. **Upload** PDFs or scanned images  
2. **Build** a semantic search knowledge base (FAISS + embeddings)  
3. **Query** your corpus and get cited answers  
4. **Synthesize** cross-document themes via an LLM

---

## 🚀 Features

- **OCR + Text Extraction** (PDFPlumber + Tesseract fallback)  
- **Chunking** into sentences with metadata (doc ID, page, sentence)  
- **Vector Indexing** (FAISS) and semantic search  
- **Per-document Summaries** and **Cross-document Theme Synthesis** via GROQ LLM  
- **Web UI** in React with file upload, doc selector, query bar, results table

---

## ⚙️ Local Setup

### Backend

1. **Install dependencies**  
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set your GROQ API key**
   ```bash
   export GROQ_API_KEY=<your_key>
   ```

3. **Run**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Test**
   ```
   Swagger UI: http://127.0.0.1:8000/docs
   Upload a PDF → /upload/
   Query → /search/?query=your+question
   ```

### Frontend

1. **Install**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure**
   * In `src/api.js`, set `baseURL` to `http://localhost:8000`

3. **Run**
   ```bash
   npm start
   ```

4. **Use** 
   http://localhost:3000

---

## 🌐 Deployment

### Backend on Hugging Face Spaces

1. Create a new **Docker** Space.
2. Push the **backend/** folder (with `Dockerfile`, `requirements.txt`, `app/`).
3. In Space **Settings → Secrets**, add `GROQ_API_KEY`.
4. Spaces will auto-build and serve on `0.0.0.0:8000`.
5. Verify `/docs` endpoint.

### Frontend on Vercel

1. Import this repo into Vercel, point to **frontend/**.
2. Build Command: `npm run build`
3. Output Directory: `build`
4. **Environment Variable**:
   ```
   REACT_APP_API_BASE_URL=https://<your-space>.hf.space
   ```
5. Deploy!

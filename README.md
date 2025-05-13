# 📝 YouTube Transcription Assistant

Transform any YouTube video into clear, structured notes powered by Google's Gemini AI. This tool extracts the transcript from a video and generates AI-assisted summaries, bullet points, and takeaways—perfect for students, content creators, and researchers.

<p align="center">
  <img src="https://img.icons8.com/color/96/000000/youtube-play.png" alt="YouTube Transcription Assistant Logo">
</p>

---

## 🚀 Features

* 🎥 **YouTube Integration** – Paste any YouTube link to extract its transcript
* 🧠 **Gemini AI Summarization** – Generates high-quality summaries, key takeaways, and notes
* ✨ **Rich Markdown Output** – Structured formatting with bullet points, headings, and highlights
* 📥 **Downloadable Notes** – Save results as Markdown files
* 📜 **Manual Transcript Input** – Paste your own transcript if needed
* 🌙 **Dark/Light Theme Support** – Dynamic interface for user comfort
* 🕘 **History Panel** – View and re-download previously generated notes

---

## 📸 Example Output

```markdown
## 🎓 Summary

- The speaker discusses the changing business landscape in 2025
- Importance of AI tools in accelerating startup workflows
- Financial planning and funding strategies
...

## 🔑 Key Takeaways

- "AI isn’t optional anymore—it’s the engine of every modern startup."
- Bootstrap smart, but plan for scale.
...

## 🗂 Detailed Notes

### 💡 Introduction
Speaker 1: Starting a business today is vastly different from five years ago...

### 🤖 Tools & Automation
Speaker 2: For example, AI tools can now write business plans in minutes...
```

---

## 🛠️ Tech Stack

* **Streamlit** – UI and frontend rendering
* **Python** – Core logic and backend
* **Google Gemini API** – AI summarization and note generation
* **YouTube Transcript API** – Pulls subtitles/transcripts from videos
* **dotenv** – Manages API keys securely
* **Pandas** – Stores user history

---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/youtube-transcriber.git
cd youtube-transcriber
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set your environment variables**
   Create a `.env` file and add your Gemini API key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

4. **Run the app**

```bash
streamlit run app.py
```

---

## 🌐 Usage

1. Paste a YouTube link
2. Click **"✨ Generate Notes"**
3. Let the app fetch and process the transcript
4. Review or download the generated notes
5. Optionally view or manage recent history

---

## 📌 Notes

* Works best with educational or commentary-style videos that have available transcripts
* Supports manual pasting of transcripts when captions are unavailable
* Video channel info requires further API integration (currently labeled "Unknown")

---

## 🧠 Future Enhancements

* 🎙️ Speaker recognition
* 🌍 Translation into other languages
* 🔗 Integration with YouTube Data API for richer metadata
* 📧 Email/export to Notion or Google Docs

---

## 📄 License

MIT License. See `LICENSE` file.



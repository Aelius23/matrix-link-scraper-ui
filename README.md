# 🔸 Matrix Link Scraper UI

A retro-styled web app for scraping links from Matrix channels and generating downloadable PDFs with page titles — featuring an animated frog mascot, tile backgrounds, and *Black Hole Sun* as MIDI.

---

## 🌐 Overview

This tool provides a surreal but functional UI to:

- 📅 Scrape links from Matrix chat channels  
- 📄 Generate PDFs with link titles + clickable URLs  
- 🖛 Display them in a solar panel-inspired interface  
- 🐸 Feature "Apple the Frog" — your animated assistant  

---

## 🧠 Components

- **Frontend:** `index.html` interface with CSS, button states, and hover effects  
- **Backend:** `main.py` with Flask, Matrix API calls, and PDF generation  
- **Static Assets:**
  - PNGs for buttons and interface elements  
  - Background tiles  
  - `BlackHoleSunMidi.mp3` on autoplay loop  

---

## ⚙️ Setup Instructions

### 1. 📁 Clone the repository

```bash
git clone https://github.com/yourname/matrix-link-scraper-ui.git
cd matrix-link-scraper-ui
```

### 2. 📦 Install dependencies

```bash
pip install flask matrix-nio fpdf aiohttp nest_asyncio beautifulsoup4 nio requests
```

### 3. 🔐 Set Matrix credentials

In `main.py`, replace the following lines:

```python
USERNAME = "@your_username:matrix.org"
ACCESS_TOKEN = "your_token_here"
```

### 4. 🧵 Configure your Matrix channel

Edit the channel in `index.html`:

```html
<select class="channel-dropdown" id="channel-dropdown">
  <option value="#your-channel:matrix.org">Your Channel Name</option>
</select>
```

### 5. ▶️ Run the server

```bash
python main.py
```

- The app will launch on **http://localhost:3000**

---

## ✨ Features

| Feature             | Description |
|---------------------|-------------|
| 🔗 Link Scraping    | Click the selector button to fetch Matrix message history |
| 📄 PDF Generation   | Automatically formats and downloads a clickable PDF |
| 🎨 Interactive UI   | Custom hover states, buttons, panels |
| 🐸 Mascot Energy    | Apple the Frog will keep you company |
| 🎵 Background Music | MIDI version of "Black Hole Sun" plays in loop (no off switch) |

---

## ⚠️ Notes

- Matrix tokens **expire often** – you'll need to refresh them periodically  
- Initial scraping takes **40–60 seconds**  
- PDF generation takes **1–2 minutes**  
- Music cannot currently be disabled (you may edit the HTML to remove autoplay)  >:)

---

## 📜 License

This project is licensed under the **MIT License** — see the [`LICENSE`](./LICENSE) file for full details.  
You are free to use, modify, and remix this project with attribution.

---

Made with frogs, vibes, and a love of Ally McBeal by [Spencer Toulouse](https://github.com/Aelius23)

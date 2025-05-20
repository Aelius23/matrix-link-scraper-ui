from flask import Flask, request, jsonify, send_file, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route("/")
def serve_index():
    return send_from_directory('.', 'index.html')

from nio import AsyncClient, RoomMessageText
import asyncio, re, io
from fpdf import FPDF
from flask import send_from_directory
import os
import nest_asyncio
import requests
from bs4 import BeautifulSoup

nest_asyncio.apply()

app = Flask(__name__, static_folder='static')

MATRIX_HOMESERVER = "https://matrix.org"
USERNAME = "@your-username:matrix.org"  # Replace with your Matrix User ID
ACCESS_TOKEN = "your-access-token"  # Replace with your Matrix access token

LINK_REGEX = r"(https?://[^\s]+)"

def fetch_title(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else "No Title Found"
    except Exception as e:
        print(f"Error fetching title for {url}: {e}")
        return "Title Unavailable"

def sanitize_text(text):
    return text.encode('latin-1', errors='ignore').decode('latin-1')

async def fetch_links_with_client(client_instance, room_id):
    links = []
    token = None
    while True:
        start_token = token or ""
        res = await client_instance.room_messages(room_id, start=start_token, direction="b", limit=100)
        if hasattr(res, "chunk"):
            for event in res.chunk:
                if isinstance(event, RoomMessageText):
                    found = re.findall(LINK_REGEX, event.body)
                    links.extend(found)
            if res.end:
                token = res.end
            else:
                break
        else:
            print("Error fetching messages:", res)
            break
    return list(set(links))

async def join_if_needed_and_fetch(room):
    local_client = AsyncClient(MATRIX_HOMESERVER, USERNAME)
    local_client.access_token = ACCESS_TOKEN
    try:
        print(f"Trying to fetch links directly for {room}...")
        links = await fetch_links_with_client(local_client, room)
        if links:
            await local_client.close()
            return links
        else:
            raise Exception("No links found initially")
    except Exception as e:
        print(f"Fetch failed, trying to join... ({e})")
        try:
            join_resp = await local_client.join(room)
            print("Join response (download):", join_resp)
            room_id = getattr(join_resp, "room_id", room)
            links = await fetch_links_with_client(local_client, room_id)
            await local_client.close()
            return links
        except Exception as e:
            print(f"Join failed: {e}")
            await local_client.close()
            return []

@app.route("/api/download")
def download_pdf():
    room = request.args.get("room")
    if not room:
        return jsonify({"error": "Missing room param"}), 400

    links = asyncio.get_event_loop().run_until_complete(join_if_needed_and_fetch(room))
    if not links:
        return jsonify({"error": "No links found"}), 404

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for link in links:
        title = fetch_title(link)
        title = sanitize_text(title)

        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 10, title)

        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 10, link, ln=True, link=link)
        pdf.ln(5)

    pdf_bytes = io.BytesIO()
    pdf_output = pdf.output(dest='S')
    pdf_bytes.write(pdf_output.encode('latin1'))
    pdf_bytes.seek(0)

    return send_file(pdf_bytes, download_name="links.pdf", as_attachment=True)

@app.route("/api/scrape")
def scrape_links():
    room = request.args.get("room")
    if not room:
        return jsonify({"error": "Missing room param"}), 400

    links = asyncio.get_event_loop().run_until_complete(join_if_needed_and_fetch(room))
    if not links:
        return jsonify({"error": "No links found"}), 404

    return jsonify({"links": links})

@app.route("/")
def serve_index():
    return send_from_directory(os.getcwd(), "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
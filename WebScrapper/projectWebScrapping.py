from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        # Get URL from the frontend
        url = request.json.get('url')
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Fetch the webpage
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch URL. Status code: {response.status_code}"}), 500

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information
        data = {
            "title": soup.title.string if soup.title else "No title",
            "meta_description": soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else "No meta description",
            "meta_keywords": soup.find("meta", attrs={"name": "keywords"})["content"] if soup.find("meta", attrs={"name": "keywords"}) else "No meta keywords",
            "headings": {f"h{i}": [h.text.strip() for h in soup.find_all(f"h{i}")] for i in range(1, 7)},
            "links": [a['href'] for a in soup.find_all('a', href=True)],
            "images": [img['src'] for img in soup.find_all('img', src=True)]
        }

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
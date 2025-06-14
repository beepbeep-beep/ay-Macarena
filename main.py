from flask import Flask, request, render_template_string, redirect
import requests
from urllib.parse import quote

app = Flask(__name__)

DUCKDUCKGO_URL = "https://html.duckduckgo.com/html/?q={query}"

# Google-style search homepage with dark mode
@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head>
      <title>PrivateSearch</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          background-color: #121212;
          color: #ffffff;
          text-align: center;
          padding-top: 15%;
        }
        input[type="text"] {
          width: 60%;
          padding: 14px;
          font-size: 18px;
          border-radius: 24px;
          border: 1px solid #555;
          background-color: #2a2a2a;
          color: white;
        }
        button {
          padding: 14px 24px;
          font-size: 16px;
          border-radius: 24px;
          border: none;
          background-color: #4285f4;
          color: white;
          margin-left: 10px;
        }
        .logo {
          font-size: 48px;
          font-weight: bold;
          color: #ffffff;
          margin-bottom: 40px;
        }
      </style>
    </head>
    <body>
      <div class="logo">PrivateSearch</div>
      <form method="GET" action="/go">
        <input type="text" name="q" placeholder="Search privately..." required />
        <button type="submit">Search</button>
      </form>
    </body>
    </html>
    """)

# Determines the browser and redirects to the appropriate cloaked URL
@app.route("/go")
def go():
    q = request.args.get("q", "")
    ua = request.headers.get("User-Agent", "").lower()

    if "safari" in ua and "chrome" not in ua:
        return redirect(f"/sumdog-cloak?q={quote(q)}")
    else:
        return redirect(f"/showbie-cloak?q={quote(q)}")

# Proxy route for Safari users
@app.route("/sumdog-cloak")
def sumdog_cloak():
    q = request.args.get("q", "")
    duckduckgo_html = get_ddg_results(q)
    return render_template_string(duckduckgo_html)

# Proxy route for Chrome users
@app.route("/showbie-cloak")
def showbie_cloak():
    q = request.args.get("q", "")
    duckduckgo_html = get_ddg_results(q)
    return render_template_string(duckduckgo_html)

# Function that fetches DuckDuckGo results
def get_ddg_results(query):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(
            "https://html.duckduckgo.com/html/",
            data={"q": query},
            headers=headers,
            timeout=5
        )
        return response.text
    except Exception as e:
        return f"<h1>Error loading results</h1><p>{e}</p>"
@app.route("/")
def home():
    return render_template_string("""
 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

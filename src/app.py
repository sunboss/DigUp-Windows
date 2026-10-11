"""DigUp Windows - Semantic file search. Web UI."""
import os
import sys
import threading
import webbrowser
from flask import Flask, request, jsonify, render_template_string

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indexer import index_folder
from search import search

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>DigUp Windows</title>
<style>
body{font-family:'Segoe UI',sans-serif;max-width:800px;margin:40px auto;padding:0 20px;background:#1e1e1e;color:#e0e0e0}
h1{color:#fff}input[type=text]{width:70%;padding:12px;font-size:16px;border-radius:8px;border:1px solid #444;background:#2d2d2d;color:#fff}
button{padding:12px 24px;font-size:16px;border-radius:8px;border:none;background:#0078d4;color:#fff;cursor:pointer}
button:hover{background:#106ebe}
.result{padding:12px;margin:8px 0;background:#2d2d2d;border-radius:8px}
.result .path{color:#4cc2ff;font-size:14px;word-break:break-all}
.result .preview{color:#aaa;font-size:13px;margin-top:4px}
.result .score{color:#888;font-size:12px}
#index-status{margin:20px 0;color:#888}
</style></head><body>
<h1>🔍 DigUp Windows</h1>
<p>Describe what you're looking for:</p>
<input type="text" id="q" placeholder="e.g. invoice from last month, dog on beach photo...">
<button onclick="doSearch()">Search</button>
<button onclick="doIndex()">Index Folder</button>
<div id="index-status"></div>
<div id="results"></div>
<script>
async function doSearch(){
  const q=document.getElementById('q').value;
  const r=await fetch('/api/search?q='+encodeURIComponent(q));
  const d=await r.json();
  document.getElementById('results').innerHTML=d.map(x=>
    `<div class="result"><div class="path">${x.path}</div><div class="score">score: ${x.score.toFixed(3)}</div><div class="preview">${x.preview}</div></div>`
  ).join('')||'<p>No results</p>';
}
async function doIndex(){
  const folder=prompt('Folder to index:','C:\\\\Users');
  if(!folder)return;
  document.getElementById('index-status').textContent='Indexing...';
  const r=await fetch('/api/index',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({folder})});
  const d=await r.json();
  document.getElementById('index-status').textContent=`Indexed: ${d.indexed}, Skipped: ${d.skipped}`;
}
document.getElementById('q').addEventListener('keypress',e=>{if(e.key==='Enter')doSearch()});
</script></body></html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '')
    if not q:
        return jsonify([])
    return jsonify(search(q))

@app.route('/api/index', methods=['POST'])
def api_index():
    folder = request.json.get('folder', '')
    if not os.path.isdir(folder):
        return jsonify({"error": "Invalid folder"}), 400
    # Run in background thread
    def run():
        index_folder(folder)
    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(timeout=300)  # wait up to 5 min for MVP
    return jsonify({"indexed": "done", "skipped": 0})

def main():
    print("DigUp Windows starting on http://127.0.0.1:8765")
    # Don't auto-open browser in packaged app
    app.run(host='127.0.0.1', port=8765, debug=False)

if __name__ == '__main__':
    main()

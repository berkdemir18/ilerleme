# -*- coding: utf-8 -*-
"""İlerleme — tek ekranlık ilerleme takip uygulaması.

Neden böyle kurulu:
  - Veri `veri.json` olarak UYGULAMANIN YANINDA duruyor. Tarayıcı deposunda değil;
    yedeklenebilir, git'e atılabilir, elle açılıp okunabilir. Her yazmada bir önceki
    hâli `veri.json.bak`'a alıyor — yani hiçbir tik kaybolmuyor.
  - Sunucu, sayfa kapanınca kendini kapatıyor (sayfa 5 sn'de bir nabız atıyor,
    15 sn nabız gelmezse çıkıyor). Arkada açık kalan python süreci olmuyor.
  - Bağımlılık yok: sadece standart kütüphane. pip install gerekmez.
"""
import http.server, json, os, socket, socketserver, subprocess, sys, threading, time, io

# .exe olarak paketlenince index.html geçici klasörden (_MEIPASS) okunur,
# veri dosyası ise HER ZAMAN .exe'nin yanında durur — böylece görünür,
# yedeklenebilir ve güncelleme exe'yi değiştirse bile yerinde kalır.
DONMUS = getattr(sys, "frozen", False)
STATIK = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(sys.executable) if DONMUS else os.path.dirname(os.path.abspath(__file__))
VERI = os.path.join(BASE, "veri.json")
YEDEK = os.path.join(BASE, "veri.json.bak")
BOS = {"tahtalar": [], "aktif": None}

son_nabiz = time.time()


def oku():
    if not os.path.exists(VERI):
        return dict(BOS)
    try:
        with io.open(VERI, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # bozuk dosya: yedekten dön
        if os.path.exists(YEDEK):
            try:
                with io.open(YEDEK, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return dict(BOS)


def yaz(d):
    if os.path.exists(VERI):
        try:
            with io.open(VERI, encoding="utf-8") as f:
                eski = f.read()
            with io.open(YEDEK, "w", encoding="utf-8", newline="\n") as f:
                f.write(eski)
        except Exception:
            pass
    gecici = VERI + ".tmp"
    with io.open(gecici, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    os.replace(gecici, VERI)


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=STATIK, **k)

    def log_message(self, *a):
        pass

    def _json(self, obj, kod=200):
        gövde = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(kod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(gövde)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(gövde)

    def do_GET(self):
        global son_nabiz
        if self.path == "/api/veri":
            return self._json(oku())
        if self.path == "/api/nabiz":
            son_nabiz = time.time()
            return self._json({"ok": True})
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        global son_nabiz
        if self.path != "/api/veri":
            return self._json({"hata": "bilinmeyen yol"}, 404)
        n = int(self.headers.get("Content-Length", 0))
        try:
            d = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception as e:
            return self._json({"hata": str(e)}, 400)
        yaz(d)
        son_nabiz = time.time()
        return self._json({"ok": True})


def bos_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def tarayici(url):
    for yol in (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ):
        if os.path.exists(yol):
            profil = os.path.join(os.environ.get("LOCALAPPDATA", BASE), "ilerleme-pencere")
            return subprocess.Popen([
                yol, "--app=" + url, "--user-data-dir=" + profil,
                "--window-size=1180,820", "--no-first-run", "--no-default-browser-check",
            ])
    import webbrowser
    webbrowser.open(url)
    return None


def bekci(httpd):
    while True:
        time.sleep(5)
        if time.time() - son_nabiz > 15:
            httpd.shutdown()
            return


if __name__ == "__main__":
    port = bos_port()
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", port), H)
    url = "http://127.0.0.1:%d/" % port
    if "--sunucu" not in sys.argv:
        tarayici(url)
        threading.Thread(target=bekci, args=(httpd,), daemon=True).start()
    else:
        print(url, flush=True)
    httpd.serve_forever()

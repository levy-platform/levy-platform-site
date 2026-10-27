"""Builds amirnet/index.html (levy-platform.com) from page.html, the same page published as the claude.ai artifact.
Run: python3 -I _amirnet_src/build.py   (from the repo root or anywhere)"""
import os, sys
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
page = open(os.path.join(here, "page.html"), encoding="utf-8").read()
emulator = "--emulator" in sys.argv
config = """{apiKey:"AIzaSyCLQ-OzqUBfLFhmlJVChS9BmhvnzFnEyyQ",authDomain:"amirnet-levy.firebaseapp.com",projectId:"amirnet-levy",storageBucket:"amirnet-levy.firebasestorage.app",messagingSenderId:"587503276267",appId:"1:587503276267:web:85100ac0ba0f3eda13eeae"}"""
fb = "11.10.0"
head = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="מכינת אמירנט: שיעורים, 3,900 מילים, מאות שאלות בפורמט המבחן, סימולציה בממשק המבחן ו-20 מבחני עבר רשמיים. מתכוננים לפטור באנגלית.">
<meta name="theme-color" content="#4F46E5">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="אמירנט">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta property="og:title" content="מכינת אמירנט">
<meta property="og:description" content="כל מה שצריך כדי להגיע לפטור באנגלית במבחן אמירנט.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%231c2330'/%3E%3Ctext x='32' y='43' font-size='30' font-family='Georgia' text-anchor='middle' fill='%23ffe46b'%3EA%3C/text%3E%3C/svg%3E">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<script src="https://www.gstatic.com/firebasejs/{fb}/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/{fb}/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/{fb}/firebase-firestore-compat.js"></script>
<script>window.FIREBASE_CONFIG={config};window.IS_SITE=true;{'window.FIREBASE_EMULATOR=true;' if emulator else ''}</script>
</head>
<body>
"""
import hashlib, glob
site = os.path.join(root, "amirnet")
h = hashlib.sha1(page.encode())
for f in sorted(glob.glob(os.path.join(site, "*.json"))): h.update(open(f, "rb").read())
version = h.hexdigest()[:10]
assets = ["./", "manifest.webmanifest"] + [os.path.basename(f) for f in sorted(glob.glob(os.path.join(site, "*.json")))] + ["icons/" + os.path.basename(f) for f in sorted(glob.glob(os.path.join(site, "icons", "*.png")))]
sw = open(os.path.join(here, "sw.template.js"), encoding="utf-8").read().replace("__VERSION__", version).replace("__ASSETS__", repr(assets).replace("'", '"'))
open(os.path.join(site, "sw.js"), "w", encoding="utf-8").write(sw)
register = "<script>if('serviceWorker' in navigator&&location.hostname!=='localhost'){addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}))}</script>"
out = os.path.join(root, "amirnet", "index.html")
open(out, "w", encoding="utf-8").write(head + page + "\n" + register + "\n</body>\n</html>\n")
print("wrote", out, "emulator" if emulator else "")

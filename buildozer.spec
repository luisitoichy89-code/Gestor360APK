[app]
title = Gestor360
package.name = gestor360
package.domain = org.luisito
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
source.include_patterns = .env
version = 1.0

# Flask + dependencias que usa app.py
requirements = python3,flask,supabase,httpx,gotrue,postgrest,realtime,storage3,python-dotenv

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
icon.filename = %(source.dir)s/icon.png

android.api = 33
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a

# Bootstrap webview: corre Flask y muestra una WebView apuntando a localhost
p4a.bootstrap = webview
p4a.port = 5000

# Seguridad: compila el código a bytecode (.pyc) y excluye el .py fuente del APK final
p4a.optimize_python = true

[buildozer]
log_level = 2
warn_on_root = 1

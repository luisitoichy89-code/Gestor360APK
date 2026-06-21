[app]
title = Gestor360
package.name = gestor360
package.domain = org.luisito
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
source.include_patterns = .env
version = 1.0

# Flask + dependencias que usa app_cliente.py, más pyjnius para crear
# el WebView nativo de Android desde Python (bootstrap sdl2)
requirements = python3,kivy,flask,supabase,httpx,gotrue,postgrest,realtime,storage3,python-dotenv,pyjnius,android

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
icon.filename = %(source.dir)s/icon.png

android.api = 33
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a

# Bootstrap sdl2: mucho más maduro y probado que "webview" (que falla en
# silencio en muchos dispositivos). Flask corre en un hilo de fondo y
# nosotros mismos creamos el WebView nativo vía pyjnius en main.py.
p4a.bootstrap = sdl2

# Seguridad: compila el código a bytecode (.pyc) y excluye el .py fuente del APK final
p4a.optimize_python = true

[buildozer]
log_level = 2
warn_on_root = 1

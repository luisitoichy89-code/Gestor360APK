import threading
import traceback
import os
import time

# Escribimos cualquier error de arranque a un archivo de texto plano,
# legible desde cualquier explorador de archivos del teléfono.
CRASH_LOG_PATHS = [
    '/sdcard/gestor360_crash.txt',
    os.path.join(os.path.expanduser('~'), 'gestor360_crash.txt'),
]

def _write_crash_log(texto):
    for path in CRASH_LOG_PATHS:
        try:
            with open(path, 'w') as f:
                f.write(texto)
        except Exception:
            continue

def run_flask():
    try:
        from app_cliente import app as flask_app
        flask_app.run(host='127.0.0.1', port=5000, threaded=True, debug=False, use_reloader=False)
    except Exception:
        _write_crash_log('ERROR AL CORRER FLASK:\n\n' + traceback.format_exc())

try:
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.clock import Clock
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
    activity = autoclass('org.kivy.android.PythonActivity').mActivity

    class GestorWebView(Widget):
        def __init__(self, **kwargs):
            super(GestorWebView, self).__init__(**kwargs)
            # Arrancamos Flask en un hilo de fondo antes de crear el WebView
            t = threading.Thread(target=run_flask)
            t.daemon = True
            t.start()
            # Pequeña espera para que Flask tenga tiempo de levantar el
            # servidor antes de que el WebView intente cargar la URL.
            Clock.schedule_once(self.create_webview, 1.5)

        @run_on_ui_thread
        def create_webview(self, *args):
            try:
                webview = WebView(activity)
                settings = webview.getSettings()
                settings.setJavaScriptEnabled(True)
                settings.setDomStorageEnabled(True)
                settings.setCacheMode(WebSettings.LOAD_DEFAULT)
                webview.setWebViewClient(WebViewClient())
                activity.setContentView(webview)
                webview.loadUrl('http://127.0.0.1:5000')
            except Exception:
                _write_crash_log('ERROR AL CREAR EL WEBVIEW:\n\n' + traceback.format_exc())

    class GestorApp(App):
        def build(self):
            return GestorWebView()

    if __name__ == '__main__':
        GestorApp().run()

except Exception:
    _write_crash_log('ERROR AL IMPORTAR / ARRANCAR LA APP (Kivy/pyjnius):\n\n' + traceback.format_exc())
    raise

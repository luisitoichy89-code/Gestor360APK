import threading
from app_cliente import app as flask_app

def run_flask():
    flask_app.run(host='0.0.0.0', port=5000, threaded=True, debug=False, use_reloader=False)

t = threading.Thread(target=run_flask)
t.daemon = True
t.start()

# El bootstrap "webview" de python-for-android detecta el servidor
# corriendo en el puerto indicado en p4a.port (buildozer.spec) y
# abre la WebView apuntando automáticamente a http://127.0.0.1:5000
t.join()

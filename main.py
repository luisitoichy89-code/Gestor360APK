import threading
import traceback
import os
import sys

# Escribimos cualquier error de arranque a un archivo de texto plano que se
# pueda abrir con cualquier explorador de archivos del teléfono, ya que
# logcat no está disponible sin root en muchos dispositivos Android.
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

try:
    from app_cliente import app as flask_app

    def run_flask():
        try:
            flask_app.run(host='0.0.0.0', port=5000, threaded=True, debug=False, use_reloader=False)
        except Exception:
            _write_crash_log('ERROR AL CORRER FLASK:\n\n' + traceback.format_exc())

    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    # El bootstrap "webview" de python-for-android detecta el servidor
    # corriendo en el puerto indicado en p4a.port (buildozer.spec) y
    # abre la WebView apuntando automáticamente a http://127.0.0.1:5000
    t.join()

except Exception:
    # Si el error ocurre incluso ANTES de poder arrancar Flask (ej. un
    # import roto de alguna dependencia), lo capturamos aquí igual.
    _write_crash_log('ERROR AL IMPORTAR / ARRANCAR LA APP:\n\n' + traceback.format_exc())
    # Re-lanzamos para que el comportamiento de crash siga siendo visible
    # también por cualquier otro medio (logcat si llegara a estar disponible).
    raise

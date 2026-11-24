import sys
import time
import urllib.error
import urllib.request

URLS = [
    "https://beledodev.com",
    "https://www.google.com",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/3",
    "https://esto-no-existe.invalid",
]
TIMEOUT = 5        # segundos antes de dar la petición por perdida
LENTO_MS = 2000    # a partir de estos milisegundos se considera lenta


def comprobar_url(url):
    """Devuelve (código HTTP o None, milisegundos, error o None)."""
    peticion = urllib.request.Request(url, headers={"User-Agent": "log-monitor/1.0"})
    inicio = time.perf_counter()
    try:
        with urllib.request.urlopen(peticion, timeout=TIMEOUT) as respuesta:
            codigo, error = respuesta.status, None
    except urllib.error.HTTPError as e:    # el servidor respondió, pero con 4xx o 5xx
        codigo, error = e.code, None
    except urllib.error.URLError as e:     # no se pudo conectar: DNS, SSL, conexión rechazada...
        codigo, error = None, str(e.reason)
    except OSError as e:                   # timeout u otro fallo de red
        codigo, error = None, type(e).__name__
    ms = round((time.perf_counter() - inicio) * 1000)
    return codigo, ms, error


def evaluar(codigo, ms, error):
    """Devuelve el estado: OK, LENTA, ERROR o CAÍDA."""
    if error:
        return "CAÍDA"
    if codigo >= 400:
        return "ERROR"
    if ms > LENTO_MS:
        return "LENTA"
    return "OK"


if __name__ == "__main__":
    hay_problemas = False
    for url in URLS:
        codigo, ms, error = comprobar_url(url)
        estado = evaluar(codigo, ms, error)
        detalle = error if error else f"HTTP {codigo}"
        print(f"[{estado:5}] {url} -> {detalle} en {ms} ms")
        if estado != "OK":
            hay_problemas = True

    sys.exit(1 if hay_problemas else 0)
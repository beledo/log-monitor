from collections import Counter

LOG_FILE = "sample.log"


def leer_log(ruta):
    """Devuelve las líneas del log sin las vacías."""
    with open(ruta, encoding="utf-8") as f:
        return [linea.strip() for linea in f if linea.strip()]


def contar_niveles(lineas):
    """Cuenta cuántas líneas hay de cada nivel: INFO, WARNING o ERROR."""
    contador = Counter()
    for linea in lineas:
        partes = linea.split()
        if len(partes) < 3:      # línea mal formada: la saltamos
            continue
        nivel = partes[2]
        contador[nivel] += 1
    return contador


def contar_errores_http(lineas):
    """Cuenta los errores por código HTTP y por endpoint."""
    por_codigo = Counter()
    por_endpoint = Counter()
    for linea in lineas:
        partes = linea.split()
        if len(partes) < 4 or partes[2] != "ERROR":
            continue
        codigo = partes[3]       # '500', '404'...
        endpoint = partes[-1]    # el último elemento: '/api/tickets'
        if codigo.isdigit():
            por_codigo[codigo] += 1
        if endpoint.startswith("/"):
            por_endpoint[endpoint] += 1
    return por_codigo, por_endpoint


def imprimir(titulo, contador):
    print(f"\n== {titulo} ==")
    for clave, total in contador.most_common():
        print(f"{clave}: {total}")


if __name__ == "__main__":
    lineas = leer_log(LOG_FILE)
    por_codigo, por_endpoint = contar_errores_http(lineas)

    imprimir("Niveles", contar_niveles(lineas))
    imprimir("Errores por código HTTP", por_codigo)
    imprimir("Endpoints con más errores", por_endpoint)
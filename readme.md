# log-monitor

Herramienta en Python para analizar logs de una aplicación y comprobar si sus servicios responden. La hice para practicar tareas habituales de soporte de aplicaciones: leer logs, detectar patrones de error, lanzar alertas y vigilar la disponibilidad.

## Qué hace

- **monitor.py**: lee un log y cuenta las líneas por nivel (INFO, WARNING, ERROR), los errores por código HTTP y los endpoints que más fallan. Lanza una alerta si los errores pasan de un umbral.
- **healthcheck.py**: comprueba una lista de URLs y muestra su estado (OK, LENTA, ERROR, CAÍDA) y el tiempo de respuesta.
- Los dos scripts terminan con código `0` si todo va bien y `1` si hay problemas, así se pueden lanzar desde un cron o un pipeline de despliegue.
- Solo usan la librería estándar de Python, sin dependencias.

## Uso

```bash
python3 monitor.py
python3 healthcheck.py
echo $?   # 0 = todo bien, 1 = hay problemas
```

## Ejemplo de salida

```
[OK   ] https://beledodev.com -> HTTP 200 en 137 ms
[ERROR] https://httpbin.org/status/500 -> HTTP 500 en 361 ms
[LENTA] https://httpbin.org/delay/3 -> HTTP 200 en 3356 ms
[CAÍDA] https://esto-no-existe.invalid -> [Errno 8] nodename nor servname provided, or not known en 3 ms
```

## Próximas mejoras

- Pasar los umbrales y las URLs por argumentos
- Enviar las alertas por correo o Slack
- Programarlo con cron
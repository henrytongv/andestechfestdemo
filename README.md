# Demo de uso de IA en la nube
Proyecto demo para mi charla "Inteligencia Artificial vista desde desarrollo en la nube" del evento Andes Tech Festival (Mendoza, Oct2024).

## Notas
- Este backend fue deployado en [Google AppEngine](https://cloud.google.com/appengine/docs/the-appengine-environments?hl=es-419) (tipo de deploy: estándar) para que pueda escalar a cero.

## A partir del 2024 necesitas agregar estos tres roles a tu usuario GCP para hacer deploy de AppEngine tipo estándar
- Artifact Registry Create-on-Push Writer
- Storage Admin
- Logs Writer

## Fly.io
La configuración para crear el Fly.io GPU Machine está en la carpeta fly_io/
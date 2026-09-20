# Subir el proyecto a GitHub

Nombre sugerido: `pnetlab-topologia`.

Descripción sugerida: Generador Python offline de topologías de monitoreo
PNETLab en draw.io, SVG y GraphML.

## Preparación

1. Descomprime el paquete y entra en la carpeta `pnetlab-topologia`.
2. Crea en tu cuenta un repositorio vacío llamado `pnetlab-topologia`.
3. Selecciona la visibilidad que prefieras. Para esta carga inicial, no añadas
   README, licencia ni gitignore desde GitHub: el paquete ya incluye README y
   gitignore. La elección de licencia queda a tu criterio.

## Publicación desde la terminal

Ejecuta dentro de la carpeta descomprimida:

```bash
git init -b main
git add .
git status
git commit -m "Agregar generador de topología PNETLab y ejemplos"
git remote add origin https://github.com/TU_USUARIO/pnetlab-topologia.git
git push -u origin main
```

Reemplaza `TU_USUARIO` por tu usuario real. Utiliza tu método de autenticación
GitHub configurado. Si Git solicita nombre y correo para el commit, configúralos
en este repositorio con tus propios datos:

```bash
git config user.name "Tu nombre"
git config user.email "Tu correo de commits"
```

Después repite el commit y el push. No incluyas contraseñas ni tokens en archivos.

## Cambios posteriores

```bash
python3 generar_topologia.py --salida ejemplos --sobrescribir
git add generar_topologia.py ejemplos README.md docs
git diff --cached --stat
git commit -m "Actualizar topología del laboratorio"
git push
```

El paquete está preparado para publicarse; descargarlo no crea un repositorio
en tu cuenta ni sube archivos automáticamente.

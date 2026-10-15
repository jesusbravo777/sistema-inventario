# Sistema de inventario

Aplicación educativa para administrar productos, cantidades y precios con **Python, Flask y SQLite**.

## Funciones
- Crear productos con nombre, stock y precio.
- Ver cantidad de tipos de productos y unidades.
- Actualizar el stock.
- Eliminar productos.
- Evitar nombres duplicados y cantidades negativas.

## Ejecutar en Windows
1. Instala Python 3.
2. Abre PowerShell en esta carpeta.
3. Crea entorno virtual: `py -m venv .venv`
4. Actívalo: `.\.venv\Scripts\Activate.ps1`
5. Instala dependencias: `pip install -r requirements.txt`
6. Ejecuta: `python app.py`
7. Abre `http://127.0.0.1:5000`

> Proyecto de práctica. Antes de publicar una aplicación real, añade autenticación, protección CSRF y configuración segura.

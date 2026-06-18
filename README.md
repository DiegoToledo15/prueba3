# Gestor de Eventos e Invitados

Aplicacion de consola en Python conectada a MongoDB local. Permite consultar eventos e invitados de la base de datos `prueba3`.

## Requisitos

- Python instalado
- MongoDB instalado e iniciado
- Libreria `pymongo`
- MongoDB Compass, opcional pero recomendado para importar los JSON

## Instalacion en un nuevo dispositivo

1. Copiar la carpeta del proyecto al nuevo equipo.

2. Instalar PyMongo:

```bash
pip install pymongo
```

3. Iniciar MongoDB en el equipo.

4. Crear o usar la base de datos:

```text
prueba3
```

5. Importar los archivos JSON en MongoDB:

- `eventos.json` en la coleccion `eventos`
- `invitados.json` en la coleccion `invitados`

6. Ejecutar el programa desde la carpeta del proyecto:

```bash
py app.py
```

Tambien puede ejecutarse con:

```bash
python app.py
```

## Opciones del programa

El menu permite:

1. Listar eventos
2. Buscar invitados por nombre
3. Buscar invitados por dominio de correo
4. Validar acceso de un invitado a un evento
5. Ver top 3 eventos con mas invitados confirmados
6. Ver invitados confirmados de un evento con datos personales
7. Salir

## Importante

La base de datos debe llamarse exactamente `prueba3`.
Las colecciones deben llamarse exactamente `eventos` e `invitados`.

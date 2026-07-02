from pymongo import MongoClient


# Conexion a MongoDB local
cliente = MongoClient("mongodb://localhost:27017/")

db = cliente["prueba3"]

eventos = db["eventos"]
invitados = db["invitados"]


def linea():
    print("-" * 50)


def titulo(texto):
    print("\n" + "=" * 50)
    print(texto)
    print("=" * 50)


def pausar():
    input("\nPresione Enter para volver al menu...")


def mostrar_invitado(invitado):
    linea()
    print(f"RUT: {invitado.get('rut', '')}")
    print(f"Nombre: {invitado.get('nombre', '')}")
    print(f"Correo: {invitado.get('correo', '')}")
    print(f"Empresa: {invitado.get('empresa', '')}")
    print(f"Estado: {invitado.get('estado', '')}")


def listar_eventos():
    titulo("LISTADO DE EVENTOS")

    # Mostramos un listado basico de eventos
    resultados = eventos.find(
        {},
        {"_id": 0, "codigo": 1, "nombre": 1, "fecha": 1, "lugar": 1, "categoria": 1}
    )

    encontrados = False
    for evento in resultados:
        encontrados = True
        linea()
        print(f"Codigo: {evento.get('codigo', '')}")
        print(f"Nombre: {evento.get('nombre', '')}")
        print(f"Fecha: {evento.get('fecha', '')}")
        print(f"Lugar: {evento.get('lugar', '')}")
        print(f"Categoria: {evento.get('categoria', '')}")

    if not encontrados:
        print("No hay eventos registrados.")

    linea()


def buscar_invitados_por_nombre():
    titulo("BUSCAR INVITADOS POR NOMBRE")

    texto = input("Ingrese parte del nombre: ").strip()

    if texto == "":
        print("Debe ingresar un texto para buscar.")
        return

    # Buscamos invitados usando una expresion regular
    resultados = invitados.find(
        {"nombre": {"$regex": texto, "$options": "i"}},
        {"_id": 0, "rut": 1, "nombre": 1, "correo": 1, "empresa": 1, "estado": 1}
    )

    encontrados = False
    for invitado in resultados:
        encontrados = True
        mostrar_invitado(invitado)

    if not encontrados:
        print("No se encontraron invitados con ese nombre.")

    if encontrados:
        linea()


def buscar_invitados_por_correo():
    titulo("BUSCAR INVITADOS POR CORREO")

    dominio = input("Ingrese correo o dominio a buscar: ").strip()

    if dominio == "":
        print("Debe ingresar un correo para buscar.")
        return

    # Buscamos invitados usando una expresion regular en el correo
    resultados = invitados.find(
        {"correo": {"$regex": dominio, "$options": "i"}},
        {"_id": 0, "rut": 1, "nombre": 1, "correo": 1, "empresa": 1, "estado": 1}
    )

    encontrados = False
    for invitado in resultados:
        encontrados = True
        mostrar_invitado(invitado)

    if not encontrados:
        print("No se encontraron invitados con ese correo o dominio.")

    if encontrados:
        linea()


def validar_acceso():
    titulo("VALIDAR ACCESO A EVENTO")

    rut = input("Ingrese RUT del invitado: ").strip()
    codigo_evento = input("Ingrese codigo del evento: ").strip()

    invitado = invitados.find_one({"rut": rut})

    if invitado is None:
        print("Invitado no encontrado")
        return

    # Validamos si el invitado esta activo
    if invitado.get("estado") == "bloqueado":
        print("Acceso denegado: invitado bloqueado")
        return

    evento = eventos.find_one({"codigo": codigo_evento})

    if evento is None:
        print("Evento no encontrado")
        return

    # Recorremos los invitados del evento para revisar si el RUT esta confirmado
    for persona in evento.get("invitados", []):
        if persona.get("rut") == rut:
            estado_evento = persona.get("estado")

            if estado_evento == "confirmado":
                print("Acceso permitido")
            else:
                print(f"Acceso denegado: estado en evento = {estado_evento}")
            return

    print("Acceso denegado: invitado no registrado en este evento")


def top_3_eventos():
    titulo("TOP 3 EVENTOS CON MAS CONFIRMADOS")

    # Usamos aggregate para contar invitados confirmados
    pipeline = [
        {"$unwind": "$invitados"},
        {"$match": {"invitados.estado": "confirmado"}},
        {
            "$group": {
                "_id": {
                    "codigo": "$codigo",
                    "nombre": "$nombre"
                },
                "total_confirmados": {"$sum": 1}
            }
        },
        {"$sort": {"total_confirmados": -1}},
        {"$limit": 3}
    ]

    resultados = eventos.aggregate(pipeline)

    encontrados = False
    for evento in resultados:
        encontrados = True
        linea()
        print(f"Codigo: {evento['_id'].get('codigo', '')}")
        print(f"Nombre: {evento['_id'].get('nombre', '')}")
        print(f"Invitados confirmados: {evento.get('total_confirmados', 0)}")

    if not encontrados:
        print("No hay eventos con invitados confirmados.")

    linea()


def invitados_confirmados_con_lookup():
    titulo("INVITADOS CONFIRMADOS POR EVENTO")

    codigo_evento = input("Ingrese codigo del evento: ").strip()

    # Usamos lookup para unir eventos con invitados por el campo rut
    pipeline = [
        {"$match": {"codigo": codigo_evento}},
        {"$unwind": "$invitados"},
        {"$match": {"invitados.estado": "confirmado"}},
        {
            "$lookup": {
                "from": "invitados",
                "localField": "invitados.rut",
                "foreignField": "rut",
                "as": "datos_invitado"
            }
        },
        {"$unwind": "$datos_invitado"},
        {
            "$project": {
                "_id": 0,
                "codigo": 1,
                "evento": "$nombre",
                "rut": "$datos_invitado.rut",
                "nombre": "$datos_invitado.nombre",
                "correo": "$datos_invitado.correo",
                "empresa": "$datos_invitado.empresa",
                "estado_invitado": "$datos_invitado.estado",
                "estado_evento": "$invitados.estado"
            }
        }
    ]

    resultados = eventos.aggregate(pipeline)

    encontrados = False
    for persona in resultados:
        encontrados = True
        linea()
        print(f"Evento: {persona.get('evento', '')}")
        print(f"Codigo: {persona.get('codigo', '')}")
        print(f"RUT: {persona.get('rut', '')}")
        print(f"Nombre: {persona.get('nombre', '')}")
        print(f"Correo: {persona.get('correo', '')}")
        print(f"Empresa: {persona.get('empresa', '')}")
        print(f"Estado invitado: {persona.get('estado_invitado', '')}")
        print(f"Estado en evento: {persona.get('estado_evento', '')}")

    if not encontrados:
        print("No se encontraron invitados confirmados para ese evento.")

    linea()


def menu():
    while True:
        titulo("MENU GESTOR DE EVENTOS")
        print("1. Listar eventos")
        print("2. Buscar invitados por nombre")
        print("3. Buscar invitados por dominio de correo")
        print("4. Validar acceso de invitado a evento")
        print("5. Top 3 eventos con mas invitados confirmados")
        print("6. Ver invitados confirmados de un evento con datos personales")
        print("7. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            listar_eventos()
            pausar()
        elif opcion == "2":
            buscar_invitados_por_nombre()
            pausar()
        elif opcion == "3":
            buscar_invitados_por_correo()
            pausar()
        elif opcion == "4":
            validar_acceso()
            pausar()
        elif opcion == "5":
            top_3_eventos()
            pausar()
        elif opcion == "6":
            invitados_confirmados_con_lookup()
            pausar()
        elif opcion == "7":
            print("Programa finalizado.")
            break
        else:
            print("Opcion invalida")
            pausar()


menu()

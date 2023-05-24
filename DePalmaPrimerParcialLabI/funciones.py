import os
import json

def menu()-> int:
    """menú de opciones
    
    returns:
        opción elegida (int)
    """
    print("""
                *** Administración de insumos - Tienda de Mascotas ***
        ----------------------------------------------
        1- Cargar datos desde archivo
        2- Listar cantidad por marca
        3- Listar insumos por marca
        4- Buscar insumo por característica
        5- Listar insumos ordenados
        6- Realizar compras
        7- Guardar en formato JSON
        8- Leer desde formato JSON
        9- Actualizar precios
        10- Agregar nuevo producto a la lista
        11- Guardar datos actualizados
        12- Salir""")
    opcion = int(input("Ingrese opción: "))
    
    return opcion

def salir() -> str:
    """Confirmación de salida

    returns:
        opción elegida (str)
    """
    salir = input("Confirma salida? s/n: ")
    while(salir != 's' and salir != 'n'):
        salir = input("Error. Confirma salida? s/n: ")
    salir = salir.lower()
    return salir

def cargar_datos(lista: list) -> list:
    """Carga la lista

    Args:
        lista (list): lista a cargar

    returns:
        lista (list): lista cargada
    """
    with open("insumos.csv", encoding="utf-8") as file:
        next(file)
        for linea in file:
            elementos = linea.strip("\n").split(",")
            diccionario = {
                "ID": elementos[0],
                "NOMBRE": elementos[1],
                "MARCA": elementos[2],
                "PRECIO": float(elementos[3].strip("$")),
                "CARACTERISTICAS": elementos[4].split("~") 
                }
            lista.append(diccionario)
    return lista

def cargar_marcas(lista: list) -> list:
    """Carga la lista de marcas

    Args:
        lista (list): lista a cargar

    returns:
        lista (list): lista cargada
    """
    marcas = []
    for insumo in lista:
        if not esta_en_lista(marcas, insumo["MARCA"]):
            marcas.append(insumo["MARCA"])
    return marcas

def listar_por_marca_elegida(lista: list, marca_elegida: str) -> None:
    marcas = cargar_marcas(lista)
    for marca in marcas:
            if(marca_elegida == marca.lower()):
                print(f"MARCA: {marca}")
                print(" ____________________________________________________")
                print("| ID |             NOMBRE             |    PRECIO    |")
                print("|____|________________________________|______________|")
                for insumo in lista:
                    if(insumo["MARCA"] == marca):
                    
                        print(f"| {insumo['ID']:2} | {insumo['NOMBRE']:31}|    ${insumo['PRECIO']:6}   |")
                        print("|____|________________________________|______________|")
                print("")  

def listar_por_marca(lista: list, condicion: str) -> None:
    """Lista los insumos por marca o da la cantiadd de insumos por marca según la condición ingresada 

    Args:
        lista (list): lista de insumos
        condición (str): determina si se dice la cantidad o se listan los insumos
    """
    marcas = []
    for insumo in lista:
        if not esta_en_lista(marcas, insumo["MARCA"]):
            marcas.append(insumo["MARCA"])
    
    if condicion == "cantidad":
        print(" _________________________________________")
        print("|           MARCA            |  CANTIDAD  |")
        print("|____________________________|____________|")        
        for marca in marcas: 
            acumulador = 0
            for insumo in lista:
                if(insumo["MARCA"] == marca):
                    acumulador += 1
    
            print(f"| {marca:22}     |   {acumulador:2}       |")
            print("|____________________________|____________|")

    elif condicion == "insumos":
        for marca in marcas:
            print(f"MARCA: {marca}")
            print(" _______________________________________________")
            print("|             NOMBRE             |    PRECIO    |")
            print("|________________________________|______________|")
            for insumo in lista:
                if(insumo["MARCA"] == marca):
                    
                    print(f"| {insumo['NOMBRE']:31}|    ${insumo['PRECIO']:6}   |")
                    print("|________________________________|______________|")
            print("")  

def esta_en_lista(lista: list, item: str) -> bool:
    """Determina si el item pasado por parámetro está en la lista

    Args:
        lista (list): lista 
        item (str): item a confirmar

    returns:
        esta (bool): True o False dependiendo si el item existe o no en la lista
    """
    esta = False
    for elemento in lista:
        if(elemento == item):
            esta = True
            break
    return esta

def listar_insumos(lista: list) -> None:
    """Lista los insumos pasados por la lista

    Args:
        lista (list): lista de insumos
    """
    print("______________________________________________________________________________________________________________________________________________________")
    print(" ID |           NOMBRE                |            MARCA            | PRECIO  |                             CARACTERISTICAS                           ")
    print("____|_________________________________|_____________________________|_________|_______________________________________________________________________")
    for insumo in lista:
        print(f" {insumo['ID']:2} | {insumo['NOMBRE']:31} | {insumo['MARCA']:22}      | ${insumo['PRECIO']:6} | ", end="")
        for carac in insumo["CARACTERISTICAS"]:
                    print(f" {carac} ", end="")
        print("")
        print("____|_________________________________|_____________________________|_________|_______________________________________________________________________")

def listar_insumos_ordenados(lista: list) -> None:
    """Lista los insumos ordenados pasados por la lista

    Args:
        lista (list): lista de insumos
    """
    print(" _______________________________________________________________________________________________________________")
    print("| ID |           NOMBRE                |            MARCA            | PRECIO  |         CARACTERISTICA         |")
    print("|____|_________________________________|_____________________________|_________|________________________________|")
    lista = ordenar_insumos(lista)
    for insumo in lista:
        print(f"| {insumo['ID']:2} | {insumo['NOMBRE']:31} | {insumo['MARCA']:22}      | ${insumo['PRECIO']:6} | {insumo['CARACTERISTICAS'][0]:30} |")
        print("|____|_________________________________|_____________________________|_________|________________________________|")

def ordenar_insumos(lista: list) -> list:
    """Ordena los insumos de la lista según marca y precio

    Args:
        lista (list): lista de insumos a ordenar

    returns:
        lista (list): lista de insumos ordenada
    """
    tam = len(lista)
    for i in range(tam - 1):
        for j in range(i + 1, tam):
            if((lista[i]["MARCA"] > lista[j]["MARCA"]) 
               or (lista[i]["MARCA"] == lista[j]["MARCA"] and lista[i]["PRECIO"] < lista[j]["PRECIO"])):
                aux = lista[i]
                lista[i] = lista[j]
                lista[j] = aux
    return lista

def buscar_insumo_por_caracteristica(lista: list) -> None:
    """Busca insumos por característica

    Args:
        lista (list): lista de insumos
    """
    listar_caracteristicas(lista)
    caracteristica = input("Ingrese característica: ")
    caracteristica = caracteristica.lower().strip(" ")
    esta = False
    print(" ______________________________________________________________________________________________________________________________________________________")
    print("  ID |           NOMBRE                |            MARCA            | PRECIO  |                             CARACTERISTICAS                           ")
    print(" ____|_________________________________|_____________________________|_________|_______________________________________________________________________")
    for item in lista:
        for elemento in item["CARACTERISTICAS"]:
            if elemento.lower() == caracteristica:
                print(f"  {item['ID']:2} | {item['NOMBRE']:31} | {item['MARCA']:22}      | ${item['PRECIO']:6} | ", end="")
                for carac in item["CARACTERISTICAS"]:
                    print(f" {carac} ", end="")
                print("")
                print(" ____|_________________________________|_____________________________|_________|_______________________________________________________________________")
                esta = True
                break

    if not esta:
        print("                                       No hay insumo con tal característica")

def listar_caracteristicas(lista: list) -> None:
    """Lista las características de los insumos

    Args:
        lista (list): lista de insumos
    """
    caracteristicas = []
    for item in lista:
        for i in range(len(item["CARACTERISTICAS"])):
            if not esta_en_lista(caracteristicas, item['CARACTERISTICAS'][i]):
                caracteristicas.append(item['CARACTERISTICAS'][i])
    for caracteristica in caracteristicas:
        print(caracteristica)

def listar_marcas(marcas: list) -> None:
    """Lista las marcas de los insumos

    Args:
        lista (list): lista de insumos
    """
    for marca in marcas:
        print(marca)


def realizar_compras(lista: list) -> None:
    """Realiza la compra de los insumos correspondientes según marca

    Args:
        lista (list): lista de insumos
    """
    total_precio = 0
    productos_comprados = []
    os.system("cls") 
    while True:
        marcas = cargar_marcas(lista)
        listar_marcas(marcas)
        marca_ingresada = input("Ingrese marca: ")
        marca_ingresada = marca_ingresada.lower().strip(" ")
        esta = False
        insumo_esta = False
        for item in lista:
            if marca_ingresada == item["MARCA"].lower():
                esta = True
        listar_por_marca_elegida(lista, marca_ingresada)

        if not esta:
            print("No hay insumos de esa marca")

        if esta:
            insumo_elegido = input("Elija un insumo a través de su ID: ")
            for item in lista:
                if insumo_elegido == item["ID"] and item["MARCA"].lower() == marca_ingresada:
                    precio = 0
                    while True:
                        try:
                            cantidad = int(input("Ingrese cantidad deseada: "))
                            while cantidad > 1000 or cantidad < 1:
                                cantidad = int(input("Error. Esa no es una cantidad válida. Ingrese cantidad deseada: "))
                            precio = cantidad * item["PRECIO"]
                            producto = {
                                "NOMBRE": item["NOMBRE"],
                                "PRECIO INDIVIDUAL": item["PRECIO"],
                                "CANTIDAD": cantidad,
                                "PRECIO TOTAL DEL PRODUCTO": precio
                            }
                            productos_comprados.append(producto)
                            total_precio += precio
                            break
                        except ValueError:
                            print("Error. Eso no es un número.")
                                
                    insumo_esta = True

            if not insumo_esta:
                print("No hay insumos con ese ID")

        seguir = input("Desea seguir comprando? s/n: ")
        while(seguir != 's' and seguir != 'n'):
            seguir = input("Error. Desea seguir comprando? s/n: ")
        print(f"Total de la compra: {total_precio:.2f}")
        factura(productos_comprados, total_precio)
        if seguir == 'n':
            break

def factura(productos: list, total: float) -> None:
    """Produce la factura de la compra de insumos

    Args:
        lista (list): lista de insumos
        total (float): total a pagar
    """
    with open("factura.txt", "w") as file:
        file.write(""" ______________________________________________________________________________________________
|       PRODUCTO                  | PRECIO   INDIVIDUAL | CANTIDAD | PRECIO TOTAL DEL PRODUCTO |
|_________________________________|_____________________|__________|___________________________|\n""")
        for producto in productos:
            file.write(f"""| {producto['NOMBRE']:31} | {producto['PRECIO INDIVIDUAL']:6}              |   {producto['CANTIDAD']:4}   | {producto['PRECIO TOTAL DEL PRODUCTO']:6.2f}                    | 
|_________________________________|_____________________|__________|___________________________|\n""")
        file.write(f"total a pagar: {total:.2f}")  

def crear_json(lista: list) -> None:
    """Crea un archivo json con los insumos que incluyen la palabra 'Alimento'

    Args:
        lista (list): lista de insumos 
    """
    lista_json = []
    for item in lista:
        if "Alimento" in item["NOMBRE"]:
              lista_json.append(item)

    with open("lista.json", "w", encoding="utf-8") as file:
        json.dump(lista_json, file, indent=4, ensure_ascii=False)
    print("El archivo fue generado correctamente")

def leer_json() -> None:
    """Lee el archivo json"""
    
    with open("lista.json", "r", encoding="utf-8") as file:
        lista = json.load(file)

    listar_insumos(lista)

def actualizar_precios(lista: list) -> None:
    """Actualiza los precios de la lista, aplicando un aumento del 8.4%

    Args:
        lista (list): lista de insumos a ser modificada en cuanto a su precio
    """
    
    precios_actualizados = list(map(lambda value: value["PRECIO"] * 108.4/100, lista))
    
    with open("insumos.csv", "w", encoding="utf-8") as file:
        file.write("ID,NOMBRE,MARCA,PRECIO,CARACTERISTICAS\n")
        for i in range(len(lista)):
                lista[i]["PRECIO"] = precios_actualizados[i]
                caracteristicas = lista[i]['CARACTERISTICAS']
                caracteristicas = ",".join(caracteristicas).replace(",","~")
                linea = f"{lista[i]['ID']},{lista[i]['NOMBRE']},{lista[i]['MARCA']},${lista[i]['PRECIO']:.2f},{caracteristicas}\n"
                file.write(linea)
    print("Los precios han sido actualizados")

def cargar_marcas_txt() -> list:
    
    marcas = []
    
    with open("marcas.txt") as file:
        for linea in file:
            marcas.append(linea.replace("\n",""))

    return marcas

def agregar_producto(lista: list) -> list:

        while True:
        
            last_id = len(lista)
            id = last_id + 1

            while True:
                nombre = input("Ingrese nombre del producto: ")
                if len(nombre) <= 31:
                    break
                else:
                    print("Error, ese es un nombre demasiado largo.")

            marcas = cargar_marcas_txt()
            listar_marcas(marcas)

            esta = False

            marca = input("Ingrese marca del producto: ")
            marca = marca.lower().strip(" ")  


            while True: 
                for elemento in marcas:
                    if marca == elemento.lower():
                        esta = True
                        break
            
                if not esta:
                    marca = input("Error. Esa marca no es correcta. Ingrese marca: ")
                    marca = marca.lower().strip(" ")
                if esta:
                        break

            while True:
                    try:
                        precio = int(input("Ingrese precio del producto: "))
                        while precio > 1000 or precio < 1:
                                precio = int(input("Error. Ese no es un precio válido. Ingrese precio del producto: "))
                        break
                    except ValueError:
                                print("Error. Eso no es un número.")
            
            caracteristicas = []

            continuar = 's'

            while continuar == 's' and len(caracteristicas) <= 3:

                caracteristica = input("Ingrese de 1 a 3 características del producto: ")
                caracteristicas.append(caracteristica)
                if(len(caracteristicas) < 3):
                    continuar = input("Desea seguir agregando características? s/n: ")
                else:
                    print("Ha llegado al límite de características")
                    break

                while(continuar != 's' and continuar != 'n'):
                    continuar = input("Error. Desea agregando características? s/n: ")
                if continuar == 'n':
                    break

            producto = {
                        "ID": id,
                        "NOMBRE": nombre,
                        "MARCA": marca,
                        "PRECIO": precio,
                        "CARACTERISTICAS": caracteristicas
                        }
            
            lista.append(producto)
        
            seguir = input("Desea seguir agregando productos? s/n: ")
            while(seguir != 's' and seguir != 'n'):
                seguir = input("Error. Desea agregando productos? s/n: ")
            if seguir == 'n':
                return lista
    
def submenu() -> int:

    print("""
        1- En formato json
        2- En formato csv
    """)
    opcion = int(input("Ingrese opción: "))
    
    return opcion

def guardar_en_json(lista: list) -> None:

    lista_json = []
    for item in lista:
              lista_json.append(item)

    while True:

        archivo = input("Ingrese nombre del archivo (solo letras): ")

        if archivo.isalpha() and len(archivo) <= 31:
            break
        else:
            print("Error, ese es un nombre inválido o demasiado largo.")

    with open(f"{archivo}.json", "w", encoding="utf-8") as file:
        json.dump(lista_json, file, indent=4, ensure_ascii=False)
    print("El archivo json fue generado correctamente")

def guardar_en_csv(lista: list) -> None:

    while True:
        archivo = input("Ingrese nombre del archivo (solo letras): ")
        if archivo.isalpha() and len(archivo) <= 31:
            break
        else:
            print("Error, ese es un nombre inválido o demasiado largo.")

    with open(f"{archivo}.csv", "w", encoding="utf-8") as file:
        file.write("ID,NOMBRE,MARCA,PRECIO,CARACTERISTICAS\n")
        for i in range(len(lista)):
            caracteristicas = lista[i]['CARACTERISTICAS']
            caracteristicas = ",".join(caracteristicas).replace(",","~")
            linea = f"{lista[i]['ID']},{lista[i]['NOMBRE']},{lista[i]['MARCA']},${lista[i]['PRECIO']:.2f},{caracteristicas}\n"
            file.write(linea)
    print("El archivo csv fue generado correctamente")

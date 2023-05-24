import os
from funciones import *

lista = []
lista_actualizada = []
flag_datos = False
flag_json = False
flag_lista_actualizada = False

while True:

    os.system("cls") 

    try:
        match(menu()): 

            case 1:
                
                lista = cargar_datos(lista)
                flag_datos = True

            case 2:

                if(flag_datos):
                    listar_por_marca(lista, "cantidad")
                else:
                    print("Cargue la lista primero")
            case 3:

                if(flag_datos):
                    listar_por_marca(lista, "insumos")
                else:
                    print("Cargue la lista primero")
                
            case 4:

                if(flag_datos):
                    buscar_insumo_por_caracteristica(lista)
                else:
                    print("Cargue la lista primero")

            case 5:

                if(flag_datos):
                    listar_insumos_ordenados(lista)
                else:
                    print("Cargue la lista primero")

            case 6:

                if(flag_datos):
                    realizar_compras(lista)
                else:
                    print("Cargue la lista primero")

            case 7:

                if(flag_datos):
                    crear_json(lista)
                    flag_json = True
                else:
                    print("Cargue la lista primero")

            case 8:

                if(flag_json):
                    leer_json()
                else:
                    print("Genere el archivo json para poder leerlo")

            case 9:

                if(flag_datos):
                    actualizar_precios(lista)
                else:
                    print("Cargue la lista primero")
            
            case 10:

                if(flag_datos):
                    lista_actualizada = agregar_producto(lista)
                    flag_lista_actualizada = True
                else:
                    print("Cargue la lista primero")

            case 11:

                if(flag_lista_actualizada): #agregar elegir nombre

                    match(submenu()):
                        case 1:
                            guardar_en_json(lista_actualizada)
                        case 2:
                            guardar_en_csv(lista_actualizada)
                        case _: 

                            print("Esa no es una opción válida")
                else:
                    print("Cargue la lista actualizada primero")

            case 12:   

                salida = salir()
                if (salida == 's'):
                    break

            case _: 

                print("Esa no es una opción válida")

    except ValueError:
        print("Esa no es una opción válida")

    os.system("pause")
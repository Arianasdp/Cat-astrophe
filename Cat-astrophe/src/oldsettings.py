#mapa de las plataformas del nivel 1
#mapa de filas y columnas que muestra dónde estarían las estructuras (y el personaje apenas aparece)

level_map = [
'                            ', 
'                            ',
'       X X    X X X         ',
'  XXX                       ',
'  XXX   P                   ',
'       XXXXXXXXXXXXXXXXXXXXX',
'     X XXXXXXXXXXXXXXXXXXXXX',
'       XXXXXXXXXXXXXXXXXXXXX',
'       XXXXXXXXXXXXXXXXXXXXX']

# tamaño de los cuadrados que forman las estructuras
tile_size_x = 30
tile_size_y = 34

for i in range(len(level_map)):
    row_len = len(level_map[i])

#tamaño de la pantalla
screen_width = 600 #probando este tamaño para ver si así logro mover la cámara
# screen_width = row_len * tile_size_x #tamaño entero
screen_height = len(level_map) * tile_size_y

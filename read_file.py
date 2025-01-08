archivo_ruta = 'archivo.txt'

with open(archivo_ruta, 'r', encoding='utf-8') as archivo:

    for linea in archivo:
        print(linea.strip())
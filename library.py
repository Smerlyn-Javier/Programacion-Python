from datetime import date

# Que debe hacer:

# a)  función buscar libros por autor
# b)  función buscar libros por título del libro
# c)  función  buscar libros por año 
# d)  función buscar libros por disponibilidad

def verificar_disponibilidad(funcion):
    def wrapper(*args, **kwargs):
        isbn = args[0]
        if not next((True for libro in libros if libro[0] == isbn and libro[4]), False):
            raise ValueError("El libro no está disponible")
        return funcion(*args, **kwargs)
    return wrapper

libros = [
    ["ISBN123", "El señor de los anillos", "J.R.R. Tolkien", 1954, True],
    ["ISBN456", "1984", "George Orwell", 1949, False],
    ["ISBN789", "Orgullo y prejuicio", "Jane Austen", 1813, True]
]

autores = {
    "J.R.R. Tolkien": ["ISBN123"],
    "George Orwell": ["ISBN456"],
    "Jane Austen": ["ISBN789"]
}

prestamos = {}

@verificar_disponibilidad
def prestar_libro(isbn):
    prestamos[isbn] = date.today()
    for libro in libros:
        if libro[0] == isbn:
            libro[4] = False

def devolver_libro(isbn):
    if isbn in prestamos:
        del prestamos[isbn]
        for libro in libros:
            if libro[0] == isbn:
                libro[4] = True

def libros_por_isbn(isbn):
    yield next(libro for libro in libros if libro[0] == isbn)

# Función para buscar libros por autor
def libros_por_autor(autor):
    for isbn in autores.get(autor, []):
        yield next(libro for libro in libros if libro[0] == isbn)

# Función para buscar libros por título
def libros_por_titulo(titulo):
    for libro in libros:
        if titulo.lower() in libro[1].lower():
            yield libro

# Función para buscar libros por año
def libros_por_año(año):
    for libro in libros:
        if libro[3] == año:
            yield libro

# Función para buscar libros por disponibilidad
def libros_por_disponibilidad(disponible=True):
    for libro in libros:
        if libro[4] == disponible:
            yield libro

# Ejemplo de uso:

# Prestar libro
try:
    prestar_libro("ISBN123")
except ValueError as e:
    print(e)

# Devolver libro
devolver_libro("ISBN123")

# Buscar libros por autor
print("\nLibros por autor:")
for libro in libros_por_autor("J.R.R. Tolkien"):
    print(libro)

# Buscar libros por título
print("\nLibros por título:")
for libro in libros_por_titulo("1984"):
    print(libro)

# Buscar libros por año
print("\nLibros por año:")
for libro in libros_por_año(1954):
    print(libro)

# Buscar libros por disponibilidad
print("\nLibros disponibles:")
for libro in libros_por_disponibilidad(True):
    print(libro)

print("\nLibros no disponibles:")
for libro in libros_por_disponibilidad(False):
    print(libro)

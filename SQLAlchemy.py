from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la conexión a MySQL
engine = create_engine('mysql+pymysql://bguevara:16557544@localhost/db_sqlAlchemy')

# Esta instrucción genera una clase base que servirá como plantilla para todas tus clases que representarán las tablas de tu base de datos
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', description='{self.description}')>"

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Crear un nuevo producto
new_producto = Product(name='producto 1', description='este es el producto 1')
session.add(new_producto)
session.commit()

# a) tarea crear el codigo para crear otro producto, colocar el codigo debajo de este comentario
new_producto_2 = Product(name='producto 2', description='este es el producto 2')
session.add(new_producto_2)
session.commit()

# Consultar todos los productos
products = session.query(Product).all()
for product in products:
    print(product)

# Consultar un producto específico
product = session.query(Product).filter_by(name='producto 1').first()
print(product)

# b) tarea crear el codigo para consultar otro producto, colocar el codigo debajo de este comentario
product_2 = session.query(Product).filter_by(name='producto 2').first()
print(product_2)

# Actualizar un producto
product.name = 'producto Actualizado'
session.commit()

# c) tarea crear el codigo para actualizar otro producto, colocar el codigo debajo de este comentario
if product_2:
    product_2.description = 'este es el producto 2 actualizado'
    session.commit()

# Eliminar un producto
session.delete(product)

# d) tarea crear el codigo para eliminar el segundo producto agregado, colocar el codigo debajo de este comentario
if product_2:
    session.delete(product_2)
session.commit()

session.close()

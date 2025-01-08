from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la conexión a MySQL
engine = create_engine('mysql+pymysql://bguevara:16557544@localhost/db_sqlAlchemy')

# Clase base para los modelos
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(120), nullable=False)
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', description='{self.description}')>"

# Crear las tablas
Base.metadata.create_all(engine)

# Crear sesión
Session = sessionmaker(bind=engine)
session = Session()

# Crear primer producto
new_producto = Product(name='🍎 Manzana', description='Manzana roja 🔴')
session.add(new_producto)
session.commit()

# a) Crear segundo producto
second_product = Product(name='🍐 Pera', description='Pera verde 🟢')
session.add(second_product)
session.commit()

# Consultar todos los productos
products = session.query(Product).all()
for product in products:
    print(product)

# Consultar primer producto
product = session.query(Product).filter_by(name='🍎 Manzana').first()
print(product)

# b) Consultar segundo producto
second_product_query = session.query(Product).filter_by(name='🍐 Pera').first()
print(second_product_query)

# Actualizar primer producto
product.name = '🍎 Manzana actualizada'
session.commit()

# c) Actualizar segundo producto
second_product_query.name = '🍐 Pera actualizada'
second_product_query.description = 'Pera verde 🟢 actualizada'
session.commit()

# Eliminar primer producto
session.delete(product)

# d) Eliminar segundo producto
session.delete(second_product_query)

session.commit()
session.close()
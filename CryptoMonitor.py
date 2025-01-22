import requests
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from flask import Flask, jsonify

class CryptoMonitor:
    def __init__(self, db_url, api_url):
        self.engine = create_engine(db_url)
        self.api_url = api_url

    def obtener_precios_criptomonedas(self):
        """Obtiene precios de criptomonedas desde la API."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()

            precios = [
                {'criptomoneda': crypto['name'], 'precio': crypto['current_price']}
                for crypto in data
            ]
            return pd.DataFrame(precios)
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return None

    def guardar_datos_en_db(self, df):
        """Guarda los datos obtenidos en la base de datos."""
        try:
            df.to_sql('precios_cripto', self.engine, if_exists='replace', index=False)
            print("Datos guardados exitosamente en la base de datos.")
        except Exception as e:
            print(f"Error al guardar datos en la base de datos: {e}")

    def obtener_datos_desde_db(self):
        """Obtiene los datos almacenados en la base de datos."""
        try:
            query = "SELECT criptomoneda, precio FROM precios_cripto"
            return pd.read_sql(query, self.engine)
        except Exception as e:
            print(f"Error al obtener datos desde la base de datos: {e}")
            return None

    def filtrar_datos(self, df):
        """Filtra las 10 criptomonedas con mayor precio."""
        try:
            df = df.dropna()
            df = df[df['precio'].apply(lambda x: isinstance(x, (int, float)))]
            df = df[df['precio'] >= 1]
            return df.sort_values(by='precio', ascending=False).head(10)
        except Exception as e:
            print(f"Error al filtrar datos: {e}")
            return None

    def crear_graficos(self, df):
        """Crea gráficos de línea y barras a partir de los datos filtrados."""
        try:
            # Gráfico de líneas
            plt.figure(figsize=(10, 6))
            plt.plot(df['criptomoneda'], df['precio'], marker='o')
            plt.title('Top 10 Criptomonedas por Precio - Gráfico de Línea')
            plt.xlabel('Criptomoneda')
            plt.ylabel('Precio (USD)')
            plt.xticks(rotation=45)
            plt.grid()
            plt.tight_layout()
            plt.show()

            # Gráfico de barras
            plt.figure(figsize=(10, 6))
            plt.bar(df['criptomoneda'], df['precio'], color='skyblue')
            plt.title('Top 10 Criptomonedas por Precio - Gráfico de Barras')
            plt.xlabel('Criptomoneda')
            plt.ylabel('Precio (USD)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error al crear gráficos: {e}")

# Configuración inicial
DB_URL = 'sqlite:///dbcripto_precios.db'
API_URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1'

crypto_monitor = CryptoMonitor(DB_URL, API_URL)

# Flask App
app = Flask(__name__)

# Parte 1: Obtener y guardar datos
df_precios = crypto_monitor.obtener_precios_criptomonedas()
if df_precios is not None:
    crypto_monitor.guardar_datos_en_db(df_precios)

# Parte 2: Extraer, filtrar y graficar datos
df_datos = crypto_monitor.obtener_datos_desde_db()
if df_datos is not None:
    df_filtrado = crypto_monitor.filtrar_datos(df_datos)
    if df_filtrado is not None:
        crypto_monitor.crear_graficos(df_filtrado)

@app.route('/api/actualizar', methods=['GET'])
def actualizar_datos():
    """Actualiza los datos desde la API y los guarda en la base de datos."""
    df = crypto_monitor.obtener_precios_criptomonedas()
    if df is not None:
        crypto_monitor.guardar_datos_en_db(df)
        return jsonify({"message": "Datos actualizados exitosamente"}), 200
    return jsonify({"message": "Error al actualizar datos"}), 500

@app.route('/api/cripto', methods=['GET'])
def obtener_datos_filtrados():
    """Obtiene las 10 criptomonedas con mayor precio desde la base de datos."""
    df = crypto_monitor.obtener_datos_desde_db()
    if df is not None:
        try:
            df_filtrado = crypto_monitor.filtrar_datos(df)
            return jsonify(df_filtrado.to_dict(orient='records')), 200
        except Exception as e:
            return jsonify({"message": f"Error al filtrar datos: {e}"}), 500
    return jsonify({"message": "Error al obtener datos"}), 500

if __name__ == '__main__':
    # Al iniciar la aplicación, se actualizan los datos automáticamente
    print("Actualizando datos iniciales...")
    df_precios = crypto_monitor.obtener_precios_criptomonedas()
    if df_precios is not None:
        crypto_monitor.guardar_datos_en_db(df_precios)
    app.run(debug=True)

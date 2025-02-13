import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import streamlit as st

df = pd.read_csv("data/vehicles_us.csv", na_values=['None', 'NA', 'NULL', ''],
                 keep_default_na=True, encoding='utf-8', on_bad_lines='skip', decimal='.', parse_dates=['date_posted'])

df['model_year'] = pd.to_numeric(df['model_year'], errors='coerce').fillna(0).astype(int)
df['cylinders'] = pd.to_numeric(df['cylinders'], errors='coerce').fillna(0).astype(int)
df['paint_color'] = df['paint_color'].fillna('Desconocido')
df['is_4wd'] = pd.to_numeric(df['is_4wd'], errors='coerce').fillna(0).astype(int)
df['odometer'] = pd.to_numeric(df['odometer'], errors='coerce').fillna(0).astype(int)

# Título
st.header('Visualización de Datos de Vehículos')

# Estadísticas y datos faltantes
df_filtrado_sin_ceros_y_nulos = df[df[['model_year','cylinders','odometer','is_4wd','price','date_posted','days_listed']].notna() & (df[['model_year','cylinders','odometer','is_4wd','price','date_posted','days_listed']] != 0)]

# Estadísticas y datos faltantes
st.write(df_filtrado_sin_ceros_y_nulos.describe())
# Muestra las primeras filas
st.write(df.head(10))

# Filtros para el precio
precio_min = st.slider('Selecciona el precio mínimo', 0, int(df['price'].max()), 0)
precio_max = st.slider('Selecciona el precio máximo', 0, int(df['price'].max()), int(df['price'].max()))

df_filtrado = df[(df['price'] >= precio_min) & (df['price'] <= precio_max)]
st.write(df_filtrado.head())

# Histograma de precios
if st.button('Mostrar Histograma de Precios Filtrado'):
    fig = px.histogram(df_filtrado, x='price', title='Histograma de Precios Filtrados')
    st.plotly_chart(fig)

# Gráfico de dispersión
if st.button('Mostrar Gráfico de Dispersión'):
    fig2 = px.scatter(df_filtrado, x='odometer', y='price', title='Precio vs Odómetro')
    st.plotly_chart(fig2)

# Gráfico de condición de los vehículos
if st.button('Mostrar Gráfico de Condición de Vehículos'):
    # Contamos la cantidad de vehículos por condición
    condition_counts = df['condition'].value_counts().reset_index()

    # Renombramos las columnas para hacerlas más claras
    condition_counts.columns = ['condition', 'count']

    # Creamos el gráfico de barras
    fig3 = px.bar(condition_counts, x='condition', y='count', title='Distribución de Condición de Vehículos')

    # Mostramos el gráfico en Streamlit
    st.plotly_chart(fig3)

# Descargar CSV de datos filtrados
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df_filtrado)
st.download_button(
    label="Descargar CSV de Datos Filtrados",
    data=csv,
    file_name='vehiculos_filtrados.csv',
    mime='text/csv',
)
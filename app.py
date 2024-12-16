from flask import Flask, render_template, request
import pandas as pd

# Crear la aplicación Flask
app = Flask(__name__)

# Crear el DataFrame compras_df
material = ['Estibas', 'Etiquetas', 'Cajas', 'Zunchos']
cantidad_necesaria = [100, 200, 150, 300]
cantidad_disponible = [60, 50, 120, 25]
fecha_compra = ['2024-12-10', '2024-12-15', '2024-12-20', '2024-12-25']
compras_data = {
    'Material': material,
    'Cantidad Necesaria': cantidad_necesaria,
    'Cantidad Disponible': cantidad_disponible,
    'Fecha de Compra': fecha_compra,
}

compras_df = pd.DataFrame(compras_data)
codigo_material_dict = {i + 1: material[i] for i in range(len(material))}
compras_df['Código del Material'] = [i + 1 for i in range(len(material))]

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para verificar stock
@app.route('/check_stock', methods=['POST'])
def check_stock():
    codigo_material = int(request.form['codigo_material'])
    # Buscar el material según el código
    if codigo_material in compras_df['Código del Material'].values:
        material_row = compras_df[compras_df['Código del Material'] == codigo_material].iloc[0]
        cantidad_disponible = material_row['Cantidad Disponible']
        # Verificar si hay stock
        if cantidad_disponible > 0:
            return f"El material {material_row['Material']} (Código {codigo_material}) tiene {cantidad_disponible} unidades en stock."
        else:
            return f"El material {material_row['Material']} (Código {codigo_material}) NO tiene unidades en stock."
    else:
        return "Código de material no válido."

if __name__ == '__main__':
    app.run(debug=True)

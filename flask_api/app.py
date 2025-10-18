# flask_api/app.py
from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'inventario.json'

def cargar_inventario():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_inventario(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def validar_fecha(fecha_str):
    if not fecha_str:
        return True
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(cargar_inventario())

@app.route('/productos/<int:id_producto>', methods=['GET'])
def obtener_producto(id_producto):
    productos = cargar_inventario()
    producto = next((p for p in productos if p['id'] == id_producto), None)
    if producto:
        return jsonify(producto)
    return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Cuerpo de la solicitud vacío'}), 400

    campos_requeridos = ['nombre', 'categoria', 'descripcion', 'precio', 'cantidad']
    for campo in campos_requeridos:
        if campo not in data or data[campo] == "":
            return jsonify({'error': f'El campo "{campo}" es obligatorio'}), 400

    try:
        precio = float(data['precio'])
        cantidad = int(data['cantidad'])
        if precio < 0 or cantidad < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': 'Precio o cantidad deben ser números válidos y no negativos'}), 400

    if 'fecha_vencimiento' in data and not validar_fecha(data['fecha_vencimiento']):
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400

    productos = cargar_inventario()
    nuevo_id = max([p['id'] for p in productos], default=0) + 1
    nuevo_producto = {
        'id': nuevo_id,
        'nombre': data['nombre'],
        'categoria': data['categoria'],
        'descripcion': data['descripcion'],
        'precio': precio,
        'cantidad': cantidad,
        'fecha_vencimiento': data.get('fecha_vencimiento') or None
    }
    productos.append(nuevo_producto)
    guardar_inventario(productos)
    return jsonify(nuevo_producto), 201

@app.route('/productos/<int:id_producto>', methods=['PUT'])
def actualizar_producto(id_producto):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Cuerpo de la solicitud vacío'}), 400

    productos = cargar_inventario()
    idx = None
    for i, p in enumerate(productos):
        if p['id'] == id_producto:
            idx = i
            break
    if idx is None:
        return jsonify({'error': 'Producto no encontrado'}), 404

    # Validar campos si están presentes
    if 'precio' in data:
        try:
            data['precio'] = float(data['precio'])
            if data['precio'] < 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'error': 'Precio inválido'}), 400

    if 'cantidad' in data:
        try:
            data['cantidad'] = int(data['cantidad'])
            if data['cantidad'] < 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'error': 'Cantidad inválida'}), 400

    if 'fecha_vencimiento' in data and not validar_fecha(data['fecha_vencimiento']):
        return jsonify({'error': 'Formato de fecha inválido'}), 400

    campos_actualizables = ['nombre', 'categoria', 'descripcion', 'precio', 'cantidad', 'fecha_vencimiento']
    for key in data:
        if key in campos_actualizables:
            productos[idx][key] = data[key]

    guardar_inventario(productos)
    return jsonify(productos[idx])

@app.route('/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    productos = cargar_inventario()
    nuevo_inventario = [p for p in productos if p['id'] != id_producto]
    if len(nuevo_inventario) == len(productos):
        return jsonify({'error': 'Producto no encontrado'}), 404
    guardar_inventario(nuevo_inventario)
    return jsonify({'mensaje': 'Producto eliminado correctamente'}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
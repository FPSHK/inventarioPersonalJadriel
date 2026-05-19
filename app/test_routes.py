from flask import Blueprint, request, jsonify
from app.models import db , Item

# Blueprint solo con endpoints de prueba para items
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def index():
    """
    Homepage
    """
    return '<h1> Corriendo en Modo de Prueba. </h1>'

@main.route('/items', methods=['GET'])
def listar_items():
    """
    Retorna la lista de items en JSON
    """
    items = Item.query.all()

    data = [
        {
            'id': item.id,
            'nombre': item.nombre,
            'categoria': item.categoria,
            'cantidad': item.cantidad,
            'precio_estimado': float(item.precio_estimado) if item.precio_estimado else None,
            'ubicacion': item.ubicacion,
            'fecha_adquisicion': item.fecha_adquisicion.isoformat() if item.fecha_adquisicion else None,
            'owner_id': item.owner_id
        }
        for item in items
    ]
    return jsonify(data), 200

@main.route('/items/<int:id>', methods=['GET'])
def listar_un_item(id):
    """
    Retorna un solo item por su ID en JSON
    """
    item = Item.query.get_or_404(id)

    data = {
        'id': item.id,
        'nombre': item.nombre,
        'categoria': item.categoria,
        'cantidad': item.cantidad,
        'precio_estimado': float(item.precio_estimado) if item.precio_estimado else None, #Lo converti a float para que sea JSON friendly
        'ubicacion': item.ubicacion,
        'fecha_adquisicion': item.fecha_adquisicion.isoformat() if item.fecha_adquisicion else None, # Lo hize JSON friendly igual
        'owner_id': item.owner_id
    }

    return jsonify(data), 200

@main.route('/items', methods=['POST'])
def crear_item():
    """
    Crea un item sin validacion.
    Espera JSON con los campos del item y 'owner_id
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    item = Item(
        nombre=data.get('nombre'),
        categoria=data.get('categoria'),
        cantidad=data.get('cantidad'),
        precio_estimado=data.get('precio_estimado'),
        ubicacion=data.get('ubicacion'),
        fecha_adquisicion=data.get('fecha_adquisicion'),
        owner_id=data.get('owner_id')
    )

    db.session.add(item)
    db.session.commit()

    return jsonify ({'message': 'Item creado', 'id' : item.id, 'owner_id': item.owner_id}), 201

@main.route('/items/<int:id>', methods=['PUT'])
def actualizar_item(id):
    """
    Actualiza un item sin validacion de usuario o permisos
    """
    item = Item.query.get_or_404(id)
    data = request.get_json()

    item.nombre = data.get('nombre', item.nombre)
    item.categoria = data.get('categoria', item.categoria)
    item.cantidad = data.get('cantidad', item.cantidad)
    item.precio_estimado = data.get ('precio_estimado', item.precio_estimado)
    item.ubicacion = data.get ('ubicacion', item.ubicacion)
    item.fecha_adquisicion = data.get ('fecha_adquisicion', item.fecha_adquisicion)
    item.owner_id = data.get ('owner_id', item.owner_id)

    db.session.commit()

    return jsonify({'message': 'Item actualizado', 'id': item.id}), 200

@main.route('/items/<int:id>', methods=['DELETE'])
def eliminar_item(id):
    """
    Elimina un item sin validacion de permisos
    """

    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item eliminado', 'id' : item.id}), 200
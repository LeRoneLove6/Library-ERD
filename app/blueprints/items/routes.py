from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Item
from . import items_bp
from app.extensions import db
from .schemas import item_schema, items_schema

# -----------------------
# CREATE ITEM
# -----------------------
@items_bp.route('/', methods=['POST'])
def create_item():
    try:
        # Marshmallow returns an Item instance directly
        new_item = item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(new_item)
    db.session.commit()
    return item_schema.jsonify(new_item), 201

# -----------------------
# GET ALL ITEMS
# -----------------------
@items_bp.route('/', methods=['GET'])
def get_all_items():
    items = db.session.execute(select(Item)).scalars().all()
    return items_schema.jsonify(items), 200

# -----------------------
# GET ITEM BY ID
# -----------------------
@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = db.session.get(Item, item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return item_schema.jsonify(item), 200

# -----------------------
# UPDATE ITEM
# -----------------------
@items_bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = db.session.get(Item, item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    try:
        # load_instance=True + partial=True returns an Item instance with updated fields
        updated_item = item_schema.load(request.json, instance=item, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return item_schema.jsonify(updated_item), 200

# -----------------------
# DELETE ITEM
# -----------------------
@items_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = db.session.get(Item, item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200

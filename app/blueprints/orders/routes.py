from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Order, OrderItems, db
from . import orders_bp
from .schemas import create_order_schema, order_schema, receipt_schema

@orders_bp.route("/", methods=["POST"])
def create_order():
   
    try:
        order_data = create_order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    
    new_order = Order(member_id=order_data["member_id"])

    
    for item in order_data["item_quant"]:
        order_item = OrderItems(
            item_id=item["item_id"],
            quantity=item["item_quant"]
        )
        new_order.order_items.append(order_item)

    
    db.session.add(new_order)
    db.session.commit()


    receipt = order_schema.dump(new_order)
    return jsonify(receipt), 201

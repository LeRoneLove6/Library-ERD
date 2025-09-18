from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.extensions import ma
from app.models import Order, OrderItems



class ReceiptSchema(ma.Schema):

    total = fields.Float(required=True)
    order = fields.Nested("OrderSchema")


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_relationships = True


    order_items = fields.Nested("OrderItemSchema", exclude=['id'], many=True)
    order_date = fields.Date()
    total_price = fields.Method("get_total_price")

    def get_total_price(self, obj):
        return obj.total_price

class OrderItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItems
        include_fk = True
        load_instance = True
    item = fields.Nested("ItemSchema", exclude=["id"])


class CreateOrderSchema(ma.Schema):
   member_id = fields.Int(required=True)
   item_quant = fields.Nested("ItemQuantitySchema", many=True)

class ItemQuantitySchema(ma.Schema):
    item_id = fields.Int(required=True)
    item_quant = fields.Int(required=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
create_order_schema = CreateOrderSchema()
receipt_schema = ReceiptSchema()
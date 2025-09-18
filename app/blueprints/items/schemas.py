from app.extensions import ma
from app.models import Item




class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
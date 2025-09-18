from app.extensions import ma
from app.models import Loan
from marshmallow import fields

class LoanSchema(ma.SQLAlchemyAutoSchema):
    books = fields.Nested('BookSchema', many=True)
    member = fields.Nested('MemberSchema')
    book_ids = fields.Method("get_book_ids")
    member_id = fields.Int(load_only=True)

    class Meta:
        model = Loan
        load_instance = True
        include_relationships = True
        fields = ("id", "book_ids", "loan_date", "member_id", "books", "member")
       

    def get_book_ids(self, obj):
        return [book.id for book in obj.books]

class EditLoanSchema(ma.Schema):
    add_book_ids = fields.List(fields.Int(), required=True)
    remove_book_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_book_ids", "remove_book_ids")

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)
return_loans_schema = LoanSchema(exclude=["member_id"])
edit_loan_schema = EditLoanSchema()


from app.extensions import ma
from app.models import LoanBook

class LoanBookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LoanBook
        load_instance = True
        include_fk = True   # ensures loan_id and book_id show up

loan_book_schema = LoanBookSchema()
loan_books_schema = LoanBookSchema(many=True)

from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import db, Book, Loan
from .schemas import loan_schema, loans_schema, return_loans_schema, edit_loan_schema

loans_bp = Blueprint("loans", __name__, url_prefix="/loans")


# CREATE a new loan with book_ids
@loans_bp.route("/", methods=["POST"])
def create_loan():
    data = request.json or {}
    book_ids = data.pop("book_ids", [])

    try:
        # Load loan data without books first
        loan = loan_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Attach books if book_ids provided
    for book_id in book_ids:
        book = db.session.get(Book, book_id)
        if book:
            loan.books.append(book)

    db.session.add(loan)
    db.session.commit()
    return loan_schema.jsonify(loan), 201


# READ ALL loans
@loans_bp.route("/", methods=["GET"])
def get_loans():
    all_loans = db.session.execute(select(Loan)).scalars().all()
    return loans_schema.jsonify(all_loans)




# DELETE a loan
@loans_bp.route("/<int:id>", methods=["DELETE"])
def delete_loan(id):
    loan = db.session.get(Loan, id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 400

    db.session.delete(loan)
    db.session.commit()
    return jsonify({"message": "Loan deleted successfully"}), 200


# EDIT a loan
@loans_bp.route("/<int:id>", methods=["PUT"])
def edit_loan(id):
    try:
        loan_edits = edit_loan_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Loan).where(Loan.id == id)
    loan = db.session.execute(query).scalars().first()

    for book_id in loan_edits['add_book_ids']:
        query = select(Book).where(Book.id == book_id)
        book = db.session.execute(query).scalars().first()

        if book and book not in loan.books:
            loan.books.append(book)

    for book_id in loan_edits['remove_book_ids']:
        query = select(Book).where(Book.id == book_id)
        book = db.session.execute(query).scalars().first()

        if book and book in loan.books:
            loan.books.remove(book)

    db.session.commit()
    return return_loans_schema.jsonify(loan), 201

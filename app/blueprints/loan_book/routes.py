from flask import request, jsonify, Blueprint
from app.models import db, Loan, Book

loan_books_bp = Blueprint("loan_books", __name__, url_prefix="/loan_books")

# ADD a book to a loan
@loan_books_bp.route("/<int:loan_id>/books/<int:book_id>", methods=["POST"])
def add_book_to_loan(loan_id, book_id):
    loan = db.session.get(Loan, loan_id)
    book = db.session.get(Book, book_id)

    if not loan or not book:
        return jsonify({"error": "Loan or Book not found"}), 404

    if book in loan.books:
        return jsonify({"message": "Book already in loan"}), 400

    loan.books.append(book)
    db.session.commit()
    return jsonify({"message": "Book added to loan successfully"}), 201

# REMOVE a book from a loan
@loan_books_bp.route("/<int:loan_id>/books/<int:book_id>", methods=["DELETE"])
def remove_book_from_loan(loan_id, book_id):
    loan = db.session.get(Loan, loan_id)
    book = db.session.get(Book, book_id)

    if not loan or not book:
        return jsonify({"error": "Loan or Book not found"}), 404

    if book not in loan.books:
        return jsonify({"message": "Book not in loan"}), 400

    loan.books.remove(book)
    db.session.commit()
    return jsonify({"message": "Book removed from loan successfully"}), 200

# LIST books in a loan
@loan_books_bp.route("/<int:loan_id>/books", methods=["GET"])
def list_books_in_loan(loan_id):
    loan = db.session.get(Loan, loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404

    books = [{"id": b.id, "title": b.title} for b in loan.books]
    return jsonify(books), 200

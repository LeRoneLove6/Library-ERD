from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, delete
from app.models import db, Book
from .schemas import book_schema, books_schema
from . import books_bp


@books_bp.route("/", methods=["POST"])
def create_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(book_data)
    db.session.commit()
    return book_schema.jsonify(book_data), 201

# GET /books/
@books_bp.route("/", methods=["GET"])
def get_books():
    all_books = db.session.execute(select(Book)).scalars().all()
    return books_schema.jsonify(all_books)

# GET /books/<id>
@books_bp.route("/<int:id>", methods=["GET"])
def get_book(id):
    book = db.session.get(Book, id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return book_schema.jsonify(book)

# PUT /books/<id>
@books_bp.route("/<int:id>", methods=["PUT"])
def update_book(id):
    book = db.session.get(Book, id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    try:
        updated_data = book_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in request.json.items():
        setattr(book, key, value)

    db.session.commit()
    return book_schema.jsonify(book)

# DELETE /books/<id>
@books_bp.route("/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = db.session.get(Book, id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200


@books_bp.route("/popular", methods=["GET"])
def get_popular_books():
    query = select(book)
    books = db.session.execute(query).scalars().all()

    books.sort(key= lambda book: len(book.loans) , reverse=True )

    return books_schema.jsonify(books)


@books_bp.route("/search", methods=["GET"])
def search_book():
    title = request.args.get("title")

    query = select(Book).where(Book.title.like(f'%{title}%'))
    books = db.session.execute(query).scalars().all()

    return books_schema.jsonify(books)
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from app.extensions import db

# Association table for many-to-many relationship between Loan and Book
loan_book = db.Table(
    'loan_book',
    db.metadata,
    db.Column('loan_id', db.Integer, db.ForeignKey('loans.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
)


class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(360), nullable=False, unique=True)
    DOB = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    loans = db.relationship('Loan', back_populates='member')
    orders = db.relationship('Order', back_populates='member')


class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    loan_date = db.Column(db.Date, default=date.today)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))

    member = db.relationship('Member', back_populates='loans')
    books = db.relationship('Book', secondary=loan_book, back_populates='loans')


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)

    loans = db.relationship('Loan', secondary=loan_book, back_populates='books')


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    order_items = db.relationship('OrderItems', back_populates='item')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, default=date.today)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))

    member = db.relationship('Member', back_populates='orders')
    order_items = db.relationship('OrderItems', back_populates='order')

    @property
    def total_price(self):
      return sum(oi.quantity * oi.item.price for oi in self.order_items)


class OrderItems(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', back_populates='order_items')
    item = db.relationship('Item', back_populates='order_items')

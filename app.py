from app import SWAGGER_URL, create_app, swaggerui_blueprint
from app.extensions import db, ma , limiter, cache
from app.models import Book, Member, Loan,  Item
from app.blueprints.books import books_bp
from app.blueprints.members import members_bp
from app.blueprints.loans import loans_bp
from app.blueprints.loan_book import loan_books_bp
from app.blueprints.items import items_bp
from app.blueprints.orders import orders_bp


app = create_app("DevelopmentConfig")

# Register your blueprints
#app.register_blueprint(books_bp)    # /books/ routes
#app.register_blueprint(members_bp)  # /members/ routes
#app.register_blueprint(loans_bp)    # /loans/ routes
#app.register_blueprint(loan_books_bp)  # /loan_books/ routes
#app.register_blueprint(items_bp)    # /items/ routes
#app.register_blueprint(orders_bp)   # /orders/ routes
#app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) #Registering our swagger blueprint


# Create database tables
with app.app_context():
    # db.drop_all()
    db.create_all()

# Run the Flask development server
if __name__ == "__main__":
    #print(app.url_map)
    app.run()

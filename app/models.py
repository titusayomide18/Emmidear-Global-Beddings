# app/models.py - main SQLAlchemy models
from flask_login import UserMixin
from .extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship("Product", backref="category", lazy="dynamic")

    def __repr__(self):
        return f"<Category {self.name}>"

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False)
    sku = db.Column(db.String(80), unique=True, nullable=True)
    description_short = db.Column(db.String(400))
    description_long = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)  # store in smallest unit or Naira integer
    currency = db.Column(db.String(10), default="NGN")
    stock = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    images = db.relationship("ProductImage", backref="product", lazy="dynamic")

    def price_display(self):
        # simple display helper (adjust if you store kobo)
        return f"₦{self.price:,}"

    def __repr__(self):
        return f"<Product {self.name}>"

class ProductImage(db.Model):
    __tablename__ = "product_images"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    alt_text = db.Column(db.String(300), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)

    def url(self):
        # in production you'd use S3 url; for dev we serve from /static/uploads/
        return f"/static/uploads/{self.filename}"

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200))
    phone = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # UserMixin provides: is_authenticated, is_active, is_anonymous, get_id()

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    total = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="pending")
    payment_method = db.Column(db.String(50), default="COD")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("OrderItem", backref="order", lazy="dynamic")

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String(200))
    qty = db.Column(db.Integer)
    price_each = db.Column(db.Integer)

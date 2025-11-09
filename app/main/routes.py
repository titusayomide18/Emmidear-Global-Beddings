# app/main/routes.py
from flask import render_template, abort
from . import bp
from app.models import Product, Category


@bp.route("/")
def index():
    # fetch featured products
    featured = Product.query.filter_by(featured=True).limit(6).all()
    # ensure images relationship is a plain list for templates
    for p in featured:
        try:
            # if relationship returns a query object (lazy='dynamic'), call .all()
            if hasattr(p.images, "all"):
                p._images = p.images.all()
            else:
                # p.images might already be a list-like collection
                p._images = list(p.images)
        except Exception:
            p._images = []
    categories = Category.query.limit(10).all()
    return render_template("index.html", featured=featured, categories=categories)


@bp.route("/product/<slug>")
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first()
    if not product:
        abort(404)
    # materialize images similarly
    try:
        if hasattr(product.images, "all"):
            product._images = product.images.all()
        else:
            product._images = list(product.images)
    except Exception:
        product._images = []
    categories = Category.query.limit(10).all()
    return render_template(
        "product_detail.html", product=product, categories=categories
    )

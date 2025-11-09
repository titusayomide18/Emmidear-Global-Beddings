from flask import jsonify, request
from . import bp
from ..models import Product, Category
from ..extensions import db

@bp.route("/categories", methods=["GET"])
def get_categories():
    cats = Category.query.all()
    data = [{"id": c.id, "name": c.name, "slug": c.slug} for c in cats]
    return jsonify(data)

@bp.route("/products", methods=["GET"])
def get_products():
    # simple query: supports ?featured=true or ?category=slug
    q = Product.query
    if request.args.get("featured") == "true":
        q = q.filter_by(featured=True)
    cat_slug = request.args.get("category")
    if cat_slug:
        # join category
        q = q.join(Category).filter(Category.slug == cat_slug)
    products = q.limit(100).all()
    result = []
    for p in products:
        images = [img.url() for img in p.images.limit(3).all()]
        result.append({
            "id": p.id,
            "name": p.name,
            "slug": p.slug,
            "price": p.price,
            "currency": p.currency,
            "stock": p.stock,
            "images": images,
        })
    return jsonify(result)

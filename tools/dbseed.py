# tools/dbseed.py
from app import create_app
from app.extensions import db
from app.models import Category, Product, ProductImage

app = create_app()
with app.app_context():
    # 1) Create categories if missing
    cat = Category.query.filter_by(slug="duvets").first()
    if not cat:
        cat = Category(name="Duvets", slug="duvets")
        db.session.add(cat)
        db.session.commit()
        print("Created category: Duvets")

    # 2) Create a product if missing
    prod = Product.query.filter_by(slug="soft-duvet").first()
    if not prod:
        prod = Product(
            name="Soft Duvet",
            slug="soft-duvet",
            sku="EMM-SD-001",
            description_short="Cozy soft duvet perfect for 4-season comfort.",
            description_long="Premium microfiber fill, breathable cover, machine washable.",
            price=30000,
            currency="NGN",
            stock=15,
            featured=True,
            category_id=cat.id
        )
        db.session.add(prod)
        db.session.commit()
        print("Created product: Soft Duvet")

    # 3) Add a product image row referencing the file in static/uploads/product-pics/
    # Change filename below to match the actual file you placed in app/static/uploads/product-pics/
    filename = "Throw-Pillows-a.jpg"   # <-- CHANGE THIS to your actual filename
    existing = ProductImage.query.filter_by(product_id=prod.id, filename=filename).first()
    if not existing:
        img = ProductImage(product_id=prod.id, filename=filename, is_primary=True)
        db.session.add(img)
        db.session.commit()
        print("Added image record:", filename)
    else:
        print("Image record already exists:", filename)

    print("Seeding complete.")
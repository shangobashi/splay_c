"""Seed product database with sample furniture."""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.database import SessionLocal
from app.models.product import Product
from app.services.matching import generate_stub_embedding


SAMPLE_PRODUCTS = [
    # Sofas
    {"name": "Harmony Sofa", "brand": "West Elm", "category": "sofa", "price": 1499.00, "retailer": "West Elm"},
    {"name": "Modern Sectional", "brand": "Wayfair", "category": "sofa", "price": 899.00, "retailer": "Wayfair"},
    {"name": "Velvet Chesterfield", "brand": "CB2", "category": "sofa", "price": 1799.00, "retailer": "CB2"},
    {"name": "Mid-Century Sofa", "brand": "Article", "category": "sofa", "price": 1299.00, "retailer": "Article"},
    {"name": "Sleeper Sofa", "brand": "IKEA", "category": "sofa", "price": 599.00, "retailer": "IKEA"},
    {"name": "L-Shaped Sectional", "brand": "Wayfair", "category": "sofa", "price": 1099.00, "retailer": "Wayfair"},
    {"name": "Leather Sofa", "brand": "West Elm", "category": "sofa", "price": 2199.00, "retailer": "West Elm"},
    {"name": "Modular Sofa", "brand": "Floyd", "category": "sofa", "price": 1895.00, "retailer": "Floyd"},
    {"name": "Linen Sofa", "brand": "Pottery Barn", "category": "sofa", "price": 1599.00, "retailer": "Pottery Barn"},
    {"name": "Tufted Sofa", "brand": "CB2", "category": "sofa", "price": 1399.00, "retailer": "CB2"},

    # Coffee Tables
    {"name": "Glass Coffee Table", "brand": "West Elm", "category": "coffee_table", "price": 399.00, "retailer": "West Elm"},
    {"name": "Wooden Coffee Table", "brand": "IKEA", "category": "coffee_table", "price": 199.00, "retailer": "IKEA"},
    {"name": "Marble Coffee Table", "brand": "CB2", "category": "coffee_table", "price": 699.00, "retailer": "CB2"},
    {"name": "Round Coffee Table", "brand": "Article", "category": "coffee_table", "price": 449.00, "retailer": "Article"},
    {"name": "Storage Coffee Table", "brand": "Wayfair", "category": "coffee_table", "price": 299.00, "retailer": "Wayfair"},
    {"name": "Industrial Coffee Table", "brand": "West Elm", "category": "coffee_table", "price": 549.00, "retailer": "West Elm"},
    {"name": "Nesting Coffee Tables", "brand": "CB2", "category": "coffee_table", "price": 399.00, "retailer": "CB2"},
    {"name": "Lift-Top Coffee Table", "brand": "Wayfair", "category": "coffee_table", "price": 329.00, "retailer": "Wayfair"},

    # Floor Lamps
    {"name": "Arc Floor Lamp", "brand": "West Elm", "category": "floor_lamp", "price": 299.00, "retailer": "West Elm"},
    {"name": "Tripod Floor Lamp", "brand": "IKEA", "category": "floor_lamp", "price": 89.00, "retailer": "IKEA"},
    {"name": "LED Floor Lamp", "brand": "CB2", "category": "floor_lamp", "price": 349.00, "retailer": "CB2"},
    {"name": "Reading Floor Lamp", "brand": "Article", "category": "floor_lamp", "price": 199.00, "retailer": "Article"},
    {"name": "Modern Floor Lamp", "brand": "Wayfair", "category": "floor_lamp", "price": 159.00, "retailer": "Wayfair"},
    {"name": "Brass Floor Lamp", "brand": "West Elm", "category": "floor_lamp", "price": 399.00, "retailer": "West Elm"},
    {"name": "Corner Floor Lamp", "brand": "CB2", "category": "floor_lamp", "price": 279.00, "retailer": "CB2"},

    # Table Lamps
    {"name": "Ceramic Table Lamp", "brand": "West Elm", "category": "table_lamp", "price": 129.00, "retailer": "West Elm"},
    {"name": "Modern Table Lamp", "brand": "IKEA", "category": "table_lamp", "price": 49.00, "retailer": "IKEA"},
    {"name": "Marble Base Lamp", "brand": "CB2", "category": "table_lamp", "price": 179.00, "retailer": "CB2"},
    {"name": "Brass Table Lamp", "brand": "Article", "category": "table_lamp", "price": 149.00, "retailer": "Article"},
    {"name": "Touch Table Lamp", "brand": "Wayfair", "category": "table_lamp", "price": 79.00, "retailer": "Wayfair"},
    {"name": "USB Table Lamp", "brand": "West Elm", "category": "table_lamp", "price": 99.00, "retailer": "West Elm"},

    # Dining Tables
    {"name": "Wooden Dining Table", "brand": "West Elm", "category": "dining_table", "price": 899.00, "retailer": "West Elm"},
    {"name": "Glass Dining Table", "brand": "IKEA", "category": "dining_table", "price": 399.00, "retailer": "IKEA"},
    {"name": "Marble Dining Table", "brand": "CB2", "category": "dining_table", "price": 1299.00, "retailer": "CB2"},
    {"name": "Extendable Dining Table", "brand": "Article", "category": "dining_table", "price": 999.00, "retailer": "Article"},
    {"name": "Round Dining Table", "brand": "Wayfair", "category": "dining_table", "price": 599.00, "retailer": "Wayfair"},
    {"name": "Farmhouse Dining Table", "brand": "Pottery Barn", "category": "dining_table", "price": 1199.00, "retailer": "Pottery Barn"},

    # Chairs
    {"name": "Dining Chair Set", "brand": "West Elm", "category": "chair", "price": 599.00, "retailer": "West Elm"},
    {"name": "Accent Chair", "brand": "IKEA", "category": "chair", "price": 199.00, "retailer": "IKEA"},
    {"name": "Velvet Accent Chair", "brand": "CB2", "category": "chair", "price": 499.00, "retailer": "CB2"},
    {"name": "Office Chair", "brand": "Article", "category": "chair", "price": 349.00, "retailer": "Article"},
    {"name": "Dining Chairs (Set of 4)", "brand": "Wayfair", "category": "chair", "price": 399.00, "retailer": "Wayfair"},
    {"name": "Armchair", "brand": "West Elm", "category": "chair", "price": 699.00, "retailer": "West Elm"},
    {"name": "Folding Chairs", "brand": "IKEA", "category": "chair", "price": 79.00, "retailer": "IKEA"},

    # Side Tables
    {"name": "Nightstand", "brand": "West Elm", "category": "side_table", "price": 299.00, "retailer": "West Elm"},
    {"name": "End Table", "brand": "IKEA", "category": "side_table", "price": 99.00, "retailer": "IKEA"},
    {"name": "Marble Side Table", "brand": "CB2", "category": "side_table", "price": 349.00, "retailer": "CB2"},
    {"name": "Nesting Tables", "brand": "Article", "category": "side_table", "price": 249.00, "retailer": "Article"},
    {"name": "C-Table", "brand": "Wayfair", "category": "side_table", "price": 129.00, "retailer": "Wayfair"},
    {"name": "Drawer Nightstand", "brand": "West Elm", "category": "side_table", "price": 399.00, "retailer": "West Elm"},

    # Pendant Lights
    {"name": "Globe Pendant", "brand": "West Elm", "category": "pendant_light", "price": 199.00, "retailer": "West Elm"},
    {"name": "Industrial Pendant", "brand": "IKEA", "category": "pendant_light", "price": 79.00, "retailer": "IKEA"},
    {"name": "Glass Pendant", "brand": "CB2", "category": "pendant_light", "price": 249.00, "retailer": "CB2"},
    {"name": "Multi-Light Pendant", "brand": "Article", "category": "pendant_light", "price": 399.00, "retailer": "Article"},
    {"name": "Drum Pendant", "brand": "Wayfair", "category": "pendant_light", "price": 159.00, "retailer": "Wayfair"},
    {"name": "Chandelier", "brand": "Pottery Barn", "category": "pendant_light", "price": 599.00, "retailer": "Pottery Barn"},
]


def seed_products():
    """Seed product database with sample furniture."""
    db = SessionLocal()

    try:
        # Check if products already exist
        existing_count = db.query(Product).count()
        if existing_count > 0:
            print(f"[!] Database already has {existing_count} products.")
            response = input("Delete and reseed? (yes/no): ")
            if response.lower() != "yes":
                print("Cancelled.")
                return

            # Delete existing products
            db.query(Product).delete()
            db.commit()
            print(f"[OK] Deleted {existing_count} existing products.")

        # Create products
        print(f"Creating {len(SAMPLE_PRODUCTS)} products...")

        for idx, data in enumerate(SAMPLE_PRODUCTS, start=1):
            # Generate embedding based on product name + category
            embedding_text = f"{data['category']} {data['name']} {data['brand']}"
            embedding_vector = generate_stub_embedding(embedding_text)

            product = Product(
                external_id=f"prod_{idx:03d}",
                name=data["name"],
                brand=data["brand"],
                category=data["category"],
                price=data["price"],
                currency="USD",
                description=f"{data['brand']} {data['name']} - High quality furniture piece",
                dimensions={"width": 80, "height": 90, "depth": 40},
                colors=["Gray", "Beige", "Navy"],
                materials=["Wood", "Fabric"],
                image_url=f"https://via.placeholder.com/400x400?text={data['name'].replace(' ', '+')}",
                images=[],
                affiliate_url=f"https://{data['retailer'].lower().replace(' ', '')}.com/{data['name'].lower().replace(' ', '-')}?ref=splay",
                retailer_url=f"https://{data['retailer'].lower().replace(' ', '')}.com/{data['name'].lower().replace(' ', '-')}",
                retailer_name=data["retailer"],
                embedding={"vector": embedding_vector},
                in_stock=True
            )

            db.add(product)

            if idx % 10 == 0:
                print(f"  Created {idx}/{len(SAMPLE_PRODUCTS)} products...")

        db.commit()
        print(f"[OK] Successfully created {len(SAMPLE_PRODUCTS)} products!")

        # Show summary by category
        print("\nProducts by category:")
        for category in ["sofa", "coffee_table", "floor_lamp", "table_lamp", "dining_table", "chair", "side_table", "pendant_light"]:
            count = db.query(Product).filter(Product.category == category).count()
            print(f"  {category}: {count}")

    except Exception as e:
        print(f"[ERROR] Error seeding products: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print(" Splay Product Seeder")
    print("=" * 50)
    print()
    seed_products()
    print()
    print("Done!")

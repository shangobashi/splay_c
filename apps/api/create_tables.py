"""Create database tables using SQLAlchemy."""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.database import Base, engine
from app.models import User, Subscription, Scan, DetectedItem, ItemMatch, Product

def create_tables():
    """Create all database tables."""
    print("=" * 50)
    print(" Creating Database Tables")
    print("=" * 50)
    print()

    try:
        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("[OK] All tables created successfully!")

        # Show created tables
        print("\nCreated tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")

    except Exception as e:
        print(f"[ERROR] Error creating tables: {e}")
        raise

    print()
    print("Done!")


if __name__ == "__main__":
    create_tables()

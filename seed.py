"""Seed file for resetting/creating the database."""

from app import app, db


def seed_database():
    """
    Seed the database by dropping all existing tables and creating new ones.
    """
    try:
        with app.app_context():
            # Drop all existing tables
            db.drop_all()

            # Create new tables
            db.create_all()

        print("Database seeded successfully.")

    except Exception as e:
        print(f"Error seeding database: {str(e)}")


# Call the seed_database function to seed the database
if __name__ == "__main__":
    seed_database()

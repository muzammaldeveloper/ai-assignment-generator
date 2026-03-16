"""
Create demo user for local testing.

Usage: python scripts/seed_db.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.factory import create_app
from app.extensions import db
from app.models.user import User


def seed():
    app = create_app()
    with app.app_context():
        if User.query.filter_by(email="demo@example.com").first():
            print("✅ Demo user already exists!")
            return

        user = User(name="Demo User", email="demo@example.com")
        user.set_password("DemoPass123")
        db.session.add(user)
        db.session.commit()

        print("✅ Demo user created:")
        print(f"   Email:    demo@example.com")
        print(f"   Password: DemoPass123")
        print(f"   ID:       {user.id}")


if __name__ == "__main__":
    seed()
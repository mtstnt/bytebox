from sqlalchemy.orm import Session
import bcrypt
from bytebox.config.database import get_database
from bytebox.users.models import UserModel

def seed_users(db: Session):
    """Seed the database with initial user accounts."""
    # Check if users already exist
    existing_users = db.query(UserModel).count()
    if existing_users > 0:
        print("Users already exist, skipping seed.")
        return
    
    # Define seed users
    seed_data = [
        {
            "email": "admin@bytebox.com",
            "username": "admin",
            "password": "admin123"
        },
        {
            "email": "user@bytebox.com",
            "username": "user",
            "password": "user123"
        },
        {
            "email": "test@bytebox.com",
            "username": "testuser",
            "password": "test123"
        }
    ]
    
    # Create users with hashed passwords
    for user_data in seed_data:
        # Hash the password using bcrypt
        password_bytes = user_data["password"].encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        
        # Create user model
        user = UserModel(
            email=user_data["email"],
            username=user_data["username"],
            password=hashed_password.decode('utf-8')
        )
        
        db.add(user)
    
    db.commit()
    print(f"Successfully seeded {len(seed_data)} users.")


def seed_database(db: Session):
    """Main seeding function to seed all tables."""
    print("Starting database seeding...")
    seed_users(db)
    print("Database seeding completed.")
    
conn = get_database()
seed_database(next(conn))

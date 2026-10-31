import sys
from app.core.database import Base, engine
from app.seed import seed_db

def reset_db():
    print("WARNING: This will destroy all application data including users, submissions, and bookmarks.")
    confirm = input("Are you sure you want to proceed? (y/N): ")
    if confirm.lower() != 'y':
        print("Reset aborted.")
        return
        
    print("Force resetting database...")
    Base.metadata.drop_all(bind=engine)
    print("Database schema dropped. Re-seeding...")
    seed_db()
    print("Database reset completed successfully!")

if __name__ == "__main__":
    reset_db()

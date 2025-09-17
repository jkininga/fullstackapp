# seed.py
from app import app, db
from models import User, Project

def seed():
    with app.app_context():
        print("Clearing old data...")
        db.drop_all()
        db.create_all()

        print("Seeding users...")
        user1 = User(username="alice", email="alice@example.com")
        user1.set_password("password123")

        user2 = User(username="bob", email="bob@example.com")
        user2.set_password("password123")

        db.session.add_all([user1, user2])
        db.session.commit()

        print("Seeding projects...")
        project1 = Project(name="AI Assistant")
        project2 = Project(name="Recipe App")

        # Link users to projects (since you’ve got the many-to-many)
        project1.users.append(user1)
        project2.users.append(user2)

        db.session.add_all([project1, project2])
        db.session.commit()

        print("Done seeding!")

if __name__ == "__main__":
    seed()

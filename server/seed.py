#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Article, User

fake = Faker()

with app.app_context():

    print("🔄 Deleting all records...")
    Article.query.delete()
    User.query.delete()

    print("👤 Creating users...")
    users = []
    usernames = []

    for _ in range(25):
        username = fake.first_name()

        # Ensure usernames are unique
        while username in usernames:
            username = fake.first_name()

        usernames.append(username)

        user = User(username=username)
        users.append(user)

    db.session.add_all(users)

    print("📝 Creating articles...")
    articles = []

    for _ in range(100):
        content = fake.paragraph(nb_sentences=8)
        preview = content[:25] + '...'

        article = Article(
            author=fake.name(),
            title=fake.sentence(),
            content=content,
            preview=preview,
            minutes_to_read=randint(1, 20),
            is_member_only=rc([True, False, False])  # ~33% chance
        )

        articles.append(article)

    db.session.add_all(articles)

    # ✅ Ensure there's at least one member-only article
    if not any(article.is_member_only for article in articles):
        print("🔐 No member-only article found. Adding one manually.")
        member_article = Article(
            author=fake.name(),
            title="Exclusive Member Article",
            content="This is content only members can read.",
            preview="Exclusive preview...",
            minutes_to_read=5,
            is_member_only=True
        )
        db.session.add(member_article)

    db.session.commit()
    print("✅ Done seeding.")


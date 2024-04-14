# from app.models.manageDB import DatabaseManager
from app.models.discord_webhook import ArticleSender

def main():
    # Database settings
    db_settings = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "s91062013",
        "db": "JLPT",
        "charset": "utf8"
    }

    # Create an ArticleSender instance
    # article_sender = ArticleSender(db_manager, 'N4')
    # test mode  
    article_sender = ArticleSender('N4', db_settings, test_mode=True)
    article_sender.send_article()

if __name__ == "__main__":
    main()
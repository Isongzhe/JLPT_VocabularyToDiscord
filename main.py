from apscheduler.schedulers.blocking import BlockingScheduler
from app.models.vocab import Vocab
from app.models.discord_webhook import DiscordNotifier

def send_word():
    word = Vocab.get_random_word()
    message = f"{word.kanji} ({word.hiragana}): {word.chinese}"
    notifier = DiscordNotifier()
    notifier.send_message(message)
    word.delete_instance()

if __name__ == "__main__":
    Vocab.initialize()
    scheduler = BlockingScheduler()
    scheduler.add_job(send_word, 'interval', hours=24)
    scheduler.start()
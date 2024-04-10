from peewee import *

db = SqliteDatabase('JLPT.db')

class Vocab(Model):
    kanji = CharField()
    hiragana = CharField()
    chinese = CharField()

    class Meta:
        database = db

    @classmethod
    def initialize(cls):
        db.connect()
        db.create_tables([cls])

    @classmethod
    def add_word(cls, kanji, hiragana, chinese):
        cls.create(kanji=kanji, hiragana=hiragana, chinese=chinese)

    @classmethod
    def get_random_word(cls):
        return cls.select().order_by(fn.Random()).get()
import unittest
import sys
sys.path.append('D:/GitHub/JLPT_VocabularyToDiscord')
from app.utils.translator import translate_to_chinese, split_hiragana_and_romaji


class TestTranslator(unittest.TestCase):

    def test_translate_to_chinese(self):
        text = "Hello"
        result = translate_to_chinese(text)
        # 你可以使用你期望的翻譯結果來替換下面的字符串
        self.assertEqual(result, "您好")

    def test_split_hiragana_and_romaji(self):
        word = {
            '漢字': '訓練',
            '平假名': 'kunrenくんれん',
            '英文翻譯': 'training; drill; practice; discipline'
        }
        result = split_hiragana_and_romaji(word)
        expected_result = {
            '漢字': '訓練',
            '平片假名': 'くんれん',
            '羅馬拼音': 'kunren',
            '英文翻譯': 'training; drill; practice; discipline'
        }
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
import unittest
import os
import sys
sys.path.insert(0, r'D:\GitHub\JLPT_VocabularyToDiscord')
from main import main

class TestMain(unittest.TestCase):
    def setUp(self):
        # 檔案路徑
        self.file_path = r'D:\GitHub\JLPT_VocabularyToDiscord\app\utils\current_level.txt'
        # 如果檔案存在，刪除它以便於測試
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_main(self):
        # 運行 main 函數
        main()

        # 檢查檔案是否存在
        self.assertTrue(os.path.exists(self.file_path))

        # 讀取檔案中的等級
        with open(self.file_path, 'r') as file:
            current_level = file.read().strip()

        # 檢查等級是否為 'N4'，因為 main 函數應該在第一次運行時將等級從 'N3' 更新為 'N4'
        self.assertEqual(current_level, 'N4')

if __name__ == '__main__':
    unittest.main()
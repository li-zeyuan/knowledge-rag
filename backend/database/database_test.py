import unittest
from .database import create_db

class TestCreateDb(unittest.TestCase):
    def test_create_db(self):
        create_db("test",[
            "/Users/zeyuan.li/Desktop/workspace/ggo/src/github.com/li-zeyuan/knowledge-rag/backend/knowledge_db/强化学习入门指南.txt"
        ], "openai")

if __name__ == "__main__":
    unittest.main()
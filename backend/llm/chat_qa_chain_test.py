import unittest
from chat_qa_chain import markdown_to_html


class TestChatQaChain(unittest.TestCase):
    def test_markdown_to_html(self):
        markdown_text = """你好"""
        html_text = markdown_to_html(markdown_text)
        print(html_text)

if __name__ == "__main__":
    unittest.main()
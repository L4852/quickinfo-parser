import unittest

from parser import Parser


class MyTestCase(unittest.TestCase):
    def test_start_end_file(self):
        parser = Parser(
            """
            -
            message: Hello World!
            -
            not_a_message: Not recorded
            """
        )

        parser2 = Parser(
            """
            -
            message: Hello World!
            -
            -
            a: 50
            -
            """
        )

        result = parser.parse()
        result2 = parser2.parse()

        self.assertEqual(result['message'], "Hello World!")
        self.assertEqual(result2['message'], "Hello World!")

        self.assertEqual('not_a_message' not in result.keys(), True)
        self.assertEqual('-' not in result.keys(), True)
        self.assertEqual('a' not in result.keys(), True)

    def test_comments(self):
        parser = Parser(
            """
            -
            message: Hello World! # This is a comment
            -
            """
        )

        parser2 = Parser(
            """
            -
            message: Hello World! # This is a comment # abc
            -
            """
        )

        result = parser.parse()
        result2 = parser2.parse()

        self.assertEqual(result['message'], "Hello World!")
        self.assertEqual(result2['message'], "Hello World!")

    def test_int(self):
        def test_list(self):
            parser = Parser(
                """
                -
                myvar : 8
                -
                """
            )

            result = parser.parse()

            self.assertEqual(result['myvar'], 8)

    def test_float(self):
        def test_list(self):
            parser = Parser(
                """
                -
                myvar : 8.5
                -
                """
            )

            result = parser.parse()

            self.assertEqual(result['myvar'], 8.5)

    def test_list(self):
        parser = Parser(
            """
            -
            mylist : / a, b, c /
            -
            """
        )

        result = parser.parse()

        self.assertEqual(result['mylist'], ['a', 'b', 'c'])

    def test_list_nested(self):
        parser = Parser(
            """
            -
            mylist : / a, b, / c, d, e / /
            -
            """
        )

        result = parser.parse()

        self.assertEqual(result['mylist'], ['a', 'b', ['c', 'd', 'e']])


if __name__ == '__main__':
    unittest.main()

import unittest

from parser import Parser


class MyTestCase(unittest.TestCase):
    # Test Functionality
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

    def test_line_read(self):
        parser = Parser(
            """
            -
            message: Hello World!
            message1: Hello World 1!
            message2: 123
            -
            """
        )

        result = parser.parse()

        self.assertEqual(result['message'], "Hello World!")
        self.assertEqual(result['message1'], "Hello World 1!")
        self.assertEqual(result['message2'], 123)

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
                my_var : 8
                -
                """
            )

            result = parser.parse()

            self.assertEqual(result['my_var'], 8)

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
            mylist : / a, b, c \\
            -
            """
        )

        result = parser.parse()

        self.assertEqual(result['mylist'], ['a', 'b', 'c'])

    def test_list_nested(self):
        parser = Parser(
            """
            -
            mylist : / a, b, / c, d, e \\ \\
            -
            """
        )

        result = parser.parse()

        self.assertEqual(result['mylist'], ['a', 'b', ['c', 'd', 'e']])

    def test_number_string(self):
        parser = Parser(
            """
            -
            number: 30
            -
            """
        )

        parser2 = Parser(
            """
            -
            string: '30
            -
            """
        )

        result = parser.parse()
        result2 = parser2.parse()

        self.assertEqual(result['number'], 30)
        self.assertEqual(result2['string'], '30')

    def test_error_invalid_character(self):
        parser = Parser(
            """
            -
            key: "value"
            -
            """
        )

        result = parser.parse()

        self.assertEqual(result, {})

    # Error Handling
    def test_error_mismatched_key(self):
        parser = Parser(
            """
            -
            incomplete_message: 
            -
            """
        )

        result = parser.parse()

        self.assertEqual(result, {})

    def test_error_mismatched_list(self):
        parser = Parser(
            """
            -
            incomplete_list: / a, b, c, 1 
            -
            """
        )

        result = parser.parse()

        self.assertEqual(result, {})

    def test_error_duplicate_key(self):
        parser = Parser(
            """
            -
            key: 1
            key: 2
            -
            """
        )

        result = parser.parse()

        self.assertEqual(result, {})

    def test_error_document_boundary(self):
        parser = Parser(
            """
            -
            key: 1 -
            """
        )

        result = parser.parse()

        self.assertEqual(result, {})

    def test_error_invalid_character(self):
        parser = Parser(
            """
            -
            key: "value"
            -
            """
        )

        result = parser.parse()

        self.assertEqual(result, {})


if __name__ == '__main__':
    unittest.main()

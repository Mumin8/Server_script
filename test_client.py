import unittest
from unittest.mock import patch
import client


class TestClient(unittest.TestCase):

    @patch('socket.create_connection')
    @patch('ssl.create_default_context')
    def test_search_string_exists(self, mock_context, mock_create_connection):

        mock_socket = (
                mock_create_connection.return_value.__enter__.return_value
                )
        mock_secure_socket = (
                mock_context.return_value.wrap_socket.
                return_value.__enter__.return_value
                )
        mock_secure_socket.recv.return_value.decode.return_value = (
                'STRING EXISTS'
                )

        valid_queries = [
                        '3;0;1;28;0;7;5;0;',
                        '10;0;1;26;0;8;3;0;',
                        '18;0;6;28;0;23;5;0;',
                        '7;0;1;28;0;9;3;0;',
                        '22;0;6;28;0;23;3;0;',
                        '7;0;6;28;0;23;5;0;;',
                        '2;0;1;26;0;7;5;0;',
                        '10;0;1;26;0;7;4;0;',
                        '7;0;1;26;0;8;3;0;',
                        '13;0;1;28;0;7;4;0;',
                        '3;0;1;16;0;7;5;0;',
                        '13;0;1;26;0;7;3;0;',
                        '9;0;1;28;0;8;5;0;',
                        '2;0;23;21;0;22;3;0;',
                        '2;0;6;26;0;24;5;0;',
                        '21;0;1;28;0;8;4;0;',
                        '10;0;1;26;0;9;3;0;',
                        '23;0;1;26;0;8;3;0;',
                        '6;0;1;26;0;7;3;0;',
                        '6;0;1;16;0;7;3;0;',
                        '25;0;23;16;0;19;3;0;',
                        '5;0;1;26;0;8;4;0;',
                        '20;0;1;28;0;6;5;0;',
                        '25;0;1;26;0;9;5;0;',
                        '11;0;6;28;0;23;5;0;',
                        '24;0;6;16;0;7;4;0;',
                        '5;0;6;26;0;23;5;0;',
                        '18;0;1;11;0;7;3;0;'
                        ]
        for query in valid_queries:
            result = client.search_string(query)
            self.assertEqual(result, 'STRING EXISTS')

    @patch('socket.create_connection')
    @patch('ssl.create_default_context')
    def test_search_string_not_exists(self,
                                      mock_context, mock_create_connection):
        mock_socket = (
                mock_create_connection.return_value.__enter__.return_value
                )
        mock_secure_socket = (
                mock_context.return_value.wrap_socket.
                return_value.__enter__.return_value
                )
        mock_secure_socket.recv.return_value.decode.return_value = (
            'STRING NOT FOUND'
            )

        invalid_query = "this;query;is;invalid;"
        result = client.search_string(invalid_query)

        self.assertEqual(result, 'STRING NOT FOUND')


if __name__ == '__main__':

    unittest.main()

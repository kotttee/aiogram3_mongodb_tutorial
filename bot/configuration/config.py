from configparser import ConfigParser
import ast

parser = ConfigParser()
parser.read('config.ini')


class Configuration:

    @staticmethod
    def bot_token() -> str:
        return parser.get('bot', 'token')

    @staticmethod
    def database_connection() -> str:
        return parser.get('database', 'connection')

    @staticmethod
    def available_languages() -> list:
        return ast.literal_eval(parser.get('languages', 'available'))

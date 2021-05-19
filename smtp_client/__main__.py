from argparse import ArgumentParser
from smtp_client import SMTPClient
from typing import Any, Dict


def parse_args() -> Dict[str, Any]:
    parser = ArgumentParser()
    parser.add_argument('--ssl', action='store_true',
                        help='Use SSL connection')
    parser.add_argument('-s', '--server', default='smtp.mail.ru:25',
                        help='Server and port')
    parser.add_argument('-t', '--to', help='Recipient address')
    parser.add_argument('-f', '--login', '--from', default='<>',
                        metavar='sender', help='Sender address')
    parser.add_argument('--subject', default='Happy pictures',
                        help='Subject of mail')
    parser.add_argument('--auth', action='store_true',
                        help='Request authentication')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose mode')
    parser.add_argument('-d', '--directory', default='.',
                        help='Source of images')
    return parser.parse_args().__dict__


if __name__ == '__main__':
    SMTPClient(**parse_args()).run()

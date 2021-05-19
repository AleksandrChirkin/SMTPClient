from pathlib import Path
from smtp_client import File, Letter, SMTPError
from socket import AF_INET, SOCK_STREAM, socket
import base64
import getpass
import os
import ssl


class SMTPClient:
    def __init__(self, ssl: bool, server: str, to: str, login: str,
                 subject: str, auth: bool, verbose: bool, directory: str):
        self.ssl = ssl
        server_port = server.split(':')
        self.server = server_port[0]
        self.port = int(server_port[1])
        self.to = to
        self.login = login
        modified_login = self.login.replace("@", ".")
        self.subject = subject
        self.directory = Path(directory)
        self.do_verbose = verbose
        if auth:
            self.password = getpass.getpass()
        self.commands = []
        self.commands = [f'EHLO {modified_login}\n',
                         f'MAIL FROM: <{self.login}>\nrcpt to: '
                         f'<{self.to}>\nDATA\n']
        if auth:
            base_login = base64.b64encode(self.login.encode('utf-8'))\
                .decode('utf-8')
            base_passwd = base64.b64encode(self.password.encode('utf-8'))\
                .decode('utf-8')
            self.commands.insert(1, 'auth login\n')
            self.commands.insert(2, f'{base_login}\n')
            self.commands.insert(3, f'{base_passwd}\n')

    def create_letter(self) -> str:
        letter = Letter()
        letter.set_header(self.login, self.to, self.subject)
        files = [File(self.directory / x)
                 for x in os.listdir(self.directory)
                 if x.endswith('.jpg')]
        for i in range(len(files)):
            if i == len(files) - 1:
                letter.set_content(files[i], True)
            else:
                letter.set_content(files[i])
        return letter.get_letter()

    def receive_message(self, sock: socket) -> None:
        all_msg = sock.recv(1024).decode('utf-8')
        msg_parts = all_msg.split('\n')[:-1]
        last_code = msg_parts[-1][0:4]
        if last_code[0] == '5':
            raise SMTPError(all_msg)
        if self.do_verbose:
            print('<- ' + all_msg)

    def send_message(self, sock: socket, msg: str) -> None:
        if self.do_verbose:
            print('-> ' + msg)
        sock.send(msg.encode())

    def run(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            try:
                sock.connect((self.server, self.port))
                self.receive_message(sock)
                if self.ssl:
                    self.send_message(sock,
                                      f'EHLO {self.login.replace("@", ".")}\n')
                    self.receive_message(sock)
                    self.send_message(sock, 'starttls\n')
                    self.receive_message(sock)
                    sock = ssl.wrap_socket(sock)
                for command in self.commands:
                    self.send_message(sock, command)
                    self.receive_message(sock)
                    if 'DATA' in command:
                        sock.send(self.create_letter().encode())
                        self.receive_message(sock)
            except SMTPError as e:
                print(e)

from smtp_client import File


class Letter:
    def __init__(self):
        self.letter_text = ''

    def set_header(self, from_usr: str, to_usr: str, subject: str) -> None:
        self.letter_text += f'From: {from_usr}\nTo: {to_usr}\n' \
                            f'Subject: {subject}'
        self.letter_text += '\nContent-type: multipart/mixed; boundary=a'

    def set_content(self, file: File, is_last: bool = False) -> None:
        self.letter_text += '\n\n--a'
        self.letter_text += '\nMime-Version: 1.0'
        self.letter_text += f'\nContent-Type: image/jpeg; ' \
                            f'name="=?UTF-8?B?{file.b64_name}?="'
        self.letter_text += f'\nContent-Disposition: attachment; ' \
                            f'filename="=?UTF-8?B?{file.b64_name}?="'
        self.letter_text += '\nContent-Transfer-Encoding: base64\n\n'
        self.letter_text += file.get_base64()
        if is_last:
            self.letter_text += '\n--a--'
            self.letter_text += '\n.\n'
        else:
            self.letter_text += '\n--a'

    def get_letter(self) -> str:
        return self.letter_text

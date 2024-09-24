from config import API_KEY, SECRET_KEY, IMEI, SESSION_COOKIES
from mitaizl import CommandHandler
from zlapi import ZaloAPI
from colorama import Fore, Style, init

init(autoreset=True)

class Client(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies):
        super().__init__(api_key, secret_key, imei=imei, session_cookies=session_cookies)
        self.command_handler = CommandHandler(self)

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        print(f"{Fore.GREEN}{Style.BRIGHT}------------------------------\n"
              f"**Message Details:**\n"
              f"- **Message:** {Style.BRIGHT}{message} {Style.NORMAL}\n"
              f"- **Author ID:** {Fore.MAGENTA}{Style.BRIGHT}{author_id} {Style.NORMAL}\n"
              f"- **Thread ID:** {Fore.YELLOW}{Style.BRIGHT}{thread_id}{Style.NORMAL}\n"
              f"- **Thread Type:** {Fore.BLUE}{Style.BRIGHT}{thread_type}{Style.NORMAL}\n"
              f"- **Message Object:** {Fore.RED}{Style.BRIGHT}{message_object}{Style.NORMAL}\n"
              f"{Fore.GREEN}{Style.BRIGHT}------------------------------\n"
              )
        if isinstance(message, str):
            self.command_handler.handle_command(message, author_id, message_object, thread_id, thread_type)

if __name__ == "__main__":
    client = Client(API_KEY, SECRET_KEY, IMEI, SESSION_COOKIES)
    client.listen(run_forever=True)

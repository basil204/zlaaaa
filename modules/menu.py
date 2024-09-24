import os
from zlapi.models import Message
import importlib

def get_all_mitaizl():
    mitaizl = {}

    for module_name in os.listdir('modules'):
        if module_name.endswith('.py') and module_name != '__init__.py':
            module_path = f'modules.{module_name[:-3]}'
            module = importlib.import_module(module_path)

            if hasattr(module, 'get_mitaizl'):
                module_mitaizl = module.get_mitaizl()
                mitaizl.update(module_mitaizl)

    command_names = list(mitaizl.keys())
    
    return command_names

def handle_menu_command(message, message_object, thread_id, thread_type, author_id, client):

    command_names = get_all_mitaizl()

    total_mitaizl = len(command_names)
    numbered_mitaizl = [f"{i+1}. {name}" for i, name in enumerate(command_names)]
    menu_message = f"Tổng số lệnh bot hiện tại có: {total_mitaizl} lệnh \nDưới đây là các lệnh hiện có của bot:\n" + "\n".join(numbered_mitaizl)

    message_to_send = Message(text=menu_message)

    client.replyMessage(message_to_send, message_object, thread_id, thread_type)
    
def get_mitaizl():
    return {
        'menu': handle_menu_command
    }

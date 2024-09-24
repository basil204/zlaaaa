import requests
import os
from zlapi.models import Message, ZaloAPIException

def handle_phone_number_info_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        nhapso = message.split()

        if len(nhapso) > 1:
            sotrave = nhapso[1].lower()

        user_info = client.fetchPhoneNumber(sotrave)

        if not isinstance(user_info, dict):
            user_info = user_info.__dict__

        if 'error' in user_info:
            error_message = Message(text="Could not retrieve user info. Please check the phone number and try again.")
            client.sendMessage(error_message, thread_id, thread_type)
            return

        user_info_message = f"User Info (via phone number):\n{user_info}" 

        message_to_send = Message(text=user_info_message)

        client.sendMessage(message_to_send, thread_id, thread_type)

    except ZaloAPIException as e:
        error_message = Message(text="Could not retrieve user info due to a Zalo API error.")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"An unexpected error occurred: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'sms': handle_phone_number_info_command, 
    }
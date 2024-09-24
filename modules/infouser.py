import requests
import os
from zlapi.models import Message, ZaloAPIException
from datetime import datetime

def handle_user_info(message, message_object, thread_id, thread_type, author_id, client):
    try:
        input_parts = message.split()

        if len(input_parts) > 1:
            input_value = input_parts[1].lower()
        if message_object.mentions:
         input_value = message_object.mentions[0]['uid']
        else:
            input_value = author_id

        # Attempt to fetch user ID using phone number
        try:
            user_id_data = client.fetchPhoneNumber(input_value, language="vi")
            if not isinstance(user_id_data, dict):
                user_id_data = user_id_data.__dict__
            user_id_to_fetch = user_id_data.get('uid') 
            sdob_to_fetch = user_id_data.get('sdob') 
        except ZaloAPIException:
            user_id_to_fetch = None 

        # If phone number lookup fails, assume input is a user ID
        if not user_id_to_fetch:
            user_id_to_fetch = input_value

        # Fetch user info using the retrieved or provided user ID
        user_info = client.fetchUserInfo(user_id_to_fetch)

        if not isinstance(user_info, dict):
            user_info = user_info.__dict__

        # Extract user data from the response
        changed_profiles = user_info.get('changed_profiles', {})
        user_data = changed_profiles.get(user_id_to_fetch, {})

        user_name = user_data.get('displayName', 'N/A')
        user_id = user_data.get('userId', 'N/A')
        user_avatar = user_data.get('avatar', None)
        user_status = user_data.get('status', 'N/A')
        user_username = user_data.get('username', 'N/A')
        user_phone_number = user_data.get('phoneNumber', 'N/A')
        user_gender = user_data.get('gender')
        
        if user_gender == 0:
            user_gender_str = "Male"
        elif user_gender == 1:
            user_gender_str = "Female"
        else:
            user_gender_str = "Other"

        # Get and format date of birth (from user_data or sdob_to_fetch)
        user_dob = user_data.get('dob') or sdob_to_fetch 
        if user_dob:
            user_dob_str = datetime.fromtimestamp(user_dob).strftime('%d/%m/%Y')
        else:
            user_dob_str = 'N/A'

        user_info_message = (
            f"User Details:\n"
            f"- Name: {user_name}\n"
            f"- ID: {user_id}\n"
            f"- Username: {user_username}\n"
            f"- Phone Number: {user_phone_number}\n"
            f"- Gender: {user_gender_str}\n"
            f"- Date of Birth: {user_dob_str}\n"
            f"- Status: {user_status}\n"
        )

        message_to_send = Message(text=user_info_message)

        if user_avatar:
            image_response = requests.get(user_avatar)
            image_path = 'temp_image.jpeg'

            with open(image_path, 'wb') as f:
                f.write(image_response.content)

            client.sendLocalImage(
                image_path,
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type
            )

            # Remove the temporary image file after sending
            os.remove(image_path)

        else:
            # Use replyMessage when no image is available
            client.replyMessage(message_to_send, message_object, thread_id, thread_type) 

    except ValueError as e:
        error_message = Message(text=str(e))
        client.replyMessage(error_message, message_object, thread_id, thread_type) 
    except ZaloAPIException as e:
        error_message = Message(text="Could not retrieve user info due to a Zalo API error.")
        client.replyMessage(error_message, message_object, thread_id, thread_type) 
    except Exception as e:
        error_message = Message(text=f"An unexpected error occurred: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id, thread_type) 

def get_mitaizl():
    return {
        'userinfo': handle_user_info, 
    }
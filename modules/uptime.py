from zlapi.models import Message
import time
import os
import requests

start_time = time.time()

def handle_uptime_command(message, message_object, thread_id, thread_type, author_id, client):
    current_time = time.time()
    uptime_seconds = int(current_time - start_time)

    days = uptime_seconds // (24 * 3600)
    uptime_seconds %= (24 * 3600)
    hours = uptime_seconds // 3600
    uptime_seconds %= 3600
    minutes = uptime_seconds // 60
    seconds = uptime_seconds % 60

    uptime_message = f"Bot đã hoạt động được {days} ngày, {hours} giờ, {minutes} phút, {seconds} giây."
    
    message_to_send = Message(text=uptime_message)
    
    api_url = 'https://api.sumiproject.net/images/girl'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        # Lấy link ảnh từ JSON
        data = response.json()
        image_url = data['url']
        
        # Tải ảnh từ link
        image_response = requests.get(image_url, headers=headers)
        image_path = 'temp_image.jpeg'
        
        with open(image_path, 'wb') as f:
            f.write(image_response.content)
        
        # Gửi ảnh đã tải về
        client.sendLocalImage(
            image_path, 
            message=message_to_send,
            thread_id=thread_id,
            thread_type=thread_type
        )
        
        # Xóa file ảnh sau khi gửi
        os.remove(image_path)
        
    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'uptime': handle_uptime_command
    }

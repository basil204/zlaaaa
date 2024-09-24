import requests
import os
from zlapi.models import Message, ZaloAPIException

def handle_bill_number_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        command_parts = message.split()
        if len(command_parts) < 2:
            raise ValueError("Missing bill number. Please provide a bill number after the command.")

        bill_number = command_parts[1]
        api_url = f"https://webapidatashop.onrender.com/checkid?id={bill_number}"

        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()

        
        ngay_mua = data.get("D")
        ngay_het_han = data.get("G")
        so_ngay_con_lai = data.get("K")
        dich_vu = data.get("Q")
        so_tien = data.get("U")
        so_dien_thoai = data.get("C")  

        if so_dien_thoai:
            user_info_data = client.fetchPhoneNumber(so_dien_thoai)  
            user_name = user_info_data.get('zalo_name', 'N/A')
            uid = user_info_data.get('uid')
            user_info_message = f"""Elite Access Hub xin chào {user_name},
Elite Access Hub gửi bạn thông tin đơn hàng:
- Ngày mua: {ngay_mua}
- Ngày hết hạn: {ngay_het_han}
- Số ngày còn lại: {so_ngay_con_lai}
- Dịch vụ bạn đang sử dụng là: {dich_vu}
- Số tiền đã thanh toán: {so_tien}
- Gruop zalo bảo hành : https://zalo.me/g/yrqroa822
"""

            admin_message = f"""Đã gửi bill cho: {so_dien_thoai}
Mua dịch vụ : {dich_vu}"""

        else:
            user_info_message = "\nC value not found in the API response."
            admin_message = user_info_message

        message_to_send = Message(text=user_info_message)
        admin_notification = Message(text=admin_message)

        client.sendMessage(message_to_send, uid, thread_type.USER)
        client.sendMessage(admin_notification, thread_id, thread_type)

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Error fetching data from the API for bill {bill_number}: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

    except ZaloAPIException as e:
        error_message = Message(text="Could not send message due to a Zalo API error.")
        client.sendMessage(error_message, thread_id, thread_type)

    except ValueError as e:
        error_message = Message(text=f"Invalid command format: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

    except Exception as e:
        error_message = Message(text=f"An unexpected error occurred while processing bill {bill_number}: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'bill': handle_bill_number_command,
    }
import requests
import os
import datetime
from zlapi.models import Message, ZaloAPIException

def handle_bill_number_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        api_url = "https://webapidatashop.onrender.com/fulldata"
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()

        today = datetime.date.today()

        for value in data:
            # Extract date components, using 0 as default for missing values
            day_in_column_h = int(value.get('H', 0))
            month_in_column_i = int(value.get('I', 0))
            year_in_column_j = int(value.get('J', 0))

            # Construct expiration date (handle potential ValueError)
            try:
                expiration_date = datetime.date(year_in_column_j, month_in_column_i, day_in_column_h)
            except ValueError:
                print(f"Invalid date encountered: {year_in_column_j}-{month_in_column_i}-{day_in_column_h}")
                continue  # Skip this row if the date is invalid

            if expiration_date == today:
                days_remaining = 0  # Since it matches today

                phone = value.get('C')
                service = value.get('Q')
                purchase_date = value.get('D')
                email = value.get('W')
                so_tien = value.get("U")  # Assuming 'so_tien' is within each 'value'
                so_tien1 = int(''.join(filter(str.isdigit, so_tien or '')))  # Handle potential None
                nd = phone + " " + service
                k_message = f"còn {days_remaining} ngày" if days_remaining > 0 else "Hết hạn rồi"

                # Fetch user name
                user_info_data = client.fetchPhoneNumber(phone)
                user_name = user_info_data.get('zalo_name', 'N/A')

                # Construct the messages
                message1 = f"""Đã gửi bảo hành Đến :{user_name}
Số điện thoại đăng ký là :{phone}
Dịch Vụ hết hạn là : {service}
"""
                message = f"""
Elite Access Hub xin chào {user_name}
đang sử dụng dịch vụ: {service} của Elite Access Hub
Đơn mua ngày: {purchase_date}
Email đã đăng ký: {email}
Thời hạn sử dụng dịch vụ của {user_name}: {k_message}
----\n
"""

                # Construct QR code image URL
                qr_code_url = f"https://api.vietqr.io/image/970436-9338739954-VyGamuZ.jpg?accountName=NGUYEN%20LIEN%20MANH&amount={so_tien1}&addInfo={nd}"

                # Fetch the QR code image
                image_response = requests.get(qr_code_url)
                image_response.raise_for_status()

                # Send the text messages
                message_to_send1 = Message(text=message1)
                client.sendMessage(message_to_send1, thread_id, thread_type)

                message_to_send = Message(text=message)
                # client.sendMessage(message_to_send, thread_id, thread_type)

                # Send the image
                image_path = 'temp_image.jpeg'
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)

                client.sendLocalImage(
                    image_path,
                    message=message_to_send,  # Associate image with the text message
                    thread_id=author_id,
                    thread_type=thread_type.USER
                )

                os.remove(image_path)  # Clean up the temporary image file

    except ZaloAPIException as e:
        error_message = Message(text="Could not send message due to a Zalo API error.")
        client.sendMessage(error_message, thread_id, thread_type)
    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Error fetching data from the API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)
    # except Exception as e:  # Consider re-enabling for general error handling
    #     error_message = Message(text=f"An unexpected error occurred: {str(e)}")
    #     client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'check': handle_bill_number_command,
    }
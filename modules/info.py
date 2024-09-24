import requests
import os
from zlapi.models import Message, ZaloAPIException
import logging

def handle_group_info_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        group_info = client.fetchGroupInfo(thread_id)
        if not isinstance(group_info, dict):
            group_info = group_info.__dict__

        
        group_details = group_info.get('gridInfoMap', {}).get(thread_id, {})
        group_name = group_details.get('name', 'N/A')
        group_id = group_details.get('groupId', 'N/A')
        group_avatar = group_details.get('fullAvt', None)

        
        group_desc = group_details.get('desc', 'N/A')
        admin_ids = group_details.get('adminIds', [])
        total_members = group_details.get('totalMember', 'N/A')
        max_members = group_details.get('maxMember', 'N/A')

     
        group_settings = group_details.get('setting', {})
        block_name = group_settings.get('blockName', 'N/A')
        sign_admin_msg = group_settings.get('signAdminMsg', 'N/A')
        add_member_only = group_settings.get('addMemberOnly', 'N/A')
        set_topic_only = group_settings.get('setTopicOnly', 'N/A')  
        enable_msg_history = group_settings.get('enableMsgHistory', 'N/A')  
        lock_create_post = group_settings.get('lockCreatePost', 'N/A')  
        lock_create_poll = group_settings.get('lockCreatePoll', 'N/A')  
        join_appr = group_settings.get('joinAppr', 'N/A')  
        lock_send_msg = group_settings.get('lockSendMsg', 'N/A')  
        lock_view_member = group_settings.get('lockViewMember', 'N/A')  

        
        group_info_message = (
            f"Group Details:\n"
            f"  - Name: {group_name}\n"
            f"  - ID: {group_id}\n"
            f"  - Description: {group_desc}\n"
            f"  - Admin IDs: {', '.join(admin_ids)}\n"
            f"  - Total Members: {total_members}\n"
            f"  - Max Members: {max_members}\n"
            f"  - Block Name Change & Avatar: {block_name}\n"
            f"  - Sign Admin Msg: {sign_admin_msg}\n"
            f"  - Add Member Only: {add_member_only}\n"
            f"  - Set Topic Only: {set_topic_only}\n"  
            f"  - Enable Msg History: {enable_msg_history}\n"  
            f"  - Lock Create Post: {lock_create_post}\n"  
            f"  - Lock Create Poll: {lock_create_poll}\n" 
            f"  - Join Approval: {join_appr}\n"  
            f"  - Lock Send Msg: {lock_send_msg}\n"  
            f"  - Lock View Member: {lock_view_member}\n"  
        )

        message_to_send = Message(text=group_info_message)

        if group_avatar:
            image_response = requests.get(group_avatar)
            image_path = 'temp_image.jpeg'

            with open(image_path, 'wb') as f:
                f.write(image_response.content)

            client.sendLocalImage(
                image_path, 
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type
            )
            
            os.remove(image_path)

    except ZaloAPIException as e:
        logging.error(f"Zalo API Error: {e}")
        error_message = Message(text="Could not retrieve group info due to a Zalo API error.")
        client.sendMessage(error_message, thread_id, thread_type)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        error_message = Message(text=f"An unexpected error occurred: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type)

def get_mitaizl():
    return {
        'info': handle_group_info_command
    }

# Updated `updateGroupSettings` function to handle all settings
def updateGroupSettings(client, groupId, defaultMode="default", **kwargs):
    """
    Update group settings.

    Args:
        groupId (int | str): Group ID to update settings
        defaultMode (str): Default mode of settings
            default: Group default settings
            anti-raid: Group default settings for anti-raid
        **kwargs: Group settings kwargs, Value: (1 = True, 0 = False)
            blockName: Không cho phép user đổi tên & ảnh đại diện nhóm
            signAdminMsg: Đánh dấu tin nhắn từ chủ/phó nhóm
            addMemberOnly: Chỉ thêm members (Khi tắt link tham gia nhóm)
            setTopicOnly: Cho phép members ghim (tin nhắn, ghi chú, bình chọn)
            enableMsgHistory: Cho phép new members đọc tin nhắn gần nhất
            lockCreatePost: Không cho phép members tạo ghi chú, nhắc hẹn
            lockCreatePoll: Không cho phép members tạo bình chọn
            joinAppr: Chế độ phê duyệt thành viên
            lockSendMsg: Không cho phép members gửi tin nhắn
            lockViewMember: Không cho phép members xem thành viên nhóm
            blocked_members: Danh sách members bị chặn (list of user IDs)

    Returns:
        bool: True if settings updated successfully, False otherwise
    """

    # Convert kwargs values to 1 or 0
    for key, value in kwargs.items():
        kwargs[key] = 1 if value else 0

    try:
        client.updateGroupSettings(groupId, defaultMode, **kwargs)
        return True
    except ZaloAPIException as e:
        logging.error(f"Zalo API Error while updating group settings: {e}")
        return False
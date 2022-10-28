"""Admins Middleware"""
from functools import wraps
from typing import Union, Literal
from pyrogram import filters, enums, Client
from pyrogram.errors import ChatWriteForbidden
from traceback import format_exc as err
from pyrogram.types import Message
from pyrogram.types import ChatPrivileges


async def authorised(func, subFunc2, client, message, *args, **kwargs):
    chatID = message.chat.id
    try:
        await func(client, message, *args, **kwargs)
    except ChatWriteForbidden:
        await client.leave_chat(chatID)
    except Exception as e:
        try:
            await message.reply_text(str(e.MESSAGE))
        except AttributeError:
            await message.reply_text(str(e))
        e = err()
        print(str(e))
    return subFunc2


async def unauthorised(message: Message, client: Client, permission, subFunc2, text):
    if text is None:
        return subFunc2
    chatID = message.chat.id

    try:
        await message.reply_text(text)
    except ChatWriteForbidden:
        await client.leave_chat(chatID)
    return subFunc2


async def member_permissions(chat_id: int, user_id: int, app: Client):
    perms = []
    try:
        member = await app.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.status == enums.ChatMemberStatus.MEMBER:
        return []
    if member.privileges.can_post_messages:
        perms.append("can_post_messages")
    if member.privileges.can_edit_messages:
        perms.append("can_edit_messages")
    if member.privileges.can_delete_messages:
        perms.append("can_delete_messages")
    if member.privileges.can_restrict_members:
        perms.append("can_restrict_members")
    if member.privileges.can_promote_members:
        perms.append("can_promote_members")
    if member.privileges.can_change_info:
        perms.append("can_change_info")
    if member.privileges.can_invite_users:
        perms.append("can_invite_users")
    if member.privileges.can_pin_messages:
        perms.append("can_pin_messages")
    if member.privileges.can_manage_video_chats:
        perms.append("can_manage_voice_chats")
    return perms


def adminsWith(
    permission: Union[
        Literal[
            "can_post_messages",
            "can_edit_messages",
            "can_delete_messages",
            "can_restrict_members",
            "can_promote_members",
            "can_change_info",
            "can_invite_users",
            "can_pin_messages",
            "can_manage_voice_chats",
        ],
        ChatPrivileges,
    ],
    unAuthorisedReply: Union[str, None, Literal["Default"]] = "Default",
):
    if unAuthorisedReply == "Default":
        unAuthorisedReply = (
            "You don't have the required permission to perform this action."
            + f"\n**Permission:** __{permission}__"
        )

    def subFunc(func):
        @wraps(func)
        async def subFunc2(client: Client, message: Message, *args, **kwargs):
            chatID = message.chat.id
            if not message.from_user:
                # For anonymous admins
                if message.sender_chat and message.sender_chat.id == message.chat.id:
                    return await authorised(
                        func,
                        subFunc2,
                        client,
                        message,
                        *args,
                        **kwargs,
                    )
                return await unauthorised(
                    message, permission, subFunc2, unAuthorisedReply
                )

            if message.chat.type == enums.ChatType.PRIVATE:
                return await authorised(
                    func, subFunc2, client, message, *args, **kwargs
                )

            userID = message.from_user.id
            permissions = await member_permissions(chatID, userID, client)
            if permission not in permissions:
                return await unauthorised(
                    message, client, permission, subFunc2, unAuthorisedReply
                )
            return await authorised(func, subFunc2, client, message, *args, **kwargs)

        return subFunc2

    return subFunc


Client.admins_with = adminsWith

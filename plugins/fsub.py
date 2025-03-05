from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest, Message
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from info import ADMINS, AUTH_CHANNEL
from database.fsub_db import Fsub_DB

LINK = None 

@Client.on_chat_join_request(filters.chat(AUTH_CHANNEL))
async def filter_join_reqs(bot, message: ChatJoinRequest):
    user_id = message.from_user.id
    f_name = message.from_user.first_name
    u_name = message.from_user.username
    date = message.date
    await Fsub_DB().add_user(
        user_id,
        f_name,
        u_name,
        date
    )

@Client.on_message(filters.command("total_reqs") & filters.private & filters.user(ADMINS))
async def total_requests(bot, message):
    total = await Fsub_DB().total_users()
    return await message.reply_text(
        f"<b>Total Number Of Requests: {total}</b>"
    )

@Client.on_message(filters.command("delete_reqs") & filters.private & filters.user(ADMINS))
async def delete_requests(bot, message):
    total = await Fsub_DB().total_users()
    await Fsub_DB().purge_users()
    return await message.reply_text(
        f"Successfully deleted all {total} requests from DB !"
    )

@Client.on_message(filters.command("purge_req") & filters.private & filters.user(ADMINS))
async def purge_requests(bot, message):
    try:
        cmd = (message.text).split(" ", 1)[1]
    except:
        return await message.reply_text("Give me a user ID along with it. For example: /purge_req 11XXXXXX")
    user = await Fsub_DB().get_user(int(cmd))
    if user:
        await Fsub_DB().delete_user(int(cmd))
        return await message.reply_text(
            f"Successfully deleted {user['first_name']} from DB."
        )
    else:
        return await message.reply_text("User not found !")

@Client.on_message(filters.command("get_req") & filters.private & filters.user(ADMINS))
async def get_request(bot, message):
    try:
        cmd = (message.text).split(" ", 1)[1]
    except:
        return await message.reply_text("Give me a user ID along with it. For example: /get_req 11XXXXXX")
    user = await Fsub_DB().get_user(int(cmd))
    if not user:
        return await message.reply_text("User Not Found !")
    txt = f"""USER DETAILS:
    ID: {user['id']}
    First Name: {user['first_name']}
    UserName: {user['username']}
    Date: {user['date']}
"""
    return await message.reply_text(
        text=txt
    )

@Client.on_message(filters.command("get_all") & filters.private & filters.user(ADMINS))
async def get_all_requests(bot, message):
    txt = "USER DETAILS:\n\n"
    msg = await message.reply_text(
        text=txt
    )
    for user in await Fsub_DB().get_all_users():
        txt+=f"ID: {user['id']}\nFirst Name: {user['first_name']}\nUserName: {user['username']}\nDate: {user['date']}\n\n--------------------\n\n"
    txt+="NO MORE USERS FOUND !"
    try:
        return await msg.edit_text(
            text=txt
        )
    except MessageTooLong:
        with open('Requests.txt', 'w+') as outfile:
            outfile.write(txt)
        await message.reply_document('Requests.txt', caption="List Of Requests")
        return await msg.delete()
    
async def Force_Sub(bot: Client, message: Message, file_id = False, mode = "checksub"):
    global LINK
    if not AUTH_CHANNEL:
        return True
    else:
        pass
    try:
        if LINK == None:
            link = await bot.create_chat_invite_link(
                chat_id=AUTH_CHANNEL,
                creates_join_request=True
            )
            LINK = link
            print("Invite link created !")
        else:
            link = LINK
    except Exception as e:
        print(f"Unable to create invite link !\n\nError: {e}")
        return False
    try:
        user = await Fsub_DB().get_user(int(message.from_user.id))
        if user and int(user['id']) == int(message.from_user.id):
            return True
        else:
            pass
    except Exception as e:
        print(f"Error: {e}")
        await message.reply_text(f"Error: {e}")
        return False
    try:
        await bot.get_chat_member(
            chat_id=AUTH_CHANNEL,
            user_id=message.from_user.id
        )
        return True
    except UserNotParticipant:
        btn = [[
            InlineKeyboardButton("🤖 Join Updates Channel", url=link.invite_link)
        ]]
        if file_id != False:
            btn.append(
                [
                    InlineKeyboardButton("🔄 Try Again", callback_data=f"{mode}#{file_id}")
                ]
            )
        else:
            pass
        await message.reply_text(
            text="Please Join My Updates Channel to use this Bot !",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.HTML
        )
        return False

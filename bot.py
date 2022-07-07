import os, logging, asyncio

from telegraph import upload_file

from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
xavierbot = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

moment_worker = []


#start
@xavierbot.on(events.NewMessage(pattern="تاك"))
async def start(event):
  await event.reply("اي شرايد مني\n علمود اتشوف الاوامر دز ` اوامر التاك `",
                    buttons=(
                      [
                        Button.url('مطور البوت', 'https://t.me/MOA_YAD'),   
                      ]
                      [
                        Button.url('تواصل المطور', 'https://t.me/M376BOT'),   
                      ]
                   ), 
                    link_preview=False
                   )

#help
@xavierbot.on(events.NewMessage(pattern="اوامر التاك"))
async def help(event):
  helptext = "**قائمه مساعده بوت التاك**\n\nالأمر: @all /n علمود توكفني دز `ايقاف`\n مثال: `@all هيي ` \n "
  await event.reply(helptext,
                    buttons=(
                      [
                        Button.url('مطور البوت', 'https://t.me/MOA_YAD'),   
                      ]             
                      [
                        Button.url('تواصل المطور', 'https://t.me/M376BOT'),   
                      ]
                   ), 
                    link_preview=False
                   )

#التاك
@xavierbot.on(events.NewMessage(pattern="@all"))
async def mentionall(event):
  global moment_worker
  if event.is_private:
    return await event.respond("**بربك هاذه كروب**")
  
  admins = []
  async for admin in xavierbot.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.a@respond("**انته مشرف شي ؟**/n يلة جر منا")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("لا يمكنني ذكر الأعضاء في المنشور القديم !!")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("مثال : `@all هيي`")
  else:
    return await event.respond("ها اطيني شي اسوي بي تاك")
    
  if mode == "text_on_cmd":
    moment_worker.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in xavierbot.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("تم الايقاف 😉")
        return
      if usrnum == 5:
        await xavierbot.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    moment_worker.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in xavierbot.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in moment_worker:
        await event.respond("**تم الايقاف 😉**")
        return
      if usrnum == 5:
        await xavierbot.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


#الغاء التاك

@xavierbot.on(events.NewMessage(pattern="ايقاف"))
async def cancel_mentionall(event):
  if not event.chat_id in moment_worker:
    return await event.respond('**ها شنو منو تحجي وياي**')
  else:
    try:
      moment_worker.remove(event.chat_id)
    except:
      pass
    return await event.respond('**جاري الايقاف**')




print("تم تنصيب بوت التاك بنجاح 💕🍂")
print("لو محتاج مساعده @MOA_YAF")
xavierbot.run_until_disconnected()

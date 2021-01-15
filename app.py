from data.config import BOT_TOKEN, request_each, DB_SETTINGS
from email.header import decode_header
from data.models import db, User
from pony.orm import db_session
from datetime import datetime
from aiogram import Bot
import asyncio
import imaplib
import email
import time

bot = Bot(token=BOT_TOKEN)


@db_session
async def main():
    while True:
        start_time = time.time()
        index = 1
        for user in User.select():
            max_date = datetime.now()
            max_unix = 1
            imap = imaplib.IMAP4_SSL("mail.innopolis.ru")
            imap.login(user.email, user.password)

            status, messages = imap.select("INBOX")
            messages = int(messages[0])

            start_time = time.time()
            for i in range(messages, messages - 3, -1):
                res, msg = imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        Date, encoding = decode_header(msg.get("Date"))[0]
                        if isinstance(Date, bytes):
                            Date = Date.decode(encoding)
                        print(Date[5:-6])
                        print(user.last_seen)
                        date_loc = datetime.strptime(Date[5:-6], '%d %b %Y %H:%M:%S')
                        unix_time = time.mktime(date_loc.timetuple())
                        if unix_time < user.last_seen:
                            continue
                        else:
                            if max_unix < unix_time:
                                max_unix = unix_time
                                max_date = date_loc
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding)
                        From, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(From, bytes):
                            From = From.decode(encoding)
                        message_l = f"New email!\n{subject}\nFrom:{From}"
                        await bot.send_message(user.user_id, message_l)
            imap.close()
            imap.logout()
            user.set(last_seen=datetime.now())  # Error with update in PonyORM
        if request_each - (time.time() - start_time) > 0.5:
            time.sleep(request_each - (time.time() - start_time))


if __name__ == "__main__":
    db.bind('sqlite', DB_SETTINGS.split(":")[1])
db.generate_mapping(create_tables=True)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

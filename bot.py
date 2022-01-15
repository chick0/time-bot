import sys
import logging
from os import environ
from logging import StreamHandler
from datetime import datetime
from datetime import timezone
from datetime import timedelta

from dotenv import load_dotenv
from NicoBot.discordapi.const import LIB_NAME
from NicoBot.discordapi.slash import SlashCommand
from NicoBot.discordapi.slash import DiscordInteractionClient

load_dotenv()

logger = logging.getLogger(LIB_NAME)
handler = StreamHandler(sys.stdout)
fmt = logging.Formatter("[%(levelname)s]|%(asctime)s|%(threadName)s|"
                        "%(funcName)s|: %(message)s")
handler.setFormatter(fmt)
logger.addHandler(handler)

logger.setLevel("INFO")
handler.setLevel("INFO")


@SlashCommand.create("시간 정보 로딩", ())
def t(ctx):
    date_format = "%Y년 %m월 %d일 [ # ]     [ @ ] %I시 %M분"
    date_map = {
        "Sun": "***일요일***",
        "Mon": "월요일",
        "Tue": "화요일",
        "Wed": "수요일",
        "Thu": "목요일",
        "Fri": "금요일",
        "Sat": "**토요일**",
    }
    time_map = {
        "AM": "*오전*",
        "PM": "오후",
    }

    pst = datetime.now(timezone(timedelta(hours=-8)))
    kst = datetime.now(timezone(timedelta(hours=+9)))

    pst = pst.strftime(date_format) \
        .replace("#", date_map.get(pst.strftime("%a"))) \
        .replace("@", time_map.get(pst.strftime("%p")))

    kst = kst.strftime(date_format) \
        .replace("#", date_map.get(kst.strftime("%a"))) \
        .replace("@", time_map.get(kst.strftime("%p")))

    return "\n".join([
        f"= **PST** =   {pst}",
        f"~~=~~ **KST** ~~=~~   {kst}",
    ])


gw = DiscordInteractionClient(
    environ.get("token"),
    intents=4609
)

gw.command_manager.register(t)

gw.start()
gw.ready_to_run.wait()

if "--update" in sys.argv:
    gw.command_manager.update()

logger.info(f"Logged in as {gw.user.username}#{gw.user.discriminator}!")

if __name__ == "__main__":
    try:
        gw.join()
    except KeyboardInterrupt:
        gw.stop()

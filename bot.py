from NicoBot.discordapi.const import LIB_NAME
from NicoBot.discordapi.slash import SlashCommand
from NicoBot.discordapi.slash import DiscordInteractionClient
import sys
import logging
from os import environ
from logging import StreamHandler
from datetime import datetime
from datetime import timezone
from datetime import timedelta

from dotenv import load_dotenv


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
    pst = datetime.now(timezone(timedelta(hours=-8))).strftime("%Y년 %m월 %d일 %H시 %M분")
    kst = datetime.now(timezone(timedelta(hours=9))).strftime("%Y년 %m월 %d일 %H시 %M분")

    return "\n".join([
        "```",
        f"PST {pst}",
        f"KST {kst}",
        "```"
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

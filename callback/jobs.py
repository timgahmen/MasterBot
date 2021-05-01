from html import escape
from telegram.ext import CallbackContext

from common import get_list_of_py
from const import CONFIG


class Jobs:
    @staticmethod
    def supervisor(context: CallbackContext):
        if "prev_bot_list" not in context.bot_data:
            # load "prev_bot_list" for the first time
            context.bot_data["prev_bot_list"] = {
                bot for bot in get_list_of_py(only_alias=True)
            }
            context.bot_data["current_bot_list"] = {
                bot for bot in get_list_of_py(only_alias=True)
            }
        else:
            # shift the "current" to "prev" and fetch "new" as "current"
            context.bot_data["prev_bot_list"] = context.bot_data["current_bot_list"]
            context.bot_data["current_bot_list"] = {
                bot for bot in get_list_of_py(only_alias=True)
            }

            failed_bots = (
                context.bot_data["prev_bot_list"] - context.bot_data["current_bot_list"]
            )
            if failed_bots:
                failed_bots_list = "\n\t".join(escape(bot) for bot in failed_bots)
                to_send = (
                    f"<b>Attention, Master!</b>"
                    f"\nSome bots aren't running now or have escaped our hold, (compared to the prev. list)"
                    f"\n"
                    f"\n<pre>Alias</pre>"
                    f"\n"
                    f"\n\t{failed_bots_list}"
                    f"\n"
                    f"\nI don't have the permission to start bots, please login to the VPS at your convenience"
                )
                for admin in CONFIG.ADMINS:
                    try:
                        context.bot.send_message(chat_id=admin, text=to_send, parse_mode="HTML")
                    except: pass

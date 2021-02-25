#

import constant
import time
import re
import signal_cli as signal
import utils
from utils import n_none
import sched

MESSAGE_READ_INTERVAL_S = 60
scheduler = sched.scheduler(time.time, time.sleep)
cmds_functions = {}


def reschedule_processing():
    scheduler.enter(MESSAGE_READ_INTERVAL_S, 1, read_and_process_messages(), ())


def parse_arguments(msg):
    match = re.search(constant.BOT_CMD_ARGUMENT_REGEX, msg)
    if n_none(match) and len(match.groups()) > 1:
        return match.group(1).split(' ')
    return None


def read_and_process_messages():
    for msg in signal.get_parsed_messages(constant.BOT_NUMBER):
        print('processing message' + str(msg))
        response_msg = None
        for cmd in cmds_functions.keys():
            if msg.message.startswith(cmd):
                response_msg = cmds_functions[cmd](parse_arguments(msg.message))
                break

        if n_none(response_msg) and response_msg != '':
            signal.send_message(constant.BOT_NUMBER, msg.source, utils.sanitize(response_msg), None)

    reschedule_processing()


def add_command(cmd, function):
    global cmds_functions
    cmds_functions[cmd] = function


def remove_command(cmd):
    global cmds_functions
    cmds_functions.pop(cmd)


def start_message_processing():
    reschedule_processing()
    scheduler.run()

if __name__ == '__main__':
    bot_commands.init()

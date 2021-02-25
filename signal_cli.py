import constant
import os
import utils
from utils import n_none

########################################################
#                      OS COMMANDS                     #
########################################################
PROGRAM_PATH = '..\\..\\signal-cli-0.6.8\\bin\\'
PROGRAM = PROGRAM_PATH + 'signal-cli.bat -u {}'
#PROGRAM = 'signal-cli -u {}'

CMD_SEND = ' send {}'
CMD_RECEIVE = ' receive --json'

OPT_MESSAGE = ' -m "{}"'
OPT_ATTACHMENT = ' -a {}'
OUTPUT = ' > {}'


def send_message(sender, recipient, message, attachment_file_name):
    cmd = PROGRAM.format(sender)
    cmd += CMD_SEND.format(recipient)

    if message is None:
        message = ''

    cmd += OPT_MESSAGE.format(message)

    if attachment_file_name is not None:
        cmd += OPT_ATTACHMENT.format(attachment_file_name)

    print('Executing command: \'{}\''.format(cmd))
    ret_val = os.system(cmd)
    if ret_val == 0:
        print('Sending message successful')
    else:
        print('ERROR Sending message failed ({})'.format(ret_val))


def receive(sender):
    return receive(sender, None)


def receive(sender, output_file):
    cmd = PROGRAM.format(sender)
    cmd += CMD_RECEIVE
    if output_file:
        cmd += OUTPUT.format(output_file)
    os.system(cmd)


def get_messages(sender, messages_only):
    receive(sender, constant.FILE_NAME_OPT_MESSAGE_DB)
    messages = []
    with open(constant.FILE_NAME_OPT_MESSAGE_DB) as input_file:
        for line in input_file:
            while True:
                try:
                    message = utils.json2obj(line)
                    if not messages_only:
                        messages.append(message)
                    elif n_none(message) and n_none(message.envelope) and (n_none(message.envelope.dataMessage) or n_none(message.envelope.syncMessage)):
                        messages.append(message)
                    break
                except ValueError:
                    # Not yet a complete JSON value
                    line += next(input_file)

    return messages


def parse_data_message(raw_msg):
    group_id = None
    return utils.json_object_hook({
        'source': raw_msg.envelope.source,
        'group_id': group_id,
        'message': raw_msg.envelope.dataMessage.message,
        'timestamp': raw_msg.envelope.dataMessage.timestamp
    })


def parse_sync_message(raw_msg):
    group_id = None
    if n_none(raw_msg.envelope.syncMessage.sentMessage):
        if n_none(raw_msg.envelope.syncMessage.sentMessage.groupInfo):
            group_id = raw_msg.envelope.syncMessage.sentMessage.groupInfo.groupId
        return utils.json_object_hook({
            'source': raw_msg.envelope.source,
            'group_id': group_id,
            'message': raw_msg.envelope.syncMessage.sentMessage.message,
            'timestamp': raw_msg.envelope.syncMessage.sentMessage.timestamp
        })


def get_parsed_messages(sender):
    raw_msgs = get_messages(sender, True)
    messages = []

    for raw_msg in raw_msgs:
        if n_none(raw_msg.envelope.dataMessage):
            messages.append(parse_data_message(raw_msg))
        elif n_none(raw_msg.envelope.syncMessage) and n_none(raw_msg.envelope.syncMessage.sentMessage):
            messages.append(parse_sync_message(raw_msg))
        else:
            print('Failed to parse message: ' + str(raw_msg))

    return messages

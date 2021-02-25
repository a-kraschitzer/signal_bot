import constant
from datetime import datetime
import external_api as api
import signal_cli as cli
import random
import sys
import utils

########################################################
#                   MESSAGE STRINGS                    #
########################################################
STRINGS_ADJECTIVES = ['beautiful', 'super duper fine', 'pretty', 'as pretty as a picture', 'attractive', 'good-looking', 'appealing', 'adorable', 'exquisite', 'sweet', 'charming', 'enchanting', 'engaging', 'bewitching', 'winsome', 'seductive', 'gorgeous', 'alluring', 'ravishing', 'glamorous', 'bonny', 'tasty', 'knockout', 'stunning', 'drop-dead gorgeous', 'adorbs', 'smashing', 'cute', 'foxy', 'beauteous', 'comely', 'fair', 'sightly', 'pulchritudinous', 'scenic', 'picturesque', 'pleasing', 'easy on the eye', 'magnificent', 'splendid', 'enjoyable', 'delightful', 'pleasant', 'nice', 'marvellous', 'wonderful', 'sublime', 'superb', 'fine', 'magical', 'enchanting', 'captivating', 'terrific', 'fabulous', 'fab', 'heavenly', 'divine', 'amazing', 'glorious', 'yaaaas', 'lovely', 'funny', 'loving']
STRINGS_MSG_GENERAL = ['You are {}!']
STRINGS_MSG_MORNING = STRINGS_MSG_GENERAL + ['Good morning {} fiancee!']
STRINGS_MSG_MIDDAY = STRINGS_MSG_GENERAL + ['Hope you have a great day {} fiancee!']
STRINGS_MSG_EVENING = STRINGS_MSG_GENERAL + ['Hope you had a great day {} fiancee!']


def get_base_msg():
    current_hour = datetime.now().hour

    if 8 <= current_hour < 11:
        msg = utils.get_random_element(STRINGS_MSG_MORNING)
    elif current_hour < 18:
        msg = utils.get_random_element(STRINGS_MSG_MIDDAY)
    elif current_hour < 23:
        msg = utils.get_random_element(STRINGS_MSG_EVENING)
    else:
        msg = utils.get_random_element(STRINGS_MSG_GENERAL)

    msg = msg.format(utils.get_random_element(STRINGS_ADJECTIVES))
    print('Base message prepared: \'{}\''.format(msg))
    return msg


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1].isdigit():
        extra_rand = int(sys.argv[1])
    else:
        extra_rand = random.randrange(5)

    message = get_base_msg()
    attachment_file_name = None

    try:
        if extra_rand == 4:
            message = message + '\n_\n' + api.get_trivia_question()
        elif extra_rand == 3:
            message = message + '\n_\n' + api.get_jeopardy_question()
        elif extra_rand == 2:
            message = message + '\n_\n' + api.get_quote()
        else:
            attachment_file_name = api.get_dog_picture()
    except:
        try:
            attachment_file_name = api.get_dog_picture()
        except:
            message = message + '\n_\n something went wrong :(,\nlet the admin know ;)'

    cli.send_message(constant.BOT_NUMBER, constant.NUMBER_RECEIVER, message, attachment_file_name)

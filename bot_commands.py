# This file processes the commands issued through messages received by the bot

import bot
import constant
import external_api as api
import random
from utils import n_none

trivia_question = None
jeopardy_question = None


def handle_horoscope(arguments):
    return api.get_horoscope()


def handle_horoscope(arguments):
    return api.get_horoscope()


def handle_jeopardy_question(arguments):
    global jeopardy_question
    jeopardy_question = api.get_jeopardy_question_raw()
    return jeopardy_question.question


def handle_jeopardy_question_answer(arguments):
    global jeopardy_question
    response_msg = ''
    if n_none(jeopardy_question):
        response_msg = response_msg + jeopardy_question.answer
    else:
        response_msg = 'No question has been asked.'
    return response_msg


def handle_trivia_question(arguments):
    global trivia_question
    trivia_question = api.get_trivia_question_raw()
    question_msg = trivia_question.question
    if n_none(trivia_question.incorrect_answers):
        question_msg += '\n_\n'
        trivia_question.incorrect_answers.append(trivia_question.correct_answer)
        random.shuffle(trivia_question.incorrect_answers)
        for answer in trivia_question.incorrect_answers:
            question_msg += answer + '\n'
    return question_msg


def handle_trivia_question_answer(arguments):
    global trivia_question
    if n_none(trivia_question):
        response_msg = trivia_question.correct_answer
    else:
        response_msg = 'No question has been asked.'
    return response_msg


def init():
    bot.add_command(constant.BOT_CMD_TRIVIA_ANSWER, handle_trivia_question_answer)
    bot.add_command(constant.BOT_CMD_TRIVIA, handle_trivia_question)
    bot.add_command(constant.BOT_CMD_JEOPARDY_ANSWER, handle_jeopardy_question_answer)
    bot.add_command(constant.BOT_CMD_JEOPARDY, handle_jeopardy_question)
    bot.add_command(constant.BOT_CMD_HOROSCOPE, handle_horoscope)


def start():
    bot.start_message_processing()

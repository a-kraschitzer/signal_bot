import utils
import constant
import requests


def get_dog_picture():
    dog_breed = utils.get_random_element(constant.URLPART_DOG_BREEDS)
    dog_pic_url = requests.get(constant.URL_DOG_API.format(dog_breed)).json()['message']
    open(constant.FILE_NAME_DOG, 'wb').write(requests.get(dog_pic_url).content)
    print('File {} successfully downloaded from \'{}\''.format(constant.FILE_NAME_DOG, dog_pic_url))
    return constant.FILE_NAME_DOG


def get_trivia_question_raw():
    """
    :return: X(category='Politics', type='multiple', difficulty='hard', question='What is centralism?', correct_answer=' Concentration of power and authority in a central organization.', incorrect_answers=['Conforming to one single common political agenda.', 'Remaining politically neutral.', 'The grey area in the spectrum of political left and right.'])
    """
    return utils.json_object_hook(requests.get(constant.URL_TRIVIA_QUESTION).json()['results'][0])


def get_trivia_question():
    question = get_trivia_question_raw()
    que_string = question.question + '\n' + question.correct_answer
    print('Found trivia question: \'{}\' with answer: \'{}\''.format(question.question, question.correct_answer))
    return utils.sanitize(que_string)


def get_jeopardy_question_raw():
    """
    :return: X(id=155814, answer='Columbia University', question="This university in New York City that was founded as King's College in 1754 uses a crown as its logo", value=200, airdate='2015-03-06T12:00:00.000Z', created_at='2015-04-02T17:23:20.929Z', updated_at='2015-04-02T17:23:20.929Z', category_id=672, game_id=4840, invalid_count=None, category={'id': 672, 'title': 'colleges & universities', 'created_at': '2014-02-11T22:49:45.911Z', 'updated_at': '2014-02-11T22:49:45.911Z', 'clues_count': 145})
    """
    return utils.json_object_hook(requests.get(constant.URL_JEOPARDY_QUESTION).json()[0])


def get_jeopardy_question():
    question = get_jeopardy_question_raw()
    que_string = '[J] ' + question.question + '\n' + question.answer
    print('Found jeopardy question: \'{}\' with answer: \'{}\''.format(question.question, question.answer))
    return utils.sanitize(que_string)


def get_horoscope_raw():
    return utils.json_object_hook(requests.post(constant.URL_HOROSCOPE, '').json())


def get_horoscope():
    horoscope = get_horoscope_raw()
    print('Found horoscope: \'{}\'.'.format(horoscope.description))
    return utils.sanitize(horoscope.description)


def get_quote_raw():
    return utils.json_object_hook(requests.get(constant.URL_QUOTES).json()['quote'])


def get_quote():
    quote = get_quote_raw()
    quote_string = quote.body + '\n-' + quote.author
    print('Found quote: \'{}\' -{}'.format(quote.body, quote.author))
    return utils.sanitize(quote_string)

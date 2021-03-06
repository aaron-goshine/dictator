#! /usr/local/bin/python3

import os
from dictator import Dictator


def draw_game():
    dictor = Dictator()
    expected_word = ""
    supplied_word = ""
    message = ""
    runing = True
    current_definition = ""

    def red(text):
        return '\033[1;31m{}\033[0m'.format(text)

    def green(text):
        return '\033[1;32m{}\033[0m'.format(text)

    def blink(text):
        return '\033[5m{}\033[0m'.format(text)

    def yellow(text):
        return '\033[0;33m{}\033[0m'.format(text)

    def notice(text):
        return '\033[0;30;47m{}\033[0m'.format(text)

    while (runing):
        _, w = os.popen('stty size', 'r').read().split()
        width = int(w)
        os.system('clear')

        user = dictor.get_user()
        # Declaration of strings
        hud = " LEVEL: {}, TOP SCORE: {}".format(user['level'], user['score'])
        title = "DICTATOR \n"
        subtitle = "Written by Aaron Goshine \n"
        how_to_play = "Please listen carefully and type the words you hear\n"
        expected = "Expected word: {}".format(expected_word)
        supplied = "Supplied word: {}".format(supplied_word)
        definition = "Definition: {}".format(current_definition)

        # Rendering some text
        print(notice(hud.ljust(width - 1, ' ')))
        print(title.center(width, ' '))
        print(subtitle.center(width, ' '))
        print(('-' * (width // 2)).center(width, ' '))
        print(how_to_play.center(width, ' '))
        print(expected.center(width, ' '))
        print(supplied.center(width, ' '))
        print('\n')
        print(yellow(definition.center(width, ' ')))
        print('\n')
        print(message)

        # Refresh the screen
        has_word = dictor.next_word()
        dictor.play()
        d = yellow('d')
        c = yellow('c')
        r = yellow('r')
        y = green('y')
        n = red('n')

        template = 'Choose [{}]efinition, [{}]epeat, [{}]ontinue | word: '
        prompt = template.format(d, r, c)

        if has_word:
            ans = str.strip(str(input(prompt)))

        while ans in ['d', 'r']:
            if (str.lower(ans) == 'd'):
                dictor.play_definition()
                dictor.play()

            if (str.lower(ans) == 'r'):
                dictor.play()
            ans = str.strip(str(input(prompt)))
        typed_word = ans

        if not has_word:
            ans = str.strip(str(input(
                'Continue playing? [{}]/[{}] :'.format(y, n))))
            if(str.lower(ans) == 'y'):
                dictor = Dictator()
                has_word = dictor.next_word()
                dictor.play()
                typed_word = str.strip(str(input('Word?: ')))
            else:
                runing = False
                print(blink(('-' * (width // 2)).center(width, ' ')))
                print(yellow('!!!Catch yooo later!!!'.center(width, ' ')))
                print(blink(('-' * (width // 2)).center(width, ' ')))
                break

        results = dictor.check_word(typed_word)

        if (results):
            if (results[0]):
                message = green('Well done'.center(width, ' '))
            else:
                message = red('Try again!'.center(width, ' '))
        expected_word = results[1]
        supplied_word = results[2]
        current_definition = results[3]

__author__ = 'Paddy'

'''
Ludum Dare 33 - August 21st-24th | #LDJAM | U+2603 | Theme: You are the Monster
'''

import pygame
import settings_parse



















def main():

    """
    The main game function. Welcome to the beginning of the end.
    :return:
    """

    # First we must initialize the pygame module and game clock before most things happen
    pygame.init()
    game_clock = pygame.time.Clock()

    # Grab the settings from the settings file. They are placed in a dictionary.
    settings = settings_parse.parse_settings('settings.cfg')

if __name__ == '__main__':

    main()

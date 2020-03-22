import random

class WordBank:
    def __init__(self, word_list, timestamp):
        self.__word_list = word_list
        self.__time_of_last_modification = timestamp

    def get_time_of_last_modification(self):
        return self.__time_of_last_modification

    def overwrite_word_list(self, word_list, timestamp):
        self.__word_list = word_list
        self.__time_of_last_modification = timestamp

    def get_random_word(self):
        random_index = random.randint(0, len(self.__word_list)-1)
        return self.__word_list[random_index]
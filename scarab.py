from words_helpers import EnglishWords
import pandas as pd
import fnmatch


class Scarab(EnglishWords):
    def __init__(self, letters):
        self.letters = letters
        self.letter_values = EnglishWords.letter_values

    def __call__(self, *args, **kwargs):
        return self.words()

    def scrabble_words(self):
        valid_words = []
        for word in EnglishWords.words:
            word_data = self._valid_word(word)
            if word_data:
                valid_words.append(self._calculate_point_value(word_data))

        df = pd.DataFrame(valid_words, columns=['word', 'wild_card', 'point_value'])
        df.sort_values(['point_value', 'word'], ascending=[False, True], inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def words(self, inplace=False):
        valid_words = []

        if inplace:
            for word in EnglishWords.words:
                if self._in_place_valid_words(word):
                    valid_words.append(word)
            return valid_words

        for word in EnglishWords.words:
            word_data = self._valid_word(word)
            if word_data:
                valid_words.append(word)

        return valid_words

    def _valid_word(self, word):
        """
        Checks whether or not the word passed is a valid word. Will return the word, as well as a list of
        wild cards used to replace any '_' in self.letters
        :param word: word to be checked
        :return: The word, and any replacements in a list (if True), or False
        """
        available_letters = list(self.letters)

        wild_card_count = available_letters.count('_')
        fails = 0
        wild_cards = []

        if wild_card_count == 0:
            for letter in word:
                if letter not in available_letters:
                    return False
                else:
                    available_letters.remove(letter)

        else:
            for letter in word:
                if fails < wild_card_count:
                    if letter not in available_letters:
                        fails += 1
                        wild_cards.append(letter)
                    else:
                        available_letters.remove(letter)

                else:
                    return False

        return word, wild_cards

    def _calculate_point_value(self, word_tuple):
        letters = list(word_tuple[0])
        wild_cards = word_tuple[1]
        if wild_cards:
            for wild_card in wild_cards:
                letters.remove(wild_card)

        total_points = 0
        for letter in letters:
            point_value = self.letter_values[letter]
            total_points += point_value

        return word_tuple[0], wild_cards, total_points

    def _in_place_valid_words(self, word):
        return fnmatch.fnmatch(word, str(self.letters))


if __name__ == '__main__':
    scarab = Scarab('lkasjfdlka___')
    words = scarab.scrabble_words()
    print(words)








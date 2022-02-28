import typing
import re


class TextProcessor:

    def __get_sentences(self, text: str) -> typing.List[str]:
        """Return a list of sentences of the text."""
        text = text.replace("...", ".")

        result = re.split(r"[.,!,?]\s", text)
        result.pop()  # delete empty string

        return result

    def __get_words(self, sentence: str) -> typing.List[str]:
        """Return a list of words of the sentence."""
        return re.split(r"\s[-,--]\s|[\,,:,;]\s|\s", sentence)

    def __init__(self, text):
        self.__text = text
        self.__sentences = self.__get_sentences(text)

        self.__words = []
        for sentence in self.__sentences:
            self.__words += list(
                    map(lambda x: x.lower(),
                        self.__get_words(sentence)
                        )
                )

    def count_words_of_type(self) -> dict:
        """Return count of words of every words type in the sentence."""
        result = dict()

        for key in set(self.__words):
            result[key] = self.__words.count(key)

        return result

    def average_words_count(self) -> float:
        """Return average word count in the sentences."""
        return len(self.__words) / len(self.__sentences)

    def median_words_count(self) -> float:
        """Return median word count in the sentences."""
        words_counts = []

        for sentence in self.__sentences:
            words_counts.append(len(self.__get_words(sentence)))

        words_counts.sort()
        counts_len = len(words_counts)

        if(counts_len % 2 == 0):
            return (
                words_counts[counts_len / 2 - 1] + words_counts[counts_len / 2]
                ) / 2

        return words_counts[counts_len // 2]

    def get_top_ngramms(self, n=4, ktop=10) -> dict:
        """Return top k n-gramms in the text."""
        result = {}

        def count_anagramms(word: str) -> None:
            word_len = len(word)

            for i in range(word_len):
                if i + n > word_len:
                    break

                anagramm = word[i:i + n]
                result[anagramm] = self.__text.count(anagramm)

        # creating a dict of n-gramms
        for word in self.__words:
            count_anagramms(word)

        # getting top k of n-gramms
        while(len(result) > ktop):
            result_keys = list(result.keys())
            min_key = result_keys[0]

            for key in result_keys[1:]:
                if(result[key] < result[min_key]):
                    min_key = key

            result.pop(min_key)

        return result

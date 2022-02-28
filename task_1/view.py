import entity


class View:
    def __init__(self, filename: str):
        with open(filename) as file:
            self.__text = file.read()

        self.__text_processor = entity.TextProcessor(self.__text)

    def start(self) -> None:
        """Start dialog with user."""
        print(self.__text)
        print(
            "Words types count: ",
            self.__text_processor.count_words_of_type()
            )
        print(
            "Average words count in sentenses: ",
            self.__text_processor.average_words_count()
            )
        print(
            "Median words count in sentenses: ",
            self.__text_processor.median_words_count()
            )

        try:
            k, n = map(
                int,
                input(
                    "Enter k and n for top anagramms(if don't, left empty): "
                    ).split()
            )
        except ValueError:
            k, n = 10, 4

        print("Top anagramms: ", self.__text_processor.get_top_ngramms(n, k))

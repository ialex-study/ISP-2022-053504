import re


def get_sentenses(text):
    text = text.replace("...", ".")

    result = re.split(r"[.,!,?]\s", text)
    result.pop()  # delete empty string

    return result


def get_words(sentense):
    return re.split(r"\s[-,--]\s|[\,,:,;]\s|\s", sentense)


def count_words_of_type(text):
    result = dict()

    words = []

    for sentense in get_sentenses(text):
        words += list(map(lambda x: x.lower(), get_words(sentense)))

    for key in set(words):
        result[key] = words.count(key)

    return result


def average_words_count(text):
    sentenses = get_sentenses(text)

    result = 0

    for sentense in sentenses:
        result += len(get_words(sentense))

    return result / len(sentenses)


def median_words_count(text):
    sentenses = get_sentenses(text)

    words_counts = []

    for sentense in sentenses:
        words_counts.append(len(get_words(sentense)))

    words_counts.sort()
    counts_len = len(words_counts)

    if(counts_len % 2 == 0):
        return (
            words_counts[counts_len / 2 - 1] + words_counts[counts_len / 2]
            ) / 2

    return words_counts[counts_len // 2]


def get_top_ngramms(text, n=4, ktop=10):
    result = {}

    def count_anagramms(word):
        word_len = len(word)

        for i in range(word_len):
            if i + n > word_len:
                break

            anagramm = word[i:i + n]
            result[anagramm] = text.count(anagramm)

    for sentense in get_sentenses(text):
        for word in get_words(sentense):
            count_anagramms(word)

    while(len(result) > ktop):
        result_keys = list(result.keys())
        min_key = result_keys[0]

        for key in result_keys[1:]:
            if(result[key] < result[min_key]):
                min_key = key

        result.pop(min_key)

    return result


if __name__ == "__main__":
    with open("text.txt") as file:
        text = file.read()

    print(text)
    print("Words types count: ", count_words_of_type(text))
    print("Average words count in sentenses: ", average_words_count(text))
    print("Median words count in sentenses: ", median_words_count(text))

    try:
        k, n = map(
            int,
            input(
                "Enter k and n for top anagramms(if don't, left empty): "
                ).split()
        )
    except ValueError:
        k, n = 10, 4

    print("Top anagramms: ", get_top_ngramms(text, n, k))

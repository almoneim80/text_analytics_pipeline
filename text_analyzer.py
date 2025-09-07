import statistics as stats
import string
import collections

data_dictionary = {}


# cleaning text
def clean_text(dirty_text):
    symbols = string.punctuation + ":>,<،.#’”…“—?؟" + "0123456789" + '\n\t\r'
    cleaned_text = dirty_text.translate(str.maketrans('', '', symbols))
    return cleaned_text


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# words count
def words_count(text):
    if len(convert_to_list(text)) <= 1:
        return 0
    return len(convert_to_list(text))


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# characters count
def chars_count(text):
    return len(text)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Popular word
def popular_word(text, word_characters=1):
    if len(convert_to_list(text)) <= 1:
        return None

    if word_characters < 1 or word_characters not in words_length(text):
        return "Word Characters is invalid"
    elif word_characters > 1:
        return collections.Counter(filtered_words_by_char_num(text, word_characters)).most_common(1)[0][0]
    else:
        return stats.mode(convert_to_list(text))


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# top mode words
def top_popular_words(text, num_of_tops=2, word_characters=1):
    if len(convert_to_list(text)) <= 1:
        return None

    top_mode = []
    i = 1

    if word_characters < 1:
        return "Word Characters can not be less than 1"
    elif word_characters > 1:
        all_words = filtered_words_by_char_num(text, word_characters)
    else:
        all_words = convert_to_list(text)

    for top in collections.Counter(all_words).most_common(num_of_tops):
        top_mode = top_mode + [top[0]]

    return top_mode


def words_length_avg(text):
    total_length = 0
    length_avg = 0
    text_lengths = words_length(text)

    for length in text_lengths:
        total_length = total_length + length

    length_avg = total_length / len(convert_to_list(text))
    return length_avg


# <<<<<<<<<<<<>>>>>>>>>>>>
# helpe methods
def filtered_words_by_char_num(text, word_characters):
    filtered_words = []

    # filter words by number of characters
    for word in text.split(' '):
        if len(word) > word_characters:
            filtered_words.append(word)

    return filtered_words


def filter_to_remove(coming_words_list, word):
    words_list_after_filter = coming_words_list

    for w in coming_words_list:
        if word == w:
            words_list_after_filter.remove(w)

    return words_list_after_filter


def convert_to_list(text):
    return list(text.split(' '))


def words_length(text):
    lengths_list = []
    for word in convert_to_list(text):
        lengths_list.append(len(word))

    return lengths_list


def prepare_outputs(text, file_number, support_clean, support_statistics, characters_of_popular_word,
                    number_top_popular_words, character_per_top_word):
    print("\n----------------text before clean --------------------")
    print(text)

    if support_clean:
        print("\n----------------text after clean --------------------")
        print(clean_text(text))

    if support_statistics:
        print("\n----------------statistics --------------------")
        print("words count in text : ", words_count(clean_text(text)))
        print("characters count in text : ", chars_count(clean_text(text)))
        print("Popular word in text : ", popular_word(clean_text(text), characters_of_popular_word))
        print("Top mode words in text : ",
              top_popular_words(clean_text(text), number_top_popular_words, character_per_top_word))
        print("Words length average: ", words_length_avg(clean_text(text)))

    data_dictionary.update(
        {
            "file_number": file_number,
            "clean_text": clean_text(text),
            "words_count": words_count(clean_text(text)),
            "chars_count": chars_count(clean_text(text)),
            "popular_word": popular_word(text, characters_of_popular_word),
            "top_mode_words": top_popular_words(text, number_top_popular_words),
        }
    )


def outputs(text, file_number, support_clean=True, support_statistics=True, characters_of_popular_word=1,
            number_top_popular_words=2, character_per_top_word=1):
    print("##############################")
    print("#       file number:         #")
    print(f"#            {file_number}               #")
    print("##############################")
    prepare_outputs(text, file_number, support_clean, support_statistics, characters_of_popular_word,
                    number_top_popular_words,
                    character_per_top_word)
    print("\n\n")


def out_to_file():
    with open(f'outputs/file-{data_dictionary["file_number"]}_analyzer_outputs.json', 'w',
              encoding="utf-8") as json_file:
        json_file.write(str(data_dictionary))


def top_popular_words_to_csv():
    with open(f'outputs/file-{data_dictionary["file_number"]}top_popular_words.csv', 'w',
              encoding="utf-8") as csv_file:
        csv_file.write(str(data_dictionary["top_mode_words"]))

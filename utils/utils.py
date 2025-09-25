import string

# cleaning text
def clean_text(dirty_text):
    """
    Cleans the input text by removing punctuation, special symbols, digits, and whitespace characters.

    Parameters:
    dirty_text (str): The text string to be cleaned.

    Returns:
    str: The cleaned text with all specified symbols, digits, and newline/tab/carriage return characters removed.

    Example:
    >>> clean_text("Hello, world! 123")
    'Hello world '
    """
    symbols = string.punctuation + ":>,<،.#’”…“—?؟" + "0123456789" + '\n\t\r'
    cleaned_text = dirty_text.translate(str.maketrans('', '', symbols))
    return cleaned_text


def filtered_words_by_char_num(text, word_characters):
    """
    Filters words in a given text that have more characters than the specified threshold.

    Parameters:
    text (str): The input text containing words separated by spaces.
    word_characters (int): The minimum number of characters a word must have to be included.

    Returns:
    list: A list of words from the input text that have more characters than 'word_characters'.

    Example:
    >>> filtered_words_by_char_num("I love programming in Python", 4)
    ['programming', 'Python']
    """

    filtered_words = []

    # filter words by number of characters
    for word in text.split(' '):
        if len(word) > word_characters:
            filtered_words.append(word)
    return filtered_words

def filter_to_remove(coming_words_list, word):
    """
    Removes all occurrences of a specific word from a given list of words.

    Parameters:
    coming_words_list (list): The list of words to filter.
    word (str): The word to remove from the list.

    Returns:
    list: A new list containing the words from the original list except the specified word.

    Example:
    >>> filter_to_remove(['apple', 'banana', 'apple', 'cherry'], 'apple')
    ['banana', 'cherry']
    """

    return [w for w in coming_words_list if w != word]


def convert_to_list(text):
    """
    Converts a string of text into a list of words, splitting by spaces.

    Parameters:
    text (str): The input string containing words separated by spaces.

    Returns:
    list: A list of words extracted from the input text.

    Example:
    >>> convert_to_list("Hello world from Python")
    ['Hello', 'world', 'from', 'Python']
    """

    translator = str.maketrans('', '', string.punctuation + "،’”…“—؟")
    cleaned_text = text.translate(translator)
    words = cleaned_text.strip().split()
    return words


def words_length(text):
    """
    Returns a list of lengths for each word in the given text.

    Parameters:
    text (str): The input string containing words separated by spaces.

    Returns:
    list: A list of integers representing the length of each word in the text.

    Example:
    >>> get_word_lengths("Hello world from Python")
    [5, 5, 4, 6]
    """
    lengths_list = [len(word) for word in convert_to_list(text)]
    return lengths_list
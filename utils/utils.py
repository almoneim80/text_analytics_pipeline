import string
import re
import emoji
from utils.logger import get_logger
logger = get_logger("utils")


# cleaning text
def clean_text(dirty_text: str, normalize_text: bool, rlen: bool):
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
    logger.info("From clean_text method: Before Cleaning text : len=%d | preview=%r", len(dirty_text), dirty_text[:200])
    symbols = string.punctuation + ":>,<،.#’”…“—?؟" + "0123456789" + '\n\t\r'
    cleaned_text = dirty_text.translate(str.maketrans('', '', symbols))

    if normalize_text:
        cleaned_text = normalize_arabic(cleaned_text)

    if rlen:
        cleaned_text = remove_links_emojis_numbers(cleaned_text)

    logger.info("From clean_text method: After Cleaning text : len=%d | preview=%r", len(cleaned_text), cleaned_text[:200])
    return cleaned_text


def filtered_words_by_char_num(text: str, word_characters: int):
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


def filter_to_remove(coming_words_list: list[str], word: str):
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


def convert_to_list(text: str):
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


def words_length(text: str):
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


def normalize_arabic(text: str):
    # Removing the mold
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652\u0670]', '', text)
    # Unification of the letters 
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ؤ', 'و', text)
    text = re.sub(r'ئ', 'ي', text)
    text = re.sub(r'ة', 'ه', text)

    text = re.sub(r'[^\w\s]', '', text)

    text = re.sub(r'\s+', ' ', text).strip()
    return text


def remove_links_emojis_numbers(text: str):
    """
    Improved text cleaning: removal of links, emojis, Arabic and English numbers, and reduction of excess spaces.
    """

    # Removing links
    text = re.sub(r'https?://\S+|www\.\S+|\b\S+\.(com|net|org|edu|gov)\b', '', text)
    # Remove emoji
    text = emoji.replace_emoji(text, replace='')
    # Remove numbers
    text = re.sub(r'[0-9٠-٩]+', '', text)

    # Reduce excess white space
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def remove_stopwords(words_list: list[str], stopwords: list[str], prefixes: list[str]) -> list[str]:
    """
    Remove stopwords and specific prefixes from a list of words.

    This function cleans a list of words by:
      1. Removing defined prefixes (e.g., "ال", "ب", "و") if present at the start of a word.
      2. Excluding words that appear in the stopwords list.

    Args:
        words_list (list[str]): List of words to process.
        stopwords (list[str]): List of stopwords to remove.
        prefixes (list[str]): List of prefixes to strip from words before filtering.

    Returns:
        list[str]: List of cleaned words with prefixes and stopwords removed.

    Example:
        >>> remove_stopwords(["المدرسة", "جميلة", "و", "النظافة"], ["و"], ["ال"])
        ['مدرسة', 'جميلة', 'نظافة']
    """
    filtered_words = []
    for word in words_list:
        for prefix in prefixes:
            if word.startswith(prefix) and len(word) > len(prefix):
                word = word[len(prefix):]
                break

        if word not in stopwords:
            filtered_words.append(word)

    return filtered_words


def split_text_by_language(text: str) -> tuple[str, str]:
    """
    Split a multilingual text into separate English and Arabic segments.

    The function detects and extracts Arabic and English words using
    Unicode and regex patterns, returning two distinct strings.

    Args:
        text (str): The input text containing mixed Arabic and/or English content.

    Returns:
        tuple[str, str]: A tuple (english_text, arabic_text) where:
            - english_text (str): Contains all detected English words.
            - arabic_text (str): Contains all detected Arabic words.

    Example:
        >>> split_text_by_language("Welcome مرحباً بك")
        ('Welcome', 'مرحباً بك')
    """
    arabic_chars = re.findall(r'[\u0600-\u06FF]+', text)
    english_chars = re.findall(r'[A-Za-z]+', text)

    arabic_text = " ".join(arabic_chars)
    english_text = " ".join(english_chars)

    return english_text, arabic_text

import pytest
from analyzer import text_analyzer as ta
import utils.utils  as ut

analyzer = ta.TextAnalyzer()

def test_chars_count():
    cleaned_text = "Hello world"  # Cleaned text
    chars = analyzer._chars_count(cleaned_text)
    
    assert chars == len(cleaned_text)
    assert analyzer.results["chars_count"] == len(cleaned_text) # check if the result updated success.


def test_words_length_avg():
    cleaned_text = "Hello world from Python"
    avg_length = analyzer._words_length_avg(cleaned_text)
    
    # Calculating the expected average height manually
    expected_lengths = [5, 5, 4, 6]  # Length of each word
    expected_avg = sum(expected_lengths) / len(expected_lengths)
    
    assert avg_length == expected_avg
    # Check for updates results
    assert analyzer.results["words_length_avg"] == expected_avg


def test_top_popular_words():
    cleaned_text = "apple banana apple cherry banana apple"
    
    # two most common words.
    top_words = analyzer._top_popular_words(cleaned_text, word_characters=1, num_of_top_words=2)
    expected_top_words = ["apple", "banana"]
    
    assert top_words == expected_top_words
    # Verify that results has been updated correctly.
    assert analyzer.results["top_popular_words"] == expected_top_words


def test_popular_word():
    cleaned_text = "apple banana apple cherry banana apple"

    analyzer = ta.TextAnalyzer()

    # Condition word_characters > 1
    popular = analyzer._popular_word(cleaned_text, word_characters=2)
    assert popular == "apple"

    # Condition word_characters <= 1 (All words are valid)
    popular_all = analyzer._popular_word(cleaned_text, word_characters=1)
    assert popular_all == "apple"

    # Condition word_characters > Length of any word (no words)س
    popular_none = analyzer._popular_word(cleaned_text, word_characters=10)
    assert popular_none == "No words with given character length"


def test_words_count():
    analyzer = ta.TextAnalyzer()

    # Normal text
    text = "apple banana cherry"
    count = analyzer._words_count(text)
    assert count == 3

    # Blank text
    text_empty = ""
    cleaned_text_empty = ut.clean_text(text_empty)
    count_empty = analyzer._words_count(cleaned_text_empty)
    assert count_empty == 0

    # One-word text
    text_one = "apple"
    count_one = analyzer._words_count(text_one)
    assert count_one == 1


def test_analyze():
    analyzer = ta.TextAnalyzer()
    
    text = "apple banana apple cherry"
    results = analyzer.analyze(text, file_number=1, num_of_top_words=2, word_characters=2)
    
    assert results["words_count"] == 4
    assert results["chars_count"] == len(ut.clean_text(text))
    assert results["top_popular_words"] == ["apple", "banana"]
    assert results["popular_word"] == "apple"
    assert "words_length_avg" in results

    # Blank Text Test
    results_empty = analyzer.analyze("", file_number=2)
    assert results_empty["words_count"] == 0
    assert results_empty["chars_count"] == 0
    assert results_empty["top_popular_words"] == []
    assert results_empty["popular_word"] is None

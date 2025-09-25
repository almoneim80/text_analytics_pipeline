import pytest
from utils import utils as ut

def test_clean_text_removes_punctuatio_and_digits():
    text = "Hello, world! 123"
    cleaned = ut.clean_text(text)
    assert cleaned == "Hello world "

def test_filtered_words_by_char_num():
    text = "I love programming in Python"
    filtered = ut.filtered_words_by_char_num(text, 4)
    assert filtered == ["programming", "Python"]

def test_filter_to_remove():
    words = ["apple", "banana", "apple", "cherry"]
    filtered = ut.filter_to_remove(words, "apple")
    assert filtered == ["banana", "cherry"]

def test_convert_to_list_removes_punctuation():
    text = "Hello, world! Python."
    words = ut.convert_to_list(text)
    assert words == ["Hello", "world", "Python"]

def test_words_length():
    text = "Hello world from Python"
    lengths = ut.words_length(text)
    assert lengths == [5, 5, 4, 6]
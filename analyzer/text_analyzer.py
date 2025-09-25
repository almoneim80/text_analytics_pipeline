import statistics as stats
import collections
import utils.utils  as ut
import logging

# logging config
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

class TextAnalyzer():
    def __init__(self):

        self.results = {}

    # characters count
    def _chars_count(self, cleaned_text):
        number_of_chars = len(cleaned_text)
        self.results.update({"chars_count": number_of_chars})
        return number_of_chars
        
    # the average of words length
    def _words_length_avg(self, cleaned_text):
        total_length = 0
        length_avg = 0
        lengths = ut.words_length(cleaned_text)
        length_avg = sum(lengths) / len(lengths) if lengths else 0
        self.results["words_length_avg"] = length_avg
        return length_avg
        
    # top mode words
    def _top_popular_words(self, cleaned_text, word_characters, num_of_top_words):
        top_mode = []
        i = 1

        if len(ut.convert_to_list(cleaned_text)) <= 1:
            return None
            
        if word_characters < 1:
            return "Word Characters can not be less than 1"
        elif word_characters > 1:
            all_words = ut.filtered_words_by_char_num(cleaned_text, word_characters)
        else:
            all_words = ut.convert_to_list(cleaned_text)

        for top in collections.Counter(all_words).most_common(num_of_top_words):
            top_mode = top_mode + [top[0]]

        self.results.update({"top_popular_words": top_mode})
        return top_mode
        
    # Popular word
    def _popular_word(self, cleaned_text, word_characters):
        words = ut.convert_to_list(cleaned_text)
        if len(words) <= 1:
            return None

        if word_characters <= 1:
            populars = stats.mode(words)
            self.results.update({"popular_word": populars})
            return populars
        else:
            filtered_words = ut.filtered_words_by_char_num(cleaned_text, word_characters)
            if not filtered_words:
                self.results.update({"popular_word": "No words with given character length"})
                return "No words with given character length"
            populars = collections.Counter(filtered_words).most_common(1)[0][0]
            self.results.update({"popular_word": populars})
            return populars
            

    # words count
    def _words_count(self, cleaned_text):
        if len(ut.convert_to_list(cleaned_text)) < 1:
            return 0
        counts = len(ut.convert_to_list(cleaned_text))
        self.results.update({"words_count": counts})
        return counts
    
    def analyze(self, text, file_number = 1, num_of_top_words = 2, word_characters = 1, support_statistics = True, support_clean = True):
        cleaned_text = ut.clean_text(text)
        if not cleaned_text.strip():
            self.results.update({
                "words_count": 0,
                "chars_count": 0,
                "words_length_avg": 0,
                "popular_word": None,
                "top_popular_words": []})
            logging.warning("Text is empty")

        self.results.update({"file_number": file_number})
        self.results.update({"orginal_text": text})
        self.results.update({"cleaned_text": cleaned_text})
        self.results.update({"support_statistics": support_statistics})
        self.results.update({"support_clean": support_clean})
    
        self._chars_count(cleaned_text)
        self._words_length_avg(cleaned_text)
        self._top_popular_words(cleaned_text, word_characters, num_of_top_words)
        self._popular_word(cleaned_text, word_characters)
        self._words_count(cleaned_text)

        return self.results
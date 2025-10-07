import statistics as stats
import collections
import utils.utils as ut
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

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


class TextAnalyzer:
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
    def _top_popular_words(self, cleaned_text, word_characters, num_of_top_words, stopwords, prefixes):
        words = ut.convert_to_list(cleaned_text)
        if not words:
            self.results.update({"top_popular_words": []})
            return []

        if word_characters > 1:
            words = ut.filtered_words_by_char_num(words, word_characters)

        if stopwords:
            words = ut.remove_stopwords(words, stopwords, prefixes)

        counter = collections.Counter(words)
        top_mode = counter.most_common(num_of_top_words)

        self.results.update({"top_popular_words": top_mode})
        return top_mode

    # Popular word
    def _popular_word(self, cleaned_text, word_characters, stopwords, prefixes):
        # check if text is just less than or equal one word.
        if len(ut.convert_to_list(cleaned_text)) <= 1:
            return None

        if word_characters <= 1:
            logging.warning("Word Characters can not be less than 1")
            return "Word Characters can not be less than 1"
        else:
            filtered_words = ut.filtered_words_by_char_num(cleaned_text, word_characters)
            if not filtered_words:
                self.results.update({"popular_word": "No words with given character length"})
                return "No words with given character length"

            if len(stopwords) > 0:
                filtered_words = ut.remove_stopwords(filtered_words, stopwords, prefixes)

            popular_word = collections.Counter(filtered_words).most_common(1)[0][0]
            self.results.update({"popular_word": popular_word})
            return popular_word

    # words count
    def _words_count(self, cleaned_text):
        if len(ut.convert_to_list(cleaned_text)) < 1:
            return 0
        counts = len(ut.convert_to_list(cleaned_text))
        self.results.update({"words_count": counts})
        return counts

    # extract Popular phases
    def _popular_phrases(self, cleaned_text, ngrams_size):
        popular_phrases = []

        # check if text is just less than or equal one word.
        words = ut.convert_to_list(cleaned_text)
        if len(words) <= 1:
            return None

        if ngrams_size <= 1:
            logging.warning("Ngrams size can not be less than 1")
            return "Ngrams size can not be less than 1"

        phrases = [" ".join(words[i:i + ngrams_size]) for i in range(len(words) - ngrams_size + 1)]

        for phrase, count in collections.Counter(phrases).most_common():
            if count > 1:
                popular_phrases.append((phrase, count))

        self.results.update({"popular_phrases": popular_phrases})
        return popular_phrases

    # TF-IDF
    def _calculate_tfidf(self, documents, stopwords, tfidf_ngram_range):
        if isinstance(tfidf_ngram_range, list):
            tfidf_ngram_range = tuple(tfidf_ngram_range)

        vectorizer = TfidfVectorizer(stop_words=stopwords, ngram_range=tfidf_ngram_range)

        tfidf_matrix = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names_out()

        tfidf_values = tfidf_matrix.toarray()
        avg_tfidf = np.mean(tfidf_values, axis=0)

        tfidf_scores = list(zip(feature_names, avg_tfidf))
        tfidf_scores.sort(key=lambda x: x[1], reverse=True)

        self.results["tfidf_scores"] = tfidf_scores
        return tfidf_scores

        # main method
    def analyze(
            self, text, stopwords, prefixes, tfidf_ngram_range, file_number=1, num_of_top_words=2, word_characters=1,
            support_statistics=True, support_clean=True, normalize_text=False, rlen=True, ngrams_size=2):
        cleaned_text = ut.clean_text(text, normalize_text, rlen)
        if not cleaned_text.strip():
            self.results.update({
                "words_count": 0,
                "chars_count": 0,
                "words_length_avg": 0,
                "popular_word": None,
                "top_popular_words": [],
                "popular_phrases": [],
                "tfidf_scores": []
            })
            logging.warning("Text is empty")

        self.results.update({"file_number": file_number})
        self.results.update({"original_text": text})
        self.results.update({"cleaned_text": cleaned_text})
        self.results.update({"support_statistics": support_statistics})
        self.results.update({"support_clean": support_clean})

        self._chars_count(cleaned_text)
        self._words_length_avg(cleaned_text)
        self._top_popular_words(cleaned_text, word_characters, num_of_top_words, stopwords, prefixes)
        self._popular_word(cleaned_text, word_characters, stopwords, prefixes)
        self._words_count(cleaned_text)
        self._popular_phrases(cleaned_text, ngrams_size)

        english_text, arabic_text = ut.split_text_by_language(cleaned_text)
        documents = [t for t in [english_text, arabic_text] if t.strip()]
        self._calculate_tfidf(documents, stopwords, tfidf_ngram_range)

        return self.results

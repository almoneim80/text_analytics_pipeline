import collections

import utils.utils as ut
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from utils.logger import get_logger

logger = get_logger("analyzer")


class TextAnalyzer:
    def __init__(self):
        self.results = {}

    # characters count
    def _chars_count(self, cleaned_text: str) -> int:
        """
        Calculate and store the total number of characters in the cleaned text.

        Args:
            cleaned_text (str): The text after cleaning and normalization.

        Returns:
            int: Number of characters in the text.

        Side Effects:
            Updates self.results["chars_count"].
        """
        number_of_chars = len(cleaned_text)
        self.results.update({"chars_count": number_of_chars})
        return number_of_chars

    # the average of words length
    def _words_length_avg(self, cleaned_text: str) -> float:
        """
        Compute and store the average word length in the cleaned text.

        Args:
            cleaned_text (str): The text after cleaning.

        Returns:
            float: Average length of words. Returns 0 if text has no words.

        Side Effects:
            Updates self.results["words_length_avg"].
        """
        lengths = ut.words_length(cleaned_text)
        length_avg = sum(lengths) / len(lengths) if lengths else 0
        self.results["words_length_avg"] = length_avg
        return length_avg

    # top mode words
    def _top_popular_words(self, cleaned_text: str, word_characters: int, num_of_top_words: int, stopwords: list[str],
                           prefixes: list[str]) -> list[tuple[str, int]]:
        """
        Extract the most frequent words in the cleaned text.

        Filters words by minimum character count, removes stopwords and prefixes,
        and returns the top-N most frequent ones.

        Args:
            cleaned_text (str): The input text to analyze.
            word_characters (int): Minimum number of characters allowed in a word.
            num_of_top_words (int): Maximum number of top frequent words to return.
            stopwords (list[str]): List of stopwords to exclude.
            prefixes (list[str]): List of prefixes to remove before counting.

        Returns:
            list[tuple[str, int]]: A list of (word, frequency) tuples.

        Side Effects:
            Updates self.results["top_popular_words"].
        """
        words = ut.convert_to_list(cleaned_text)
        if not words:
            self.results.update({"top_popular_words": []})
            return []

        if word_characters > 1:
            words = ut.filtered_words_by_char_num(" ".join(words), word_characters)

        if stopwords:
            words = ut.remove_stopwords(words, stopwords, prefixes)

        counter = collections.Counter(words)
        top_mode = counter.most_common(num_of_top_words)

        self.results.update({"top_popular_words": top_mode})
        return top_mode

    # Popular word
    def _popular_word(self, cleaned_text: str, word_characters: int, stopwords: list[str],
                      prefixes: list[str]) -> str | None:
        """
        Identify and store the single most frequent word in the cleaned text.

        Args:
            cleaned_text (str): The input text to analyze.
            word_characters (int): Minimum length of words to consider.
            stopwords (list[str]): Words to exclude.
            prefixes (list[str]): Prefixes to remove before counting.

        Returns:
            str | None: The most popular word, or None if the text has <= 1 word.

        Notes:
            - Logs a warning if word_characters <= 1.
            - Updates self.results["popular_word"].
        """

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
    def _words_count(self, cleaned_text: str) -> int:
        """
        Count and store the number of words in the cleaned text.

        Args:
            cleaned_text (str): The text after cleaning.

        Returns:
            int: Total number of words in the text.

        Side Effects:
            Updates self.results["words_count"].
        """
        if len(ut.convert_to_list(cleaned_text)) < 1:
            return 0
        counts = len(ut.convert_to_list(cleaned_text))
        self.results.update({"words_count": counts})
        return counts

    # extract Popular phases
    def _popular_phrases(self, cleaned_text: str, ngrams_size: int) -> None | str | list[tuple[str, int]]:
        """
        Extract and store the most frequent n-gram phrases from the text.

        Args:
            cleaned_text (str): The text after cleaning.
            ngrams_size (int): Size of n-grams (e.g., 2 for bigrams).

        Returns:
            list[tuple[str, int]] | None:
                List of (phrase, count) tuples, or None if not applicable.

        Notes:
            - Logs a warning if ngrams_size <= 1.
            - Updates self.results["popular_phrases"].
        """

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
    def _calculate_tfidf(self, documents: list[str], stopwords: list[str],
                         tfidf_ngram_range: tuple[int, int] | list[int]) -> list[tuple[str, float]]:
        """
        Compute and store the average TF-IDF scores for the given documents,
        safely handling empty documents or stopwords-only text.
        """
        logger.info("STOPWORDS count=%d sample=%r", len(stopwords), stopwords[:10])
        if isinstance(tfidf_ngram_range, list):
            tfidf_ngram_range = tuple(tfidf_ngram_range)

        # Filter out empty documents
        documents = [doc for doc in documents if doc.strip()]
        if not documents:
            logger.warning("TF-IDF skipped: all documents are empty after cleaning or stopwords removal.")
            self.results["tfidf_scores"] = []
            return []

        # If stopwords remove everything, set stop_words to None
        effective_stopwords = stopwords if any(doc not in stopwords for doc in documents) else None

        vectorizer = TfidfVectorizer(stop_words=effective_stopwords, ngram_range=tfidf_ngram_range)

        try:
            tfidf_matrix = vectorizer.fit_transform(documents)
        except ValueError as e:
            if "empty vocabulary" in str(e):
                logger.warning("TF-IDF skipped due to empty vocabulary.")
                self.results["tfidf_scores"] = []
                return []
            else:
                raise e

        feature_names = vectorizer.get_feature_names_out()
        tfidf_values = tfidf_matrix.toarray()
        avg_tfidf = np.mean(tfidf_values, axis=0)

        tfidf_scores = list(zip(feature_names, avg_tfidf))
        tfidf_scores.sort(key=lambda x: x[1], reverse=True)

        self.results["tfidf_scores"] = tfidf_scores
        return tfidf_scores

    # Text Categorization
    def _classify_text(self, cleaned_text: str, topics: dict[str, list[str]]) -> str:
        """
        Classify the text based on topic keyword occurrences.

        Counts how often each topic's words appear in the text and assigns
        the topic with the highest count as the best match.

        Args:
            cleaned_text (str): The cleaned text to classify.
            topics (dict[str, list[str]]): Mapping of topics to their keyword lists.

        Returns:
            str: The best-matching topic name, or "غير محدد" if no topic matches.

        Side Effects:
            Updates self.results["best_topic"].
        """
        counts = {topic: 0 for topic in topics}
        for topic, words in topics.items():
            counts[topic] = sum(cleaned_text.count(w) for w in words)

        best_topic = max(counts, key=counts.get)
        self.results["best_topic"] = best_topic
        return best_topic if counts[best_topic] > 0 else "غير محدد"

    # callable method
    def analyze(self, text: str, stopwords: list[str], prefixes: list[str],
                tfidf_ngram_range: tuple[int, int] | list[int], topics: dict[str, list[str]],
                file_number: int = 1, num_of_top_words: int = 2, word_characters: int = 1,
                support_statistics: bool = True, support_clean: bool = True,
                normalize_text: bool = False, rlen: bool = True, ngrams_size: int = 2) -> dict:
        """
        Perform a full linguistic and statistical analysis on the given text.

        This method cleans the text, computes lexical statistics, extracts popular
        words and phrases, calculates TF-IDF scores, and performs topic
        classification. It consolidates all intermediate results into a single
        dictionary.

        Args:
            text (str): Raw input text to analyze.
            stopwords (list[str]): List of stopwords to remove from the analysis.
            prefixes (list[str]): List of prefixes to strip before counting words.
            tfidf_ngram_range (tuple[int, int] | list[int]):
                Range of n-grams (e.g., (1, 2)) used in TF-IDF computation.
            topics (dict[str, list[str]]):
                Mapping of topic names to their associated keyword lists.
            file_number (int, optional): Identifier for the analyzed file. Defaults to 1.
            num_of_top_words (int, optional): Number of top frequent words to extract. Defaults to 2.
            word_characters (int, optional): Minimum character length for valid words. Defaults to 1.
            support_statistics (bool, optional): Whether to include statistical metrics in results. Defaults to True.
            support_clean (bool, optional): Whether to include cleaned text in results. Defaults to True.
            normalize_text (bool, optional): Whether to normalize characters (e.g., remove diacritics).
            Defaults to False.
            rlen (bool, optional): Whether to retain text length normalization. Defaults to True.
            ngrams_size (int, optional): Size of n-grams for phrase extraction. Defaults to 2.

        Returns:
            dict: A dictionary containing all computed analysis results, including:
                - "original_text" (str)
                - "cleaned_text" (str)
                - "words_count" (int)
                - "chars_count" (int)
                - "words_length_avg" (float)
                - "popular_word" (str)
                - "top_popular_words" (list[tuple[str, int]])
                - "popular_phrases" (list[tuple[str, int]])
                - "tfidf_scores" (list[tuple[str, float]])
                - "best_topic" (str)
                - "file_number" (int)
                - "support_statistics" (bool)
                - "support_clean" (bool)

        Notes:
            - Logs a warning if the text is empty after cleaning.
            - Internally calls helper methods for each metric (_chars_count, _popular_word, etc.).

        Side Effects:
            Updates self.results with all analysis outputs.
        """
        cleaned_text = ut.clean_text(text, normalize_text, rlen)
        logger.info("AFTER CLEANING: len=%d | preview=%r", len(cleaned_text), cleaned_text[:200])
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
        self._classify_text(cleaned_text, topics)

        english_text, arabic_text = ut.split_text_by_language(cleaned_text)
        logger.info("SPLIT LANGS: english_len=%d | arabic_len=%d", len(english_text), len(arabic_text))
        logger.info("SPLIT PREVIEWS: EN=%r AR=%r", english_text[:100], arabic_text[:100])
        documents = [t for t in [english_text, arabic_text] if t.strip()]
        logger.info("DOCUMENTS FOR TFIDF: count=%d, docs=%r", len(documents), [d[:100] for d in documents])
        self._calculate_tfidf(documents, stopwords, tfidf_ngram_range)

        return self.results

import json
import csv
import logging
import pandas as pd
from utils.logger import get_logger

logger = get_logger("export")


class Export:
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir

    def print_console(self, result):
        """
        Display text analysis results in the console in a structured format.

        This method prints the original text, the cleaned version (if available),
        and various linguistic and statistical metrics such as word count,
        character count, most frequent words/phrases, and TF-IDF scores.

        Args:
            result (dict): Dictionary containing the analysis results.
                Expected keys:
                    - "original_text" (str): The raw input text.
                    - "cleaned_text" (str, optional): The cleaned version of the text.
                    - "support_clean" (bool): Whether cleaning results are included.
                    - "support_statistics" (bool): Whether statistical data is included.
                    - "words_count" (int)
                    - "chars_count" (int)
                    - "popular_word" (str)
                    - "top_popular_words" (list[tuple[str, int]])
                    - "words_length_avg" (float)
                    - "popular_phrases" (list[tuple[str, int]])
                    - "tfidf_scores" (dict[str, float])

        Raises:
            KeyError: If any expected key is missing in the `result` dictionary.
            :param result:
        """
        print("\n----------------text before clean --------------------")
        print(result["original_text"])

        if result["support_clean"]:
            print("\n----------------text after clean --------------------")
            print(result["cleaned_text"])

        if result["support_statistics"]:
            print("\n----------------statistics --------------------")
            print("words count in text : ", result["words_count"])
            print("characters count in text : ", result["chars_count"])
            print("Popular word in text : ", result["popular_word"])
            print("Top Popular words in text : ", result["top_popular_words"])
            print("Words length average: ", result["words_length_avg"])
            print("Popular Phrases in text : ", result["popular_phrases"])
            print("TF-IDF scores in text : ", result["tfidf_scores"])

    def export_csv(self, result):
        """
        Export top popular words and phrases to a CSV file.

        This method writes the most frequent words and phrases (and their counts)
        to a CSV file in the output directory.
        Each row contains a popular word with its frequency and a corresponding
        phrase with its frequency.

        Args:
            result (dict): Dictionary containing the analysis results.
                Expected keys:
                    - "file_number" (int): Index of the analyzed file.
                    - "top_popular_words" (list[tuple[str, int]])
                    - "popular_phrases" (list[tuple[str, int]])

        File Output:
            {output_dir}/file-{file_number}_top_popular_words.csv

        Logs:
            - Success message when export is successful.
            - Error message on failure.

        Raises:
            Exception: Logs the exception if file writing fails.
        """
        try:
            with open(f'{self.output_dir}/file-{result["file_number"]}top_popular_words.csv', 'w', encoding="utf-8",
                      newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Popular Words", "Count", "Popular Phrases", "Count"])

                words = result["top_popular_words"]
                phrases = result["popular_phrases"]
                max_len = max(len(words), len(phrases))

                for i in range(max_len):
                    word, word_count = words[i] if i < len(words) else ("", "")
                    phrase, phrase_count = phrases[i] if i < len(phrases) else ("", "")
                    writer.writerow([word, word_count, phrase, phrase_count])

            logging.info(f"CSV file saved successfully: outputs/file-{result["file_number"]}"
                         f"top_popular_words_and_phrases.csv")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")

    def export_excel(self, result):
        """
        Export top popular words and phrases to an Excel (.xlsx) file.

        This method creates a tabular Excel file containing the most frequent words
        and phrases extracted from the analyzed text.

        Args:
            result (dict): Dictionary containing the analysis results.
                Expected keys:
                    - "file_number" (int): Index of the analyzed file.
                    - "top_popular_words" (list[tuple[str, int]])
                    - "popular_phrases" (list[tuple[str, int]])

        File Output:
            {output_dir}/file-{file_number}_top_popular_words_and_phrases.xlsx

        Logs:
            - Error message if the export fails.

        Raises:
            Exception: Logs the exception on write failure.
        """
        words = result["top_popular_words"]
        phrases = result["popular_phrases"]
        max_len = max(len(words), len(phrases))
        data = []

        try:
            for i in range(max_len):
                word, word_count = words[i] if i < len(words) else ("", "")
                phrase, phrase_count = phrases[i] if i < len(phrases) else ("", "")
                data.append([word, word_count, phrase, phrase_count])

            df = pd.DataFrame(data, columns=["Popular Words", "word_count", "Popular phrases", "phrase_count"])
            df.to_excel(f"{self.output_dir}/file-{result['file_number']}_top_popular_words_and_phrases.xlsx",
                        index=False)
        except Exception as e:
            logging.error(f"Failed to save file: {e}")

    def export_json(self, result):
        """
        Export full text analysis results to a JSON file.

        This method serializes and saves the entire `result` dictionary containing
        text analysis data to a formatted JSON file.

        Args:
            result (dict): Dictionary containing the full analysis results.
                Must include at least:
                    - "file_number" (int): Index of the analyzed file.

        File Output:
            {output_dir}/file-{file_number}_analyzer_outputs.json

        Logs:
            - Success message on successful save.
            - Error message on failure.

        Raises:
            Exception: Logs the exception if JSON writing fails.
        """
        try:
            with (open(f'{self.output_dir}/file-{result["file_number"]}_analyzer_outputs.json', 'w', encoding="utf-8")
                  as json_file):
                json.dump(result, json_file, ensure_ascii=False, indent=4)
            logging.info(f"JSON file saved successfully: outputs/file-{result["file_number"]}_analyzer_outputs.json")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")

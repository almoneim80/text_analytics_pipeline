import json
import csv
import logging
import pandas as pd

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


class Export():
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir

    def print_console(self, result):
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
        try:
            with (open(f'{self.output_dir}/file-{result["file_number"]}_analyzer_outputs.json', 'w', encoding="utf-8")
                  as json_file):
                json.dump(result,  json_file, ensure_ascii=False, indent=4)
            logging.info(f"JSON file saved successfully: outputs/file-{result["file_number"]}_analyzer_outputs.json")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
        



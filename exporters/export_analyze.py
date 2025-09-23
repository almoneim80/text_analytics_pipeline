import json
import csv
import logging

# logging config
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("outputs/app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

class Export():
    def __init__(self):
        pass

    @staticmethod
    def print_console(text, cleaned_text, results, support_clean, support_statistics):
        print("\n----------------text before clean --------------------")
        print(text)
        
        if support_clean:
            print("\n----------------text after clean --------------------")
            print(cleaned_text)

        if support_statistics:
            print("\n----------------statistics --------------------")
            print("words count in text : ", results["words_count"])
            print("characters count in text : ", results["chars_count"])
            print("Popular word in text : ", results["popular_word"])
            print("Top Popular words in text : ", results["top_popular_words"])
            print("Words length average: ", results["words_length_avg"])

    @staticmethod
    def export_csv(results, file_number):
        try:
            with open(f'outputs/file-{file_number}top_popular_words.csv', 'w', encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Top Popular Words"])
                for word  in results["top_popular_words"]:
                    writer.writerow([word])
            logging.info(f"CSV file saved successfully: outputs/file-{file_number}top_popular_words.csv")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
            

    @staticmethod
    def export_json(results, file_number):
        try:
            with open(f'outputs/file-{file_number}_analyzer_outputs.json', 'w', encoding="utf-8") as json_file:
                json.dump(results,  json_file, ensure_ascii=False, indent=4)
            logging.info(f"JSON file saved successfully: outputs/file-{file_number}_analyzer_outputs.json")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
        



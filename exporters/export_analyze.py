import json
import csv
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

class Export():
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir

    def print_console(self, result):
        print("\n----------------text before clean --------------------")
        print(result["orginal_text"])
        
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

    def export_csv(self, result):
        try:
            with open(f'{self.output_dir}/file-{result["file_number"]}top_popular_words.csv', 'w', encoding="utf-8", newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Top Popular Words"])
                for word  in result["top_popular_words"]:
                    writer.writerow([word])
            logging.info(f"CSV file saved successfully: outputs/file-{result["file_number"]}top_popular_words.csv")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
            

    def export_json(self, result):
        try:
            with open(f'{self.output_dir}/file-{result["file_number"]}_analyzer_outputs.json', 'w', encoding="utf-8") as json_file:
                json.dump(result,  json_file, ensure_ascii=False, indent=4)
            logging.info(f"JSON file saved successfully: outputs/file-{result["file_number"]}_analyzer_outputs.json")
        except Exception as e:
            logging.error(f"Failed to save file: {e}")
        



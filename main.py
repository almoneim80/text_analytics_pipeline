import analyzer.text_analyzer as ta
import pathlib
import logging
import json
import exporters.export_analyze as exa

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

# config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# read file
ext = config["supported_files"]

# read files from user
def cli():
    paths = []
    while True:
        inp = input("Please, input file path (or 'C' to finish): ")
        if inp.lower() == 'c':
            break
        paths.append(inp)
    return paths

# read all files contents
def read_files(file_paths):
    texts = []
    for file in file_paths:
        path = pathlib.Path(file)

        if not path.exists() or path.is_dir() or path.suffix not in ext:
            logging.warning(f"Skipping invalid path: {file}")
            continue
        
        for encoding in config["supported_encoding"]:
            try:
                with open(file, 'r', encoding=encoding) as f:
                    text = f.read()
                    texts.append(text)
                    logging.info(f"Read {file} with {encoding}")
                    break
            except UnicodeDecodeError:
                continue
        else:
            logging.error(f"Could not read {file} with UTF-8 or UTF-16")
            
    return texts

# do analyze
def analyze_files(
        texts, analyzer, exporter, num_of_top_words,
        word_characters, support_statistics, support_clean, export_json, export_csv, export_console):
    for i, text in enumerate(texts):
        if not text.strip():
            logging.warning(f"File {i} is empty")
            continue
        result = analyzer.analyze(
            text=text, file_number=i+1,
            num_of_top_words=num_of_top_words,
            word_characters=word_characters,
            support_statistics=support_statistics,
            support_clean=support_clean)
        
        if export_console:
            exporter.print_console(result)
        if export_csv:
            exporter.export_csv(result)
        if export_json:
            exporter.export_json(result)

# run
paths = cli()
if len(paths) == 0:
    logging.error("No files provided for analysis")
    exit()

texts = read_files(paths)
exporter = exa.Export(output_dir=config["output_folder"])
analyzer = ta.TextAnalyzer()
analyze_files(
    texts,
    analyzer,
    exporter,
    num_of_top_words=config["num_of_top_words"],
    word_characters=config["word_characters"],
    support_statistics=config["support_statistics"],
    support_clean=config["support_clean"],
    export_json=config["export_json"],
    export_csv=config["export_csv"],
    export_console=config["export_console"]
    )


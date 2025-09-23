import analyzer.text_analyzer as ta
import pathlib
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

# read file
ext = ['.txt']

def read_files(file_paths):
    data = []
    for file in file_paths:
        path = pathlib.Path(file)

        if not path.exists() or path.is_dir() or path.suffix not in ext:
            logging.warning(f"Skipping invalid path: {file}")
            continue
        
        for encoding in ["utf-8", "utf-16"]:
            try:
                with open(file, 'r', encoding=encoding) as f:
                    text = f.read()
                    data.append(text)
                    logging.info(f"Read {file} with {encoding}")
                    break
            except UnicodeDecodeError:
                continue
        else:
            logging.error(f"Could not read {file} with UTF-8 or UTF-16")
            
    return data


logging.info(f"Please input all files you want to analyse (extensions allowed: {ext})")
logging.info("If done, enter (C) character")


paths = []
inp = ''
for i in range(10):
    inp = input("Please, input file path: ")
    if inp.lower() == 'c':
        break
    else:
        if pathlib.Path(inp).is_dir():
            logging.error(f"path {inp} is not valid")
        elif pathlib.Path(inp).suffix not in ext:
            logging.warning(f"file {inp} extension is not valid")
        else:
            paths.append(inp)

if len(paths) == 0:
    logging.error("No files provided for analysis")
else:
    text = read_files(paths)
    analyzer = ta.TextAnalyzer()
    for i, t in enumerate(text):
        if t == "":
            logging.warning(f"file  {i} is null")
            continue
        analyzer.analyze(text=t, file_number=i, num_of_top_words=8, word_characters=5, support_statistics=True, support_clean=True)

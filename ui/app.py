import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sidebar import load_config, sidebar_ui
from result_viewer import display_result
import analyzer.text_analyzer as ta
import exporters.export_analyze as exa
from file_uploader import upload_files
from utils.logger import get_logger
logger = get_logger("app")

# Page setup
st.set_page_config(page_title="🧠 Text Analyzer", layout="wide")
st.title("🧠 Text Analyzer - Arabic")

# load settings and side interface
config = load_config()
settings = sidebar_ui(config)

# Upload files
texts, uploaded_files = upload_files(config.get("supported_files", ["txt"]))
logger.info(f"Result of calling upload_files method from upload_files class: texts={texts} | len={len(texts)} | uploaded_files={uploaded_files[:200]!r}")

# Start analysis
if st.button("Start Analysis"):
    analyzer = ta.TextAnalyzer()
    exporter = exa.Export(output_dir=config["output_folder"])

    for i, text in enumerate(texts):
        result = analyzer.analyze(
            text=text,
            file_number=i + 1,
            num_of_top_words=settings["num_of_top_words"],
            word_characters=settings["word_characters"],
            support_statistics=settings["support_statistics"],
            support_clean=settings["support_clean"],
            normalize_text=settings["normalize_text"],
            rlen=settings["remove_links_emojis_numbers"],
            stopwords=settings["stopwords"],
            prefixes=settings["prefixes"],
            ngrams_size=settings["ngrams_size"],
            tfidf_ngram_range=settings["tfidf_ngram_range"],
            topics=settings["topics"]
        )

        # Display results
        display_result(
            result,
            settings["support_clean"],
            settings["support_statistics"],
            settings["ENABLE_TFIDF"]
        )

        # Export
        if settings["export_json"]:
            exporter.export_json(result)
        if settings["export_csv"]:
            exporter.export_csv(result)
        if settings["export_excel"]:
            exporter.export_excel(result)
        if settings["export_console"]:
            print(result)

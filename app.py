import streamlit as st
from ui.sidebar import load_config, sidebar_ui
from ui.result_viewer import display_result
import analyzer.text_analyzer as ta
import exporters.export_analyze as exa
from ui.file_uploader import upload_files

# Page setup
st.set_page_config(page_title="🧠 Text Analyzer", layout="wide")
st.title("🧠 Text Analyzer - Arabic")

# load settings and side interface
config = load_config()
settings = sidebar_ui(config)

# Upload files
texts, uploaded_files = upload_files(config.get("supported_files", ["txt"]))

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

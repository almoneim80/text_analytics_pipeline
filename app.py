import streamlit as st
import analyzer.text_analyzer as ta
import exporters.export_analyze as exa
import json

# Load config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

st.title("🧠 Text Analyzer")

# Upload files
uploaded_files = st.file_uploader(
    "Upload one or more text files",
    type=config.get("supported_files", ["txt"]),
    accept_multiple_files=True
)

analyze_all = st.checkbox("Analyze all files together", value=config.get("analyze_all_together", False))

if uploaded_files:
    texts = [f.read().decode("utf-8", errors="ignore") for f in uploaded_files]
    st.success(f"{len(uploaded_files)} file(s) loaded successfully!")

    if st.button("Start Analysis"):
        analyzer = ta.TextAnalyzer()
        exporter = exa.Export(output_dir=config["output_folder"])

        if analyze_all:
            # Combine all texts
            combined_text = " ".join(texts)
            result = analyzer.analyze(
                text=combined_text,
                file_number=0,
                num_of_top_words=config["num_of_top_words"],
                word_characters=config["word_characters"],
                support_statistics=config["support_statistics"],
                support_clean=config["support_clean"],
                normalize_text=config["normalize_text"],
                rlen=config["remove_links_emojis_numbers"],
                stopwords=config["stopwords"],
                prefixes=config["prefixes"],
                ngrams_size=config["ngrams_size"],
                tfidf_ngram_range=tuple(config["tfidf_ngram_range"])
            )
            st.subheader("Analysis Result")
            st.json(result)

            # Export
            if config.get("export_json", False):
                exporter.export_json(result)
            if config.get("export_csv", False):
                exporter.export_csv(result)
            if config.get("export_excel", False):
                exporter.export_excel(result)

        else:
            for i, text in enumerate(texts):
                result = analyzer.analyze(
                    text=text,
                    file_number=i + 1,
                    num_of_top_words=config["num_of_top_words"],
                    word_characters=config["word_characters"],
                    support_statistics=config["support_statistics"],
                    support_clean=config["support_clean"],
                    normalize_text=config["normalize_text"],
                    rlen=config["remove_links_emojis_numbers"],
                    stopwords=config["stopwords"],
                    prefixes=config["prefixes"],
                    ngrams_size=config["ngrams_size"],
                    tfidf_ngram_range=tuple(config["tfidf_ngram_range"])
                )
                st.subheader(f"Analysis Result for File {i+1}")
                st.json(result)

                # Export
                if config.get("export_json", False):
                    exporter.export_json(result)
                if config.get("export_csv", False):
                    exporter.export_csv(result)
                if config.get("export_excel", False):
                    exporter.export_excel(result)

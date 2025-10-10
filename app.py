import streamlit as st
import analyzer.text_analyzer as ta
import exporters.export_analyze as exa
import json
import pandas as pd

# Load config
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

st.set_page_config(page_title="🧠 Text Analyzer", layout="wide")
st.title("🧠 Text Analyzer")

# Upload files
uploaded_files = st.file_uploader(
    "Upload one or more text files",
    type=config.get("supported_files", ["txt"]),
    accept_multiple_files=True
)

analyze_all = st.checkbox(
    "Analyze all files together", value=config.get("analyze_all_together", False)
)


def display_result(result):
    with st.expander(f"📂 Analysis Result for File #{result['file_number']}"):
        # Tabs for sections
        tabs = st.tabs(["📄 Original Text", "🧹 Cleaned Text" if result["support_clean"] else "", "📊 Statistics", "🔑 TF-IDF"])

        # Original Text
        with tabs[0]:
            st.write(result["original_text"])

        # Cleaned Text
        if result["support_clean"]:
            with tabs[1]:
                st.write(result["cleaned_text"])

        # Statistics
        with tabs[2]:
            if result["support_statistics"]:
                stats_col1, stats_col2 = st.columns(2)
                with stats_col1:
                    st.metric("Words Count", result["words_count"])
                    st.metric("Characters Count", result["chars_count"])
                    st.metric("Average Word Length", round(result["words_length_avg"], 2))
                    st.metric("Most Popular Word", result["popular_word"])
                    st.metric("Text Topic", result["best_topic"])
                with stats_col2:
                    st.markdown("**Top Popular Words**")
                    if result["top_popular_words"]:
                        df_words = pd.DataFrame(result["top_popular_words"], columns=["Word", "Count"])
                        st.dataframe(df_words, use_container_width=True)
                    else:
                        st.write("No data")

                    st.markdown("**Popular Phrases**")
                    if result["popular_phrases"]:
                        df_phrases = pd.DataFrame(result["popular_phrases"], columns=["Phrase", "Count"])
                        st.dataframe(df_phrases, use_container_width=True)
                    else:
                        st.write("No data")

        # TF-IDF
        with tabs[3]:
            if config.get("ENABLE_TFIDF", True):
                if result["tfidf_scores"]:
                    df_tfidf = pd.DataFrame(result["tfidf_scores"], columns=["Term", "Score"])
                    st.dataframe(df_tfidf.sort_values(by="Score", ascending=False), use_container_width=True)
                else:
                    st.write("No TF-IDF data")


if uploaded_files:
    texts = [f.read().decode("utf-8", errors="ignore") for f in uploaded_files]
    st.success(f"{len(uploaded_files)} file(s) loaded successfully!")

    if st.button("Start Analysis"):
        analyzer = ta.TextAnalyzer()
        exporter = exa.Export(output_dir=config["output_folder"])

        if analyze_all:
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
                tfidf_ngram_range=tuple(config["tfidf_ngram_range"]),
                topics=config["topics"]
            )
            display_result(result)

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
                    tfidf_ngram_range=tuple(config["tfidf_ngram_range"]),
                    topics=config["topics"]
                )
                display_result(result)

                # Export
                if config.get("export_json", False):
                    exporter.export_json(result)
                if config.get("export_csv", False):
                    exporter.export_csv(result)
                if config.get("export_excel", False):
                    exporter.export_excel(result)

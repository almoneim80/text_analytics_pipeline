import streamlit as st
import json
import os


def load_config():
    """
    Loads and returns the application configuration from a JSON file.

    The configuration file is expected to be named "config.json" and located
    at the root directory of the project (one level above this script's directory).

    The function reads the JSON file with UTF-8 encoding and returns its contents
    as a Python dictionary.

    Returns:
        dict: A dictionary containing configuration key-value pairs.

    Raises:
        FileNotFoundError: If the "config.json" file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.

    Example:
        >>> config = load_config()
        >>> print(config["database"]["host"])
        "localhost"
    """
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def sidebar_ui(config):
    """
    Builds and renders the Streamlit sidebar UI for configuring text analysis settings.

    This function provides a fully interactive sidebar with multiple sections:
    1. Analyzer Settings: Toggle options for cleaning, statistics, normalization,
       TF-IDF, n-grams size, console export, and other analysis preferences.
    2. Numeric Inputs: Controls for top words count and minimum word length.
    3. TF-IDF Settings: N-gram range slider for TF-IDF computation.
    4. Export Options: Toggle export formats (JSON, CSV, Excel).
    5. Stopwords & Prefixes: Text areas for custom stopwords and prefixes.
    6. Topics Editor: Multi-select and editable keyword lists for each topic.

    Args:
        config (dict): A dictionary containing default configuration values for the sidebar.
                       Example keys include:
                       - "analyze_all_together"
                       - "support_clean"
                       - "support_statistics"
                       - "normalize_text"
                       - "remove_links_emojis_numbers"
                       - "ENABLE_TFIDF"
                       - "num_of_top_words"
                       - "word_characters"
                       - "tfidf_ngram_range"
                       - "export_json"
                       - "export_csv"
                       - "export_excel"
                       - "stopwords"
                       - "prefixes"
                       - "topics"
                       - "ngrams_size"
                       - "export_console"

    Returns:
        dict: A dictionary containing all current user-selected sidebar settings. Keys include:
              "analyze_all", "support_clean", "support_statistics", "normalize_text",
              "remove_links_emojis_numbers", "ENABLE_TFIDF", "num_of_top_words",
              "word_characters", "tfidf_ngram_range", "export_json", "export_csv",
              "export_excel", "stopwords", "prefixes", "topics", "ngrams_size", "export_console".

    Example:
        >>> config = load_config()
        >>> settings = sidebar_ui(config)
        >>> if settings["support_clean"]:
        >>>     cleaned_text = clean_text(original_text)
    """
    st.sidebar.header("⚙️ Analyzer Settings")

    # Boolean options
    analyze_all = st.sidebar.checkbox("Analyze all files together", value=config.get("analyze_all_together", False))
    support_clean = st.sidebar.checkbox("Enable Cleaning", value=config.get("support_clean", True))
    support_statistics = st.sidebar.checkbox("Enable Statistics", value=config.get("support_statistics", True))
    normalize_text = st.sidebar.checkbox("Normalize Text", value=config.get("normalize_text", True))
    remove_links_emojis_numbers = st.sidebar.checkbox("Remove Links/Emojis/Numbers",
                                                      value=config.get("remove_links_emojis_numbers", True))
    ENABLE_TFIDF = st.sidebar.checkbox("Enable TF-IDF", value=config.get("ENABLE_TFIDF", True))
    ngrams_size = st.sidebar.number_input("N-Grams Size", min_value=1, value=config.get("ngrams_size", 2))
    export_console = st.sidebar.checkbox("Export Console", value=config.get("export_console", True))

    # Numeric inputs
    num_of_top_words = st.sidebar.number_input("Number of Top Words", min_value=1,
                                               value=config.get("num_of_top_words", 10))
    word_characters = st.sidebar.number_input("Minimum Word Length", min_value=1,
                                              value=config.get("word_characters", 2))

    # TF-IDF ngram range
    tfidf_ngram_range = st.sidebar.slider(
        "TF-IDF Ngram Range (min, max)",
        min_value=1, max_value=5,
        value=(config.get("tfidf_ngram_range", [1, 2])[0], config.get("tfidf_ngram_range", [1, 2])[1])
    )

    # Export options
    st.sidebar.header("📤 Export Options")
    export_json = st.sidebar.checkbox("Export JSON", value=config.get("export_json", True))
    export_csv = st.sidebar.checkbox("Export CSV", value=config.get("export_csv", True))
    export_excel = st.sidebar.checkbox("Export Excel", value=config.get("export_excel", True))

    # Stopwords & Prefixes
    st.sidebar.header("📌 Stopwords & Prefixes")
    stopwords = st.sidebar.text_area("Stopwords (comma separated)", value=",".join(config.get("stopwords", []))).split(
        ",")
    prefixes = st.sidebar.text_area("Prefixes (comma separated)", value=",".join(config.get("prefixes", []))).split(",")

    # Topics Editor
    st.sidebar.header("🏷 Topics Editor")
    topics = config.get("topics", {})
    selected_topics = st.sidebar.multiselect("Select Topics", options=list(topics.keys()), default=list(topics.keys()))

    topics_edited = {}
    for t in selected_topics:
        keywords_text = st.sidebar.text_area(f"{t}", value=",".join(topics.get(t, [])), height=100)
        keywords_list = [k.strip() for k in keywords_text.split(",") if k.strip()]
        topics_edited[t] = keywords_list

    return {
        "analyze_all": analyze_all,
        "support_clean": support_clean,
        "support_statistics": support_statistics,
        "normalize_text": normalize_text,
        "remove_links_emojis_numbers": remove_links_emojis_numbers,
        "ENABLE_TFIDF": ENABLE_TFIDF,
        "num_of_top_words": num_of_top_words,
        "word_characters": word_characters,
        "tfidf_ngram_range": tfidf_ngram_range,
        "export_json": export_json,
        "export_csv": export_csv,
        "export_excel": export_excel,
        "stopwords": stopwords,
        "prefixes": prefixes,
        "topics": topics_edited,
        "ngrams_size": ngrams_size,
        "export_console": export_console,
    }

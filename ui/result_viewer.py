import streamlit as st
import pandas as pd


def display_result(result, support_clean=True, support_statistics=True, ENABLE_TFIDF=True):
    """
    Displays a comprehensive analysis of a text file in a Streamlit interface.

    This function uses Streamlit components to present:
    1. The original text.
    2. The cleaned/processed text (optional).
    3. Text statistics such as word count, character count, average word length,
       most popular words, and detected topic (optional).
    4. TF-IDF scores for terms in the text (optional).

    The output is organized in an expandable section with tabs for each type of information.

    Args:
        result (dict): A dictionary containing the analysis results with keys such as:
            - "file_number" (int): The identifier of the file.
            - "original_text" (str): Raw text content.
            - "cleaned_text" (str): Preprocessed/cleaned text.
            - "words_count" (int): Number of words.
            - "chars_count" (int): Number of characters.
            - "words_length_avg" (float): Average word length.
            - "popular_word" (str): Most frequent word.
            - "best_topic" (str): Best predicted topic.
            - "top_popular_words" (list of tuples, optional): Top frequent words and counts.
            - "popular_phrases" (list of tuples, optional): Top frequent phrases and counts.
            - "tfidf_scores" (list of tuples, optional): Term TF-IDF scores.
        support_clean (bool, optional): If True, display the cleaned text tab. Default is True.
        support_statistics (bool, optional): If True, display the statistics tab. Default is True.
        ENABLE_TFIDF (bool, optional): If True, display the TF-IDF tab. Default is True.

    Returns:
        None: This function only renders Streamlit UI elements and does not return a value.

    Example:
        >>> result = analyze_text(file_path="example.txt")
        >>> display_result(result)
    """
    with st.expander(f"📂 Analysis Result for File #{result['file_number']}"):
        tabs = st.tabs(["📄 Original Text", "🧹 Cleaned Text", "📊 Statistics", "🔑 TF-IDF"])

        # Original Text
        with tabs[0]:
            st.write(result["original_text"])

        # Cleaned Text
        if support_clean:
            with tabs[1]:
                st.write(result["cleaned_text"])

        # Statistics
        if support_statistics:
            with tabs[2]:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Words Count", result["words_count"])
                    st.metric("Characters Count", result["chars_count"])
                    st.metric("Average Word Length", round(result["words_length_avg"], 2))
                    st.metric("Most Popular Word", result["popular_word"])
                    st.metric("Text Topic", result["best_topic"])
                with col2:
                    if result.get("top_popular_words"):
                        st.dataframe(pd.DataFrame(result["top_popular_words"], columns=["Word", "Count"]))
                    if result.get("popular_phrases"):
                        st.dataframe(pd.DataFrame(result["popular_phrases"], columns=["Phrase", "Count"]))

        # TF-IDF
        if ENABLE_TFIDF:
            with tabs[3]:
                if result.get("tfidf_scores"):
                    df_tfidf = pd.DataFrame(result["tfidf_scores"], columns=["Term", "Score"])
                    st.dataframe(df_tfidf.sort_values(by="Score", ascending=False))

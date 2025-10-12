import streamlit as st
import pandas as pd

def display_result(result, support_clean=True, support_statistics=True, ENABLE_TFIDF=True):
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

import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="QA",
    layout="wide"
)

st.title("RAG System")

tab1, tab2 = st.tabs(["Question Answering", "Analytics"])
with tab1:

    st.header("Ask Questions")

    question = st.text_input(
        "Enter your question"
    )

    if st.button("Ask"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:

            with st.spinner("Generating answer..."):

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question
                    }
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("Answer Generated")

                    st.subheader("Answer")

                    st.write(result["answer"])

                    st.subheader("Source Pages")

                    st.write(result["sources"])

                    st.metric(
                        "Latency",
                        f'{result["latency_ms"]:.2f} ms'
                    )

                else:

                    st.error(
                        response.json()["detail"]
                    )

with tab2:

    st.header("Analytics")

    if st.button("Load Analytics"):

        response = requests.get(
            f"{API_URL}/analytics"
        )

        if response.status_code == 200:

            data = response.json()

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Queries",
                data["total_queries"]
            )

            col2.metric(
                "Average Latency",
                f'{data["average_latency_ms"]:.2f} ms'
            )

            col3.metric(
                "Failed Queries",
                data["failed_queries"]
            )

            st.subheader("Top Questions")

            df = pd.DataFrame(
                data["top_questions"]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.error("Unable to fetch analytics.")


import streamlit as st
import requests

st.set_page_config(
    page_title="ReviewSense | Sentiment Analysis",
    page_icon="🎬",
    layout="centered"
)
API_URL = "http://127.0.0.1:8000/predict"


st.title("🎬 ReviewSense")                             #style the page
st.subheader("Understand the sentiment behind movie reviews")

st.write(
    "Enter a movie review below and let our AI model "
    "analyse whether it expresses positive or negative sentiment."
)

st.divider()


review = st.text_area(             #review input
    "Enter your movie review",
    placeholder="e.g. This movie was absolutely amazing...",
    height=180,
    max_chars=10000
)

#prediction
if st.button("Analyse Review", type="primary", use_container_width=True):

    if not review.strip():
        st.warning("Please enter a movie review first.")

    else:
        try:
            with st.spinner("Analysing your review..."):

                response = requests.post(
                    API_URL,
                    json={"review": review},
                    timeout=30
                )

            if response.status_code == 200:

                result = response.json()

                sentiment = result["sentiment"]
                probabilities = result["probabilities"]

                st.divider()
                st.subheader("Analysis Results")

                #Display predicted sentiment
                if sentiment == "positive":
                    st.success("😊 Positive Sentiment")
                else:
                    st.error("😞 Negative Sentiment")

                #display probabilities
                st.write("### Sentiment Scores")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Positive",
                        f"{probabilities['positive'] * 100:.2f}%"
                    )

                with col2:
                    st.metric(
                        "Negative",
                        f"{probabilities['negative'] * 100:.2f}%"
                    )

                #visualizing scores
                st.write("**Positive score**")
                st.progress(probabilities["positive"])

                st.write("**Negative score**")
                st.progress(probabilities["negative"])

            elif response.status_code == 422:
                error = response.json()
                st.warning(error["detail"][0]["msg"])

            else:
                st.error(
                    f"API returned an error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the ReviewSense API. "
                "Please make sure the backend is running."
            )

        except requests.exceptions.Timeout:
            st.error("The request timed out. Please try again.")

        except requests.exceptions.RequestException as error:
            st.error(f"An unexpected request error occurred: {error}")


#footer
st.divider()
st.caption(
    "ReviewSense | Machine Learning Sentiment Analysis "
    "| Powered by TF-IDF and Logistic Regression"
)

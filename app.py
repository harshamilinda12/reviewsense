
import requests
import streamlit as st

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ReviewSense | Movie Sentiment Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = "http://127.0.0.1:8000/predict"
MAX_HISTORY = 10
CLOSE_CALL_THRESHOLD = 0.65

EXAMPLE_REVIEWS = {
    "positive": (
        "An amazing movie with brilliant performances, beautiful "
        "cinematography, and an unforgettable story."
    ),
    "negative": (
        "The movie was incredibly boring. The acting was terrible, "
        "and the storyline made no sense."
    ),
    "mixed": (
        "The acting was excellent and the visuals were beautiful, "
        "but the story was predictable and the ending was disappointing."
    ),
}


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "review_input" not in st.session_state:
    st.session_state.review_input = ""

if "latest_prediction" not in st.session_state:
    st.session_state.latest_prediction = None

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def load_example(kind):
    st.session_state.review_input = EXAMPLE_REVIEWS[kind]
    st.session_state.latest_prediction = None


def clear_review():
    st.session_state.review_input = ""
    st.session_state.latest_prediction = None


def reset_prediction():
    st.session_state.latest_prediction = None


def clear_history():
    st.session_state.prediction_history = []


def is_close_call(probabilities):
    return (
        max(float(score) for score in probabilities.values())
        < CLOSE_CALL_THRESHOLD
    )


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
<style>
    .stApp {
        background: #0b1020;
        color: #e8edf7;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .eyebrow, .section-label {
        color: #a78bfa;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .hero-title {
        font-size: clamp(2.5rem, 6vw, 4rem);
        font-weight: 800;
        letter-spacing: -2px;
        line-height: 1.2;
        margin: 0.6rem 0;
    }

    .hero-title span {
        color: #a78bfa;
    }

    .hero-description {
        color: #a2acc0;
        font-size: 1.05rem;
        max-width: 650px;
        line-height: 1.7;
        margin-bottom: 2rem;
    }

    .info-card, .score-card {
        background: #151d30;
        border: 1px solid #29344d;
        border-radius: 16px;
        padding: 24px;
    }

    .info-card {
        margin-top: 27px;
    }

    .info-card h3 {
        margin-top: 0;
        font-size: 1.2rem;
    }

    .info-card p, .step-description {
        color: #a2acc0;
        line-height: 1.6;
    }

    .info-card p {
        font-size: 0.94rem;
    }

    .pipeline-step {
        padding: 14px 0;
        border-bottom: 1px solid #29344d;
        font-size: 0.9rem;
    }

    .pipeline-step:last-child {
        border-bottom: none;
    }

    .step-description {
        font-size: 0.82rem;
        margin: 5px 0 0 27px;
    }

    .stTextArea textarea {
        background: #151d30 !important;
        border: 1px solid #35415b !important;
        border-radius: 12px !important;
        color: #f1f5ff !important;
        font-size: 1rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #a78bfa !important;
    }

    div.stButton > button[kind="primary"] {
        background: #7c3aed;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        min-height: 48px;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #6d28d9;
        color: white;
    }

    .result-banner {
        border-radius: 15px;
        padding: 24px;
        margin: 15px 0 20px;
    }

    .result-banner.positive {
        background: #12342d;
        border: 1px solid #28765c;
    }

    .result-banner.negative {
        background: #382026;
        border: 1px solid #834450;
    }

    .result-title {
        font-size: 1.7rem;
        font-weight: 750;
        margin: 8px 0;
    }

    .result-subtitle {
        color: #c5cbd8;
        font-size: 0.9rem;
    }

    .score-card {
        margin-bottom: 15px;
        padding: 20px;
    }

    .score-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-bottom: 14px;
    }

    .score-value {
        font-size: 1.3rem;
        font-weight: 700;
    }

    .score-track {
        height: 9px;
        border-radius: 10px;
        background: #30394d;
        overflow: hidden;
    }

    .score-fill {
        height: 100%;
        border-radius: 10px;
    }

    .score-fill.positive {
        background: #34d399;
    }

    .score-fill.negative {
        background: #fb7185;
    }

    .footer-note {
        color: #7d899d;
        text-align: center;
        font-size: 0.8rem;
        padding-top: 25px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
<div class="eyebrow">Movie Review Intelligence</div>
<div class="hero-title">🎬 Review<span>Sense</span></div>
<div class="hero-description">
    Discover the sentiment behind movie reviews. Our machine learning model
    analyses review text to identify positive and negative opinions.
</div>
""",
    unsafe_allow_html=True,
)

st.divider()


# --------------------------------------------------
# Review input
# --------------------------------------------------

left_col, right_col = st.columns([1.7, 1], gap="large")

with left_col:

    st.markdown(
        '<div class="section-label">ANALYZE A REVIEW</div>',
        unsafe_allow_html=True,
    )

    st.subheader("What's your take on the movie?")
    st.caption("Try an example review")

    example_cols = st.columns(3)

    for column, kind in zip(
        example_cols, ("positive", "negative", "mixed")
    ):
        with column:
            st.button(
                kind.title(),
                on_click=load_example,
                args=(kind,),
                use_container_width=True,
            )

    review = st.text_area(
        "Your movie review",
        placeholder="Enter a movie review here...",
        height=210,
        max_chars=10000,
        key="review_input",
        on_change=reset_prediction,
    )

    st.caption(
        "For best results, enter an English-language movie review."
    )

    analyse_col, clear_col = st.columns([3, 1])

    with analyse_col:
        analyse_button = st.button(
            "Analyse Sentiment",
            type="primary",
            use_container_width=True,
        )

    with clear_col:
        st.button(
            "Clear",
            on_click=clear_review,
            use_container_width=True,
        )


# --------------------------------------------------
# How ReviewSense Works
# --------------------------------------------------

with right_col:

    st.markdown(
        """
<div class="info-card">
    <h3>How ReviewSense Works</h3>
    <p>From a movie review to a sentiment prediction in four steps.</p>
    <div class="pipeline-step">
        📝 <strong>Write a review</strong>
    </div>
    <div class="pipeline-step">
        🔤 <strong>Convert text into features</strong>
        <div class="step-description">TF-IDF processes the review text.</div>
    </div>
    <div class="pipeline-step">
        🧠 <strong>Predict sentiment</strong>
        <div class="step-description">Logistic Regression analyses the features.</div>
    </div>
    <div class="pipeline-step">
        📊 <strong>View your results</strong>
        <div class="step-description">See the prediction and probability scores.</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# FastAPI prediction request
# --------------------------------------------------

if analyse_button:

    st.session_state.latest_prediction = None

    if not review.strip():
        st.warning("Please enter a movie review first.")

    else:
        try:
            with st.spinner("Analysing your review..."):

                response = requests.post(
                    API_URL,
                    json={"review": review},
                    timeout=30,
                )

            if response.status_code == 200:

                api_result = response.json()

                prediction = {
                    "review": review.strip(),
                    "sentiment": api_result["sentiment"],
                    "probabilities": api_result["probabilities"],
                }

                st.session_state.latest_prediction = prediction

                st.session_state.prediction_history.insert(
                    0, prediction
                )

                st.session_state.prediction_history = (
                    st.session_state.prediction_history[:MAX_HISTORY]
                )

            elif response.status_code in (400, 422):

                detail = response.json().get(
                    "detail", "Invalid review."
                )

                if isinstance(detail, list):
                    detail = (
                        detail[0].get("msg", "Invalid review.")
                        if detail
                        else "Invalid review."
                    )

                st.warning(str(detail))

            else:
                st.error(
                    f"API returned an error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to the API. "
                "Make sure FastAPI is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. Please try again."
            )

        except requests.exceptions.RequestException as error:

            st.error(f"Request failed: {error}")

        except (ValueError, KeyError, TypeError):

            st.error(
                "The API returned an unexpected response format."
            )


# --------------------------------------------------
# Prediction results
# --------------------------------------------------

result = st.session_state.latest_prediction

if result is not None:

    sentiment = result["sentiment"]
    probabilities = result["probabilities"]

    positive_score = float(probabilities["positive"]) * 100
    negative_score = float(probabilities["negative"]) * 100

    close_call = is_close_call(probabilities)

    st.divider()

    st.markdown(
        '<div class="section-label">ANALYSIS RESULTS</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Sentiment Analysis")

    if sentiment == "positive":

        label = "Positive Sentiment"
        emoji = "😊"
        description = (
            "The model leans toward positive sentiment."
        )

    else:

        label = "Negative Sentiment"
        emoji = "😞"
        description = (
            "The model leans toward negative sentiment."
        )

    st.markdown(
        f"""
<div class="result-banner {sentiment}">
    <div class="eyebrow">MODEL PREDICTION</div>
    <div class="result-title">{emoji} {label}</div>
    <div class="result-subtitle">{description}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ----------------------------------------------
    # Uncertainty information
    # ----------------------------------------------

    if close_call:

        st.info(
            "**Close-call prediction:** The model's positive and "
            "negative scores are relatively close. This may happen "
            "with mixed or ambiguous reviews. Treat the predicted "
            "label cautiously."
        )

    else:

        st.caption(
            "The model shows a clearer preference for one sentiment, "
            "but it can still make mistakes."
        )

    # ----------------------------------------------
    # Probability cards
    # ----------------------------------------------

    score_col1, score_col2 = st.columns(
        2, gap="medium"
    )

    for column, name, score, css_class, icon in (
        (
            score_col1,
            "Positive",
            positive_score,
            "positive",
            "😊",
        ),
        (
            score_col2,
            "Negative",
            negative_score,
            "negative",
            "😞",
        ),
    ):

        with column:

            st.markdown(
                f"""
<div class="score-card">
    <div class="score-header">
        <span>{icon} {name}</span>
        <span class="score-value">{score:.2f}%</span>
    </div>
    <div class="score-track">
        <div class="score-fill {css_class}"
             style="width: {score:.2f}%"></div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

    st.caption(
        "These scores are model estimates, not guarantees of "
        "correctness. A close call is not a neutral sentiment "
        "prediction: the current model has only positive "
        "and negative classes."
    )


# --------------------------------------------------
# Prediction history
# --------------------------------------------------

if st.session_state.prediction_history:

    st.divider()

    st.subheader("Recent Analyses")

    st.caption(
        "Up to 10 predictions stored for this Streamlit session."
    )

    for item in st.session_state.prediction_history:

        history_sentiment = item["sentiment"]
        history_probabilities = item["probabilities"]
        history_review = item["review"]

        preview = history_review[:65]

        if len(history_review) > 65:
            preview += "..."

        history_icon = (
            "🟢"
            if history_sentiment == "positive"
            else "🔴"
        )

        with st.expander(
            f"{history_icon} "
            f"{history_sentiment.title()} — {preview}"
        ):

            st.write("**Review**")
            st.write(history_review)

            if is_close_call(history_probabilities):
                st.caption("Close-call prediction")

            history_col1, history_col2 = st.columns(2)

            with history_col1:
                st.metric(
                    "Positive",
                    f"{float(history_probabilities['positive']) * 100:.2f}%",
                )

            with history_col2:
                st.metric(
                    "Negative",
                    f"{float(history_probabilities['negative']) * 100:.2f}%",
                )

    st.button(
        "Clear History",
        on_click=clear_history,
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.markdown(
    """
<div class="footer-note">
    ReviewSense · NLP-powered Movie Sentiment Analysis
    <br>
    Built with Streamlit, FastAPI, Scikit-learn and Python
</div>
""",
    unsafe_allow_html=True,
)

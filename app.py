
import streamlit as st
import requests

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ReviewSense | Movie Sentiment Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://127.0.0.1:8000/predict"


# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown("""
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

    .eyebrow {
        color: #a78bfa;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero-title {
        font-size: clamp(2.5rem, 6vw, 4rem);
        font-weight: 800;
        letter-spacing: -2px;
        margin: 0.6rem 0;
        line-height: 1.2;
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

    .section-label {
        color: #a78bfa;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 0.8rem;
    }

    .info-card {
        background: #151d30;
        border: 1px solid #29344d;
        border-radius: 16px;
        padding: 24px;
        margin-top: 27px;
    }

    .info-card h3 {
        margin-top: 0;
        font-size: 1.2rem;
    }

    .info-card p {
        color: #a2acc0;
        line-height: 1.7;
        font-size: 0.94rem;
    }

    .pipeline-step {
        padding: 11px 0;
        border-bottom: 1px solid #29344d;
        color: #d7ddec;
        font-size: 0.9rem;
    }

    .stTextArea textarea {
        background-color: #151d30 !important;
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
        margin: 15px 0 20px 0;
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
        padding: 20px;
        background: #151d30;
        border: 1px solid #29344d;
        border-radius: 14px;
        margin-bottom: 15px;
    }

    .score-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        gap: 12px;
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
""", unsafe_allow_html=True)


# --------------------------------------------------
# Hero section
# --------------------------------------------------

st.markdown("""
<div class="eyebrow">Movie Review Intelligence</div>

<div class="hero-title">
    🎬 Review<span>Sense</span>
</div>

<div class="hero-description">
    Discover the sentiment behind movie reviews.
    Our machine learning model analyses review text
    to identify positive and negative opinions.
</div>
""", unsafe_allow_html=True)

st.divider()


# --------------------------------------------------
# Main content
# --------------------------------------------------

left_col, right_col = st.columns([1.7, 1], gap="large")

with left_col:
    st.markdown(
        '<div class="section-label">01 / ANALYZE A REVIEW</div>',
        unsafe_allow_html=True
    )

    st.subheader("What's your take on the movie?")

    review = st.text_area(
        "Your movie review",
        placeholder=(
            "Enter a movie review here...\n\n"
            "Example: The performances were excellent, "
            "but the story was disappointing."
        ),
        height=210,
        max_chars=10000
    )

    st.caption("Enter a movie review to analyse its sentiment.")

    analyse_button = st.button(
        "✨ Analyse Sentiment",
        type="primary",
        use_container_width=True
    )


with right_col:
    st.markdown("""
    <div class="info-card">
        <h3>How ReviewSense Works</h3>
        <p>
            ReviewSense uses Natural Language Processing
            to identify sentiment in movie reviews.
        </p>

        <div class="pipeline-step">
            📝 &nbsp; 1. Enter your movie review
        </div>

        <div class="pipeline-step">
            ⚙️ &nbsp; 2. TF-IDF converts text into features
        </div>

        <div class="pipeline-step">
            🧠 &nbsp; 3. Logistic Regression predicts sentiment
        </div>

        <div class="pipeline-step">
            📊 &nbsp; 4. Explore the prediction scores
        </div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# API request
# --------------------------------------------------

result = None

if analyse_button:

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

            elif response.status_code == 422:
                error = response.json()
                detail = error.get("detail", "Invalid review.")

                if isinstance(detail, list):
                    detail = (
                        detail[0].get("msg", "Invalid review.")
                        if detail else "Invalid review."
                    )

                st.warning(str(detail))

            else:
                st.error(
                    f"API returned an error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the ReviewSense API. "
                "Make sure the FastAPI backend is running."
            )

        except requests.exceptions.Timeout:
            st.error("The request timed out. Please try again.")

        except requests.exceptions.RequestException as error:
            st.error(f"Request failed: {error}")


# --------------------------------------------------
# Prediction results
# --------------------------------------------------

if result is not None:

    sentiment = result["sentiment"]
    probabilities = result["probabilities"]

    positive_score = float(probabilities["positive"]) * 100
    negative_score = float(probabilities["negative"]) * 100

    st.divider()

    st.markdown(
        '<div class="section-label">02 / ANALYSIS RESULTS</div>',
        unsafe_allow_html=True
    )

    st.subheader("Sentiment Analysis")

    if sentiment == "positive":
        label = "Positive Sentiment"
        emoji = "😊"
        description = (
            "This review expresses predominantly positive sentiment."
        )
    else:
        label = "Negative Sentiment"
        emoji = "😞"
        description = (
            "This review expresses predominantly negative sentiment."
        )

    st.markdown(f"""
    <div class="result-banner {sentiment}">
        <div class="eyebrow">MODEL PREDICTION</div>
        <div class="result-title">{emoji} {label}</div>
        <div class="result-subtitle">{description}</div>
    </div>
    """, unsafe_allow_html=True)

    score_col1, score_col2 = st.columns(2, gap="medium")

    with score_col1:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-header">
                <span>😊 Positive</span>
                <span class="score-value">{positive_score:.2f}%</span>
            </div>
            <div class="score-track">
                <div class="score-fill positive"
                     style="width: {positive_score:.2f}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with score_col2:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-header">
                <span>😞 Negative</span>
                <span class="score-value">{negative_score:.2f}%</span>
            </div>
            <div class="score-track">
                <div class="score-fill negative"
                     style="width: {negative_score:.2f}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "These are model probability estimates, not guarantees "
        "of prediction correctness."
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.markdown("""
<div class="footer-note">
    ReviewSense · NLP-powered Movie Sentiment Analysis
    <br>
    Built with Streamlit, FastAPI, Scikit-learn and Python
</div>
""", unsafe_allow_html=True)

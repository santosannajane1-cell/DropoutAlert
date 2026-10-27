'''Reusable page layout components: heading, footer, and prediction result.'''
import streamlit as st


def show_footer():
    st.divider()
    st.caption(
        "DropoutAlert | Research Prototype | "
        "Predictions are intended to support academic review."
    )


def show_page_heading(title, description):
    st.title(title)
    st.markdown(
        f'<div class="page-note">{description}</div>',
        unsafe_allow_html=True
    )
    st.divider()


def show_risk_result(record):
    st.subheader("Prediction Result")
    st.write(f"**Student:** {record['Student Name']}")

    if record["Prediction"] == "At Risk":
        st.markdown(
            '<div class="result-panel risk-panel">'
            'AT RISK — Further academic review recommended'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="result-panel safe-panel">'
            'NOT FLAGGED AS AT RISK'
            '</div>',
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estimated Dropout Risk", f"{record['Risk Percentage']:.2f}%")
    with col2:
        st.metric("Prediction Status", record["Prediction"])

    st.progress(max(0.0, min(1.0, record["Risk Percentage"] / 100)))
    st.caption("Estimated probability of belonging to the dropout class.")
    st.info(
        "This is a model-generated estimate, not a final decision. "
        "Consider the student's circumstances and other relevant "
        "evidence before determining appropriate support."
    )

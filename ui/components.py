
"""Reusable HTML components for DropoutAlert."""
import streamlit as st


def welcome_banner(student_name="Student"):
    """Display the dashboard welcome banner."""

    html = f"""
    <div class="welcome-banner">
        <div class="welcome-content">
            <div class="welcome-label">STUDENT EARLY-WARNING SYSTEM</div>
            <h2>Welcome to DropoutAlert!</h2>
            <p>
                Hello, {student_name}! Monitor student predictions
                and identify learners who may need academic support.
            </p>
        </div>
        <div class="welcome-icon">🎓</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def section_title(title, subtitle=""):
    """Display a reusable dashboard section heading."""

    html = f"""
    <div class="section-heading">
        <h3>{title}</h3>
        <p>{subtitle}</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def info_card(title, value, description, icon="📊"):
    """Display a reusable HTML information card."""

    html = f"""
    <div class="info-card">
        <div class="info-card-icon">{icon}</div>
        <div class="info-card-title">{title}</div>
        <div class="info-card-value">{value}</div>
        <div class="info-card-description">{description}</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

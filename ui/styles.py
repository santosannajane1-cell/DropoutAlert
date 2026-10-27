
"""Professional visual theme and CSS styling for DropoutAlert."""

import streamlit as st


def apply_styles():
    """Apply consistent professional dashboard styling."""

    st.markdown("""
    <style>

        /* ----------------------------------
           COLOR PALETTE
        ---------------------------------- */

        :root {
            --primary: #1E3A5F;
            --primary-light: #2F5D8A;
            --background: #F4F6F9;
            --surface: #FFFFFF;
            --border: #E1E6ED;
            --text: #263445;
            --muted: #697586;

            --green: #2E7D5B;
            --orange: #B7791F;
            --red: #B93838;
        }


        /* ----------------------------------
           MAIN APPLICATION
        ---------------------------------- */

        .stApp {
            background-color: var(--background);
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1500px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }


        /* ----------------------------------
           TYPOGRAPHY
        ---------------------------------- */

        h1, h2, h3 {
            color: var(--primary) !important;
            font-weight: 700 !important;
        }

        h1 {
            font-size: 1.8rem !important;
        }

        h2 {
            font-size: 1.3rem !important;
        }

        h3 {
            font-size: 1.05rem !important;
        }

        p, label, li {
            color: var(--text);
        }

        [data-testid="stCaptionContainer"] p {
            color: var(--muted);
            font-size: 0.82rem;
        }


        /* ----------------------------------
           SIDEBAR
        ---------------------------------- */

        [data-testid="stSidebar"] {
            background-color: var(--primary);
            border-right: 1px solid #D9E1EA;
        }

        [data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.20);
        }

        .brand-title {
            color: #FFFFFF;
            font-size: 25px;
            font-weight: 800;
            text-align: center;
            margin-top: 8px;
        }

        .brand-subtitle {
            color: #DCE5EF;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 1px;
            line-height: 1.6;
            text-align: center;
        }

        [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 5px;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            padding: 10px 12px;
            border-radius: 6px;
        }

        /* Remove sidebar hover effects */
        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background-color: transparent !important;
        }


        /* ----------------------------------
           DASHBOARD WELCOME BANNER
        ---------------------------------- */

        .welcome-banner {
            background-color: #FFFFFF;
            border: 1px solid var(--border);
            border-left: 5px solid var(--primary);
            border-radius: 10px;
            padding: 22px 25px;
            margin: 2px 0 20px;
            min-height: 110px;
        }

        .welcome-title {
            font-size: 1.45rem;
            font-weight: 800;
            color: var(--primary);
        }

        .welcome-subtitle {
            color: var(--muted);
            font-size: 0.88rem;
            margin-top: 5px;
        }

        .welcome-icon {
            font-size: 2.2rem;
            text-align: right;
        }


        /* ----------------------------------
           METRIC CARDS
        ---------------------------------- */

        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
        }

        [data-testid="stMetricLabel"] p {
            color: #657386 !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
        }

        [data-testid="stMetricValue"] {
            color: var(--primary) !important;
            font-weight: 750 !important;
            font-size: 1.65rem !important;
        }

        [data-testid="stMetricDelta"] {
            font-size: 0.75rem;
        }


        /* ----------------------------------
           DATA TABLES
        ---------------------------------- */

        [data-testid="stDataFrame"] {
            background-color: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
        }


        /* ----------------------------------
           FORMS
        ---------------------------------- */

        [data-testid="stForm"] {
            background-color: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 22px;
        }


        /* ----------------------------------
           BUTTONS
        ---------------------------------- */

        .stButton > button,
        .stFormSubmitButton > button,
        .stDownloadButton > button {
            min-height: 40px;
            border-radius: 6px;
            font-weight: 600;
            box-shadow: none !important;
            transition: none !important;
        }

        /* Primary buttons */
        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {
            background-color: var(--primary);
            color: #FFFFFF;
            border: 1px solid var(--primary);
        }

        /* Keep buttons visually consistent on hover */
        .stButton > button:hover,
        .stFormSubmitButton > button:hover,
        .stDownloadButton > button:hover {
            box-shadow: none !important;
            transform: none !important;
            transition: none !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {
            background-color: var(--primary);
            color: #FFFFFF;
            border-color: var(--primary);
        }


        /* ----------------------------------
           PROGRESS BARS
        ---------------------------------- */

        [data-testid="stProgress"] > div {
            background-color: #E5EAF0;
            border-radius: 10px;
        }

        [data-testid="stProgress"] > div > div {
            background-color: var(--primary-light);
            border-radius: 10px;
        }


        /* ----------------------------------
           NOTIFICATIONS
        ---------------------------------- */

        .notice-item {
            display: flex;
            gap: 11px;
            padding: 12px 0;
            border-bottom: 1px solid #E9EDF2;
            align-items: flex-start;
        }

        .notice-icon {
            background-color: #EDF2F7;
            color: var(--primary);
            border-radius: 6px;
            padding: 7px 9px;
            font-size: 1.05rem;
        }

        .notice-title {
            font-size: 0.83rem;
            font-weight: 700;
            color: var(--text);
        }

        .notice-copy {
            font-size: 0.75rem;
            color: var(--muted);
            margin-top: 3px;
        }


        /* ----------------------------------
           MINI PANELS
        ---------------------------------- */

        .mini-panel {
            background-color: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px 18px;
            height: 100%;
        }


        /* ----------------------------------
           PREDICTION RESULT PANELS
        ---------------------------------- */

        .result-panel {
            padding: 16px 19px;
            border-radius: 8px;
            margin: 8px 0 15px;
            font-size: 0.95rem;
            font-weight: 700;
        }

        .risk-panel {
            background-color: #FDF0F0;
            border: 1px solid #E9CACA;
            border-left: 5px solid var(--red);
            color: #8B2B2B;
        }

        .safe-panel {
            background-color: #EDF6F1;
            border: 1px solid #C9DFD1;
            border-left: 5px solid var(--green);
            color: #245B40;
        }


        /* ----------------------------------
           ALERTS AND DIVIDERS
        ---------------------------------- */

        [data-testid="stAlert"] {
            border-radius: 8px;
        }

        hr {
            border-color: var(--border);
        }


        /* ----------------------------------
           REMOVE FOOTER
        ---------------------------------- */

        footer {
            visibility: hidden;
        }

    </style>
    """, unsafe_allow_html=True)

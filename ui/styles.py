
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
   PROFESSIONAL INTERACTIVE BUTTONS
---------------------------------- */

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    min-height: 42px;
    padding: 0.5rem 1.1rem;
    border-radius: 8px;
    font-weight: 600;
    border: 1px solid #D5DEE9;
    box-shadow: 0 2px 4px rgba(30, 58, 95, 0.05);
    transition:
        background-color 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease,
        transform 0.2s ease;
    user-select: none;
    -webkit-user-select: none;
}

/* Primary action buttons */

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: #1E3A5F;
    color: #FFFFFF;
    border: 1px solid #1E3A5F;
}

/* Elegant hover effect */

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #7892B0;
    box-shadow: 0 4px 10px rgba(30, 58, 95, 0.12);
    transform: translateY(-1px);
}

/* Primary button hover */

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    background: #2F527A;
    border-color: #2F527A;
    color: #FFFFFF;
}

/* Keyboard accessibility */

.stButton > button:focus-visible,
.stFormSubmitButton > button:focus-visible,
.stDownloadButton > button:focus-visible {
    outline: 2px solid #7892B0;
    outline-offset: 3px;
}

/* Keep button text non-editable */

.stButton > button *,
.stFormSubmitButton > button *,
.stDownloadButton > button * {
    user-select: none;
    -webkit-user-select: none;
}

/* ----------------------------------
   INTERACTIVE DASHBOARD CARDS
---------------------------------- */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E1E6ED;
    border-radius: 10px;
    padding: 16px;
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease,
        transform 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #B7C7D9;
    box-shadow: 0 5px 14px rgba(30, 58, 95, 0.07);
    transform: translateY(-2px);
}

/* ----------------------------------
   INTERACTIVE PANELS
---------------------------------- */

.mini-panel {
    background: #FFFFFF;
    border: 1px solid #E1E6ED;
    border-radius: 10px;
    padding: 16px 18px;
    height: 100%;
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

.mini-panel:hover {
    border-color: #B7C7D9;
    box-shadow: 0 4px 12px rgba(30, 58, 95, 0.06);
}

/* ----------------------------------
   FORM INPUTS
---------------------------------- */

.stTextInput input,
.stNumberInput input,
.stSelectbox [data-baseweb="select"],
.stTextArea textarea {
    border-radius: 7px;
}

/* ----------------------------------
   SIDEBAR NAVIGATION
---------------------------------- */

[data-testid="stSidebar"] [role="radiogroup"] label {
    border-radius: 7px;
    transition: background-color 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background-color: rgba(255, 255, 255, 0.12);
}

/* ----------------------------------
   TABLES
---------------------------------- */

[data-testid="stDataFrame"] {
    border: 1px solid #E1E6ED;
    border-radius: 9px;
    overflow: hidden;
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

        /* Generate Prediction Button */
div.stButton > button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 20px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.2s ease-in-out !important;
}

/* Button Hover Effect */
div.stButton > button:hover {
    background-color: #1D4ED8 !important;
    color: #FFFFFF !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
}

/* Button Focus */
div.stButton > button:focus {
    outline: 2px solid #93C5FD !important;
    outline-offset: 2px !important;
}

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

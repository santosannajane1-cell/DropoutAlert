
import streamlit as st
from ui.styles import apply_styles
from ui.layout import show_footer, show_page_heading, show_risk_result
from ui.forms import student_prediction_form
import pandas as pd
import pickle
import sqlite3
from datetime import datetime
from pathlib import Path

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="DropoutAlert | Early-Warning System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
DB_PATH = BASE_DIR / "dropoutalert.db"

NAVY = "#003049"
STEEL_BLUE = "#669BBC"
CRIMSON = "#C1121F"

apply_styles()


# =====================================================
# STUDENT ID HELPER
# =====================================================

def format_student_id(record_id, prediction_date=None):
    """Create a readable ID without changing the database ID."""
    year = datetime.now().year

    if prediction_date:
        try:
            year = datetime.strptime(
                str(prediction_date),
                "%Y-%m-%d %H:%M:%S"
            ).year
        except (ValueError, TypeError):
            pass

    return f"DA-{year}-{int(record_id):03d}"


# =====================================================
# LOAD TRAINED MODEL
# =====================================================

@st.cache_resource
def load_model_files():
    with open(MODEL_DIR / "dropout_model.pkl", "rb") as file:
        trained_model = pickle.load(file)

    with open(MODEL_DIR / "features.pkl", "rb") as file:
        model_features = pickle.load(file)

    return trained_model, model_features


model, features = load_model_files()


# =====================================================
# DATABASE
# =====================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prediction_date TEXT NOT NULL,
                student_name TEXT NOT NULL,
                admission_grade REAL NOT NULL,
                age INTEGER NOT NULL,
                units_enrolled INTEGER NOT NULL,
                units_approved INTEGER NOT NULL,
                semester_grade REAL NOT NULL,
                evaluations INTEGER NOT NULL,
                attendance_rate REAL NOT NULL DEFAULT 100,
                absences INTEGER NOT NULL DEFAULT 0,
                prediction TEXT NOT NULL,
                risk_percentage REAL NOT NULL
            )
        """)

        # Add the attendance columns to existing databases, if needed.
        existing_columns = {
            row[1] for row in conn.execute("PRAGMA table_info(predictions)")
        }
        if "attendance_rate" not in existing_columns:
            conn.execute(
                "ALTER TABLE predictions ADD COLUMN attendance_rate REAL NOT NULL DEFAULT 100"
            )
        if "absences" not in existing_columns:
            conn.execute(
                "ALTER TABLE predictions ADD COLUMN absences INTEGER NOT NULL DEFAULT 0"
            )


def save_prediction(record):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO predictions (
                prediction_date,
                student_name,
                admission_grade,
                age,
                units_enrolled,
                units_approved,
                semester_grade,
                evaluations,
                attendance_rate,
                absences,
                prediction,
                risk_percentage
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record["Date & Time"],
            record["Student Name"],
            record["Admission Grade"],
            record["Age"],
            record["Units Enrolled"],
            record["Units Approved"],
            record["Semester Average"],
            record["Evaluations"],
            record["Attendance Rate"],
            record["Absences"],
            record["Prediction"],
            record["Risk Percentage"]
        ))

        return cursor.lastrowid


def load_predictions(search="", risk_filter="All Records"):
    query = """
        SELECT
            id AS 'Record ID',
            prediction_date AS 'Date & Time',
            student_name AS 'Student Name',
            admission_grade AS 'Admission Grade',
            age AS 'Age',
            units_enrolled AS 'Units Enrolled',
            units_approved AS 'Units Approved',
            semester_grade AS 'Semester Average',
            evaluations AS 'Evaluations',
            attendance_rate AS 'Attendance Rate (%)',
            absences AS 'Absences',
            prediction AS 'Prediction',
            risk_percentage AS 'Risk Percentage'
        FROM predictions
        WHERE student_name LIKE ?
    """

    params = [f"%{search.strip()}%"]

    if risk_filter != "All Records":
        query += " AND prediction = ?"
        params.append(risk_filter)

    query += " ORDER BY id DESC"

    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)


def load_record(record_id):
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT
                id,
                prediction_date,
                student_name,
                admission_grade,
                age,
                units_enrolled,
                units_approved,
                semester_grade,
                evaluations,
                attendance_rate,
                absences,
                prediction,
                risk_percentage
            FROM predictions
            WHERE id = ?
        """, (record_id,))

        return cursor.fetchone()


def delete_record(record_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM predictions WHERE id = ?",
            (record_id,)
        )


initialize_database()


# =====================================================
# SHARED HELPERS
# =====================================================

def format_risk_table(data):
    display = data.copy()

    if "Risk Percentage" in display.columns:
        display["Risk Percentage"] = display[
            "Risk Percentage"
        ].map(lambda value: f"{value:.2f}%")

    return display


def add_student_ids(data):
    """Add formatted student IDs to a copy of the records."""
    display = data.copy()

    if not display.empty:
        display["Student ID"] = display.apply(
            lambda row: format_student_id(
                row["Record ID"],
                row["Date & Time"]
            ),
            axis=1
        )

    return display


def navigate_to(page_name):
    st.session_state["page_navigation"] = page_name


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:
    st.markdown(
        '<div class="brand-title">DropoutAlert</div>'
        '<div class="brand-subtitle">'
        'STUDENT EARLY-WARNING SYSTEM'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "New Prediction",
            "Student Records",
            "Risk Analysis"
        ],
        label_visibility="visible",
        key="page_navigation"
    )

    st.divider()
    st.caption("Academic Research Prototype")


# =====================================================
# SHARED DASHBOARD DATA
# =====================================================

all_records = load_predictions()
total_predictions = len(all_records)

if total_predictions:
    at_risk_count = int(
        (all_records["Prediction"] == "At Risk").sum()
    )
    not_at_risk_count = total_predictions - at_risk_count
    average_risk = float(
        all_records["Risk Percentage"].mean()
    )
else:
    at_risk_count = 0
    not_at_risk_count = 0
    average_risk = 0.0


# =====================================================
# PAGE 1: DASHBOARD
# =====================================================

if page == "Dashboard":

    welcome_left, welcome_right = st.columns([5, 1])

    with welcome_left:
        st.markdown(
            """
            <div class="welcome-banner">
                <div style="color:#64748B;font-size:.85rem;font-weight:600;">
                    STUDENT MONITORING
                </div>
                <div class="welcome-title">Welcome to DropoutAlert!</div>
                <div class="welcome-subtitle">
                    Monitor student predictions and identify learners
                    who may need academic support.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with welcome_right:
        st.markdown(
            '<div class="welcome-banner welcome-icon">🎓📘</div>',
            unsafe_allow_html=True
        )

    # Summary cards
    metric_cols = st.columns(4)

    metric_cols[0].metric(
        "Total Predictions",
        total_predictions
    )
    metric_cols[1].metric(
        "Students At Risk",
        at_risk_count
    )
    metric_cols[2].metric(
        "Not At Risk",
        not_at_risk_count
    )
    metric_cols[3].metric(
        "Average Risk",
        f"{average_risk:.1f}%"
    )

    st.write("")

    # Recent predictions and notice board
    recent_col, notice_col = st.columns([1.25, 1])

    with recent_col:
        st.markdown(
            '<div class="mini-panel">',
            unsafe_allow_html=True
        )

        st.subheader("Recent Predictions")

        if total_predictions:
            recent = all_records.head(6).copy()
            recent["Student ID"] = recent.apply(
                lambda row: format_student_id(
                    row["Record ID"],
                    row["Date & Time"]
                ),
                axis=1
            )

            recent_view = recent[
                [
                    "Student ID",
                    "Student Name",
                    "Prediction",
                    "Risk Percentage"
                ]
            ].copy()

            recent_view["Risk Percentage"] = (
                recent_view["Risk Percentage"].map(
                    lambda value: f"{value:.1f}%"
                )
            )

            st.dataframe(
                recent_view,
                use_container_width=True,
                hide_index=True,
                height=245
            )
        else:
            st.info(
                "No prediction records yet. "
                "Create a new prediction to see results here."
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with notice_col:
        st.markdown(
            '<div class="mini-panel">',
            unsafe_allow_html=True
        )

        st.subheader("Notice Board")

        notices = [
            (
                "📢",
                "Academic review reminder",
                "Students marked At Risk should be reviewed "
                "with their academic context."
            ),
            (
                "📊",
                "Prediction overview",
                "The dashboard summarizes model estimates, "
                "not final decisions."
            ),
            (
                "🛡️",
                "Use results responsibly",
                "Combine model output with adviser judgment "
                "and additional evidence."
            )
        ]

        for icon, title, copy in notices:
            st.markdown(
                f'<div class="notice-item">'
                f'<div class="notice-icon">{icon}</div>'
                f'<div><div class="notice-title">{title}</div>'
                f'<div class="notice-copy">{copy}</div></div></div>',
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.write("")

    # Lower dashboard section
    analysis_col, quick_col, performance_col = st.columns(
        [1, 1, 1.15]
    )

    with analysis_col:
        st.markdown(
            '<div class="mini-panel">',
            unsafe_allow_html=True
        )

        st.subheader("Prediction Distribution")

        if total_predictions:
            chart_data = pd.DataFrame({
                "Status": ["At Risk", "Not At Risk"],
                "Records": [at_risk_count, not_at_risk_count]
            })

            st.bar_chart(
                chart_data,
                x="Status",
                y="Records",
                color=STEEL_BLUE,
                height=210
            )
        else:
            st.info("Create a prediction to populate this chart.")

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with quick_col:
        st.markdown(
            '<div class="mini-panel">',
            unsafe_allow_html=True
        )

        st.subheader("Quick Access")
        st.caption("Go directly to a common task")

        st.button(
            "➕ New Prediction",
            use_container_width=True,
            on_click=navigate_to,
            args=("New Prediction",)
        )

        st.button(
            "📋 Student Records",
            use_container_width=True,
            on_click=navigate_to,
            args=("Student Records",)
        )

        st.button(
            "📈 Risk Analysis",
            use_container_width=True,
            on_click=navigate_to,
            args=("Risk Analysis",)
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with performance_col:
        st.markdown(
            '<div class="mini-panel">',
            unsafe_allow_html=True
        )

        st.subheader("Risk Overview")
        st.metric(
            "Average Estimated Risk",
            f"{average_risk:.2f}%"
        )

        st.progress(
            max(0.0, min(1.0, average_risk / 100))
        )

        st.caption(
            "Average estimated probability across saved predictions. "
            "This is a screening aid, not a standalone decision."
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    show_footer()


# =====================================================
# PAGE 2: NEW PREDICTION
# =====================================================

elif page == "New Prediction":

    show_page_heading(
        "New Prediction",
        "Enter the student's information to estimate dropout risk."
    )

    form_values = student_prediction_form()

    st.markdown("### Attendance Information")
    st.caption(
        "For counselor reference only. Attendance is saved with the student record "
        "and does not affect the machine-learning prediction."
    )
    attendance_col1, attendance_col2 = st.columns(2)
    with attendance_col1:
        attendance_rate = st.number_input(
            "Attendance Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=100.0,
            step=1.0,
            help="Enter the student's attendance percentage from 0 to 100."
        )
    with attendance_col2:
        absences = st.number_input(
            "Number of Absences",
            min_value=0,
            max_value=365,
            value=0,
            step=1,
            help="Enter the total number of absences."
        )

    submitted = form_values["submitted"]
    student_name = form_values["student_name"]
    admission_grade = form_values["admission_grade"]
    age = form_values["age"]
    units_enrolled = form_values["units_enrolled"]
    units_approved = form_values["units_approved"]
    semester_grade = form_values["semester_grade"]
    evaluations = form_values["evaluations"]

    if submitted:
        if not student_name.strip():
            st.error("Enter the student's name.")

        elif units_approved > units_enrolled:
            st.error(
                "Approved units cannot exceed enrolled units."
            )

        else:
            input_data = pd.DataFrame(
                [[
                    admission_grade,
                    age,
                    units_enrolled,
                    units_approved,
                    semester_grade,
                    evaluations
                ]],
                columns=features
            )

            try:
                prediction = model.predict(input_data)[0]
                probabilities = model.predict_proba(input_data)[0]

                class_index = list(model.classes_).index(1)

                risk_percentage = (
                    float(probabilities[class_index]) * 100
                )

                status = (
                    "At Risk" if prediction == 1
                    else "Not At Risk"
                )

                record = {
                    "Date & Time": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "Student Name": student_name.strip(),
                    "Admission Grade": admission_grade,
                    "Age": age,
                    "Units Enrolled": units_enrolled,
                    "Units Approved": units_approved,
                    "Semester Average": semester_grade,
                    "Evaluations": evaluations,
                    "Attendance Rate": attendance_rate,
                    "Absences": int(absences),
                    "Prediction": status,
                    "Risk Percentage": round(
                        risk_percentage, 2
                    )
                }

                record_id = save_prediction(record)

                record["Record ID"] = record_id
                record["Student ID"] = format_student_id(
                    record_id,
                    record["Date & Time"]
                )

                st.session_state["latest_prediction"] = record

                st.success(
                    f"Prediction saved successfully. "
                    f"Student ID: {record['Student ID']}"
                )

            except (ValueError, KeyError):
                st.error(
                    "The prediction could not be completed. "
                    "Check the model's expected feature names "
                    "and class labels."
                )

            except Exception as error:
                st.error(
                    "An unexpected error occurred while generating "
                    "the prediction. Check the terminal for details."
                )
                print(f"Prediction error: {error}")

    latest = st.session_state.get("latest_prediction")

    if latest:
        st.divider()

        st.markdown(
            f"**Student ID:** {latest.get('Student ID', format_student_id(latest['Record ID'], latest['Date & Time']))}"
        )

        show_risk_result(latest)

    show_footer()


# =====================================================
# PAGE 3: STUDENT RECORDS
# =====================================================

elif page == "Student Records":

    show_page_heading(
        "Student Records",
        "Search, review, export, and manage saved predictions."
    )

    search_col, filter_col = st.columns([2, 1])

    with search_col:
        search_name = st.text_input(
            "Search Student",
            placeholder="Enter student name"
        )

    with filter_col:
        risk_filter = st.selectbox(
            "Prediction Status",
            [
                "All Records",
                "At Risk",
                "Not At Risk"
            ]
        )

    records = load_predictions(
        search=search_name,
        risk_filter=risk_filter
    )

    st.caption(f"{len(records)} matching record(s)")

    if not records.empty:

        # Create a display-only copy. Database IDs remain unchanged.
        display_records = add_student_ids(records)

        # Number the currently displayed rows from 1.
        display_records.insert(
            0,
            "No.",
            range(1, len(display_records) + 1)
        )

        # Hide the internal database ID from the visible table.
        display_table = display_records.drop(
            columns=["Record ID"]
        )

        st.dataframe(
            format_risk_table(display_table),
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Export CSV",
            data=display_table.to_csv(
                index=False
            ).encode("utf-8"),
            file_name="dropoutalert_student_records.csv",
            mime="text/csv"
        )

        st.divider()
        st.subheader("Record Details")

        # Use the real database ID for lookups and deletion.
        record_ids = records["Record ID"].astype(int).tolist()

        selected_id = st.selectbox(
            "Select Student",
            record_ids,
            format_func=lambda rid: (
                f"{format_student_id(rid, records.loc[records['Record ID'] == rid, 'Date & Time'].iloc[0])}"
                f" — {records.loc[records['Record ID'] == rid, 'Student Name'].iloc[0]}"
            )
        )

        selected = load_record(int(selected_id))

        if selected:
            (
                rid,
                date,
                name,
                admission,
                record_age,
                enrolled,
                approved,
                grade,
                evaluations,
                attendance_rate,
                absences,
                status,
                risk
            ) = selected

            student_id = format_student_id(rid, date)

            with st.container(border=True):
                st.subheader(name)
                st.caption(f"Student ID: {student_id}")

                col1, col2, col3 = st.columns(3)

                col1.metric("Student ID", student_id)
                col2.metric("Prediction", status)
                col3.metric("Estimated Risk", f"{risk:.2f}%")

                st.caption(f"Prediction date: {date}")

                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.write(f"**Admission Grade:** {admission:g}")
                    st.write(f"**Age at Enrollment:** {record_age}")
                    st.write(f"**Units Enrolled:** {enrolled}")

                with detail_col2:
                    st.write(f"**Units Approved:** {approved}")
                    st.write(f"**Semester Average:** {grade:g}")
                    st.write(f"**Evaluations:** {evaluations}")
                    st.write(f"**Attendance Rate:** {attendance_rate:g}%")
                    st.write(f"**Number of Absences:** {absences}")

            st.divider()
            st.subheader("Delete Record")

            st.caption(
                "Deleting a record permanently removes it from the database."
            )

            confirm_delete = st.checkbox(
                f"Confirm deletion of {student_id}",
                key=f"delete_confirm_{rid}"
            )

            if st.button(
                "Delete Selected Record",
                disabled=not confirm_delete,
                type="secondary"
            ):
                delete_record(int(rid))

                latest = st.session_state.get("latest_prediction")

                if latest and latest.get("Record ID") == rid:
                    st.session_state.pop(
                        "latest_prediction",
                        None
                    )

                st.success(f"{student_id} has been deleted.")
                st.rerun()

    else:
        st.info(
            "No matching records. Change the search or status filter."
        )

    show_footer()


# =====================================================
# PAGE 4: RISK ANALYSIS
# =====================================================

elif page == "Risk Analysis":

    show_page_heading(
        "Risk Analysis",
        "Review prediction outcomes and estimated risk probabilities."
    )

    if all_records.empty:
        st.info("Save a prediction to view risk analysis.")

    else:
        left, right = st.columns(2)

        with left:
            st.subheader("Prediction Distribution")

            distribution = pd.DataFrame({
                "Status": ["At Risk", "Not At Risk"],
                "Records": [at_risk_count, not_at_risk_count]
            })

            st.bar_chart(
                distribution,
                x="Status",
                y="Records",
                color=STEEL_BLUE,
                height=300
            )

        with right:
            st.subheader("Estimated Risk Ranges")

            risk_data = all_records[
                "Risk Percentage"
            ].clip(0, 100)

            risk_bins = pd.cut(
                risk_data,
                bins=[-0.01, 25, 50, 75, 100],
                labels=[
                    "0–25%",
                    "Above 25–50%",
                    "Above 50–75%",
                    "Above 75–100%"
                ],
                include_lowest=True
            )

            range_counts = (
                risk_bins.value_counts(sort=False)
                .rename_axis("Risk Range")
                .reset_index(name="Records")
            )

            st.bar_chart(
                range_counts,
                x="Risk Range",
                y="Records",
                color=CRIMSON,
                height=300
            )

        st.divider()
        st.subheader("Risk Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average Estimated Risk",
            f"{average_risk:.2f}%"
        )

        col2.metric(
            "Highest Estimated Risk",
            f"{all_records['Risk Percentage'].max():.2f}%"
        )

        col3.metric(
            "Records with Risk ≥ 70%",
            int(
                (all_records["Risk Percentage"] >= 70).sum()
            )
        )

        st.caption(
            "The 70% threshold is descriptive and has not been "
            "validated as a decision cutoff. Predicted class and "
            "estimated probability are different measures."
        )

        st.divider()
        st.subheader("Records Flagged for Review")

        flagged_records = all_records[
            all_records["Prediction"] == "At Risk"
        ].copy()

        if not flagged_records.empty:
            flagged_records = add_student_ids(flagged_records)

            flagged_view = flagged_records[
                [
                    "Student ID",
                    "Student Name",
                    "Semester Average",
                    "Units Enrolled",
                    "Units Approved",
                    "Risk Percentage"
                ]
            ]

            st.dataframe(
                format_risk_table(flagged_view),
                use_container_width=True,
                hide_index=True
            )

            st.info(
                "These records may warrant further review and "
                "appropriate academic support."
            )

        else:
            st.success(
                "No records are currently flagged as At Risk."
            )

    show_footer()

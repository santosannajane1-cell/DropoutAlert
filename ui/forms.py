
"""Professional form interface for student academic prediction."""

import streamlit as st


def student_prediction_form():
    """Display student, academic, and attendance information."""

    # --------------------------------------------------
    # STUDENT INFORMATION
    # --------------------------------------------------

    st.subheader("Student Information")

    student_name = st.text_input(
        "Full Name",
        placeholder="Enter the student's full name",
        help="Enter the student's complete name."
    )

    st.divider()

    # --------------------------------------------------
    # ACADEMIC INFORMATION
    # --------------------------------------------------

    st.subheader("Academic Information")

    col1, col2 = st.columns(2)

    with col1:

        admission_grade = st.number_input(
            "Admission Grade (0–100)",
            min_value=0.0,
            max_value=100.0,
            value=None,
            step=1.0,
            format="%.0f",
            placeholder="Enter admission grade"
        )

        age = st.number_input(
            "Age at Enrollment",
            min_value=17,
            max_value=70,
            value=None,
            step=1,
            format="%d",
            placeholder="Enter age"
        )

        units_enrolled = st.number_input(
            "First Semester Units Enrolled",
            min_value=0,
            max_value=26,
            value=None,
            step=1,
            format="%d",
            placeholder="0–26"
        )

    with col2:

        units_approved = st.number_input(
            "First Semester Units Passed",
            min_value=0,
            max_value=26,
            value=None,
            step=1,
            format="%d",
            placeholder="0–26"
        )

        semester_grade = st.number_input(
            "First Semester Average Grade (0–100)",
            min_value=0.0,
            max_value=100.0,
            value=None,
            step=1.0,
            format="%.0f",
            placeholder="Enter average grade"
        )

        evaluations = st.number_input(
            "First Semester Evaluations",
            min_value=0,
            max_value=45,
            value=None,
            step=1,
            format="%d",
            placeholder="0–45"
        )

    st.caption(
        "Enter academic grades using the 0–100 scale. "
        "Predictions are estimates intended to support academic "
        "review, not replace adviser judgment."
    )

    st.divider()

    # --------------------------------------------------
    # ATTENDANCE INFORMATION
    # --------------------------------------------------

    st.subheader("Attendance Information")

    st.caption(
        "Attendance is calculated using 100 total class meetings. "
        "This information is for counselor reference only and "
        "does not affect the machine-learning prediction."
    )

    attendance_col1, attendance_col2 = st.columns(2)

    with attendance_col1:

        absences = st.number_input(
            "Number of Absences",
            min_value=0,
            max_value=100,
            value=0,
            step=1,
            help="Enter the total number of class absences."
        )

    # --------------------------------------------------
    # AUTOMATIC ATTENDANCE CALCULATION
    # --------------------------------------------------

    attendance_rate = max(0, 100 - absences)

    with attendance_col2:

        st.metric(
            label="Attendance Rate",
            value=f"{attendance_rate}%"
        )

    st.progress(attendance_rate / 100)

    st.caption(
        f"{100 - absences} attended class meetings "
        f"out of 100 total meetings."
    )

    st.divider()

    # --------------------------------------------------
    # GENERATE PREDICTION BUTTON
    # --------------------------------------------------

    submitted = st.button(
        "Generate Prediction",
        type="primary",
        use_container_width=True
    )

    # --------------------------------------------------
    # RETURN FORM VALUES
    # --------------------------------------------------

    return {
        "submitted": submitted,
        "student_name": student_name,
        "admission_grade": admission_grade,
        "age": age,
        "units_enrolled": units_enrolled,
        "units_approved": units_approved,
        "semester_grade": semester_grade,
        "evaluations": evaluations,
        "attendance_rate": attendance_rate,
        "absences": absences,
    }

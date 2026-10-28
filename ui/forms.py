
"""Professional form interface for student academic prediction."""

import streamlit as st


def student_prediction_form():
    """Display the student prediction form and return submitted values."""

    with st.form("student_prediction_form"):

        st.subheader("Student Information")

        student_name = st.text_input(
            "Full Name",
            placeholder="Enter the student's full name",
            help="Enter the student's complete name."
        )

        st.divider()
        st.subheader("Academic Information")

        col1, col2 = st.columns(2)

        with col1:
            admission_grade = st.number_input(
                "Admission Grade",
                min_value=0,
                max_value=100,
                value=None,
                step=0.1,
                format="%.1f",
                placeholder="0-100"
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
                "First Semester Units Approved",
                min_value=0,
                max_value=26,
                value=None,
                step=1,
                format="%d",
                placeholder="0–26"
            )

            semester_grade = st.number_input(
                "First Semester Average Grade",
                min_value=0,
                max_value=100,
                value=None,
                step=0.01,
                format="%.2f",
                placeholder="0–100"
            )

            evaluations = st.number_input(
                "First Semester Evaluations",
                min_value=0,
                max_value=50,
                value=None,
                step=1,
                format="%d",
                placeholder="0–50"
            )

        st.divider()

        st.caption(
            "Enter values using the dataset's grading scale. "
            "All predictions are estimates intended to support "
            "academic review, not replace adviser judgment."
        )

        submitted = st.form_submit_button(
            "Generate Prediction",
            type="primary",
            use_container_width=True
        )

    return {
        "submitted": submitted,
        "student_name": student_name,
        "admission_grade": admission_grade,
        "age": age,
        "units_enrolled": units_enrolled,
        "units_approved": units_approved,
        "semester_grade": semester_grade,
        "evaluations": evaluations,
    }

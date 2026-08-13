"""Reusable SQL-backed analytics for the university dataset."""

from typing import Dict, Tuple

from src.database import connect_mysql


GRADE_VALUES = (2, 3, 4, 5, 6)
DURATION_LABELS = ("1-2 years", "3 years", "4 years", "more than 4 years")


def get_grade_distribution() -> Dict[int, int]:
    """Return the number of class-student records for each displayed grade."""
    connection = connect_mysql()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT FinalGrade, COUNT(*)
            FROM ClassStudent
            WHERE FinalGrade IN (%s, %s, %s, %s, %s)
            GROUP BY FinalGrade
            """,
            GRADE_VALUES,
        )
        counts = dict(cursor.fetchall())
        return {grade: counts.get(grade, 0) for grade in GRADE_VALUES}
    finally:
        cursor.close()
        connection.close()


def get_student_enrollment_by_gender_and_year() -> Dict[Tuple[int, str], int]:
    """Return student counts grouped by enrollment year and gender."""
    connection = connect_mysql()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT Student.YearStart, Person.Gender, COUNT(*)
            FROM Person
            INNER JOIN Student ON Student.StudentID = Person.PersonID
            WHERE Person.Gender IN ('M', 'F')
            GROUP BY Student.YearStart, Person.Gender
            """,
        )
        return {(year, gender): count for year, gender, count in cursor.fetchall()}
    finally:
        cursor.close()
        connection.close()


def get_study_duration_distribution() -> Dict[str, int]:
    """Return the study-duration buckets used by the dashboard export."""
    connection = connect_mysql()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT
                SUM(CASE WHEN YearEnd - YearStart IN (1, 2) THEN 1 ELSE 0 END),
                SUM(CASE WHEN YearEnd - YearStart = 3 THEN 1 ELSE 0 END),
                SUM(CASE WHEN YearEnd - YearStart = 4 THEN 1 ELSE 0 END),
                SUM(CASE
                    WHEN YearEnd IS NULL OR YearEnd - YearStart > 4 THEN 1
                    ELSE 0
                END)
            FROM Student
            WHERE YearStart IS NOT NULL
            """
        )
        counts = cursor.fetchone()
        return dict(zip(DURATION_LABELS, (int(count or 0) for count in counts)))
    finally:
        cursor.close()
        connection.close()

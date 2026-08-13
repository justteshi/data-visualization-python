"""Export the database-backed analytics as static JSON for a future frontend."""

import json
from pathlib import Path
from typing import Any, Dict

from src.analytics import (
    get_grade_distribution,
    get_student_enrollment_by_gender_and_year,
    get_study_duration_distribution,
)


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "public" / "data" / "analytics.json"
GENDER_ORDER = {"M": 0, "F": 1}


def build_analytics_export() -> Dict[str, Any]:
    """Return the static JSON-ready representation of the analytics layer."""
    grade_distribution = get_grade_distribution()
    enrollment_by_gender_and_year = get_student_enrollment_by_gender_and_year()
    study_duration = get_study_duration_distribution()
    academic_years = sorted({year for year, _ in enrollment_by_gender_and_year})
    gender_totals = {
        gender: sum(
            count
            for (_, record_gender), count in enrollment_by_gender_and_year.items()
            if record_gender == gender
        )
        for gender in GENDER_ORDER
    }
    most_common_grade, most_common_grade_count = max(
        grade_distribution.items(), key=lambda item: (item[1], -item[0])
    )
    largest_duration_group, largest_duration_count = max(
        study_duration.items(), key=lambda item: item[1]
    )

    return {
        "summary": {
            "totalStudents": sum(study_duration.values()),
            "academicYears": {
                "count": len(academic_years),
                "first": academic_years[0],
                "last": academic_years[-1],
            },
            "genderTotals": gender_totals,
            "mostCommonGrade": {
                "grade": most_common_grade,
                "count": most_common_grade_count,
            },
            "largestStudyDurationGroup": {
                "label": largest_duration_group,
                "count": largest_duration_count,
            },
        },
        "gradeDistribution": [
            {"grade": grade, "count": count}
            for grade, count in grade_distribution.items()
        ],
        "studentsByGenderAndYear": [
            {"year": year, "gender": gender, "count": count}
            for (year, gender), count in sorted(
                enrollment_by_gender_and_year.items(),
                key=lambda item: (item[0][0], GENDER_ORDER[item[0][1]]),
            )
        ],
        "studyDuration": [
            {"label": label, "count": count} for label, count in study_duration.items()
        ],
    }


def export_analytics_data(output_path: Path = OUTPUT_PATH) -> None:
    """Write a deterministic UTF-8 JSON export, creating its directory if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(build_analytics_export(), output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")


if __name__ == "__main__":
    export_analytics_data()

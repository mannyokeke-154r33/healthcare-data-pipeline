import pandas as pd
import pytest

from src.pipeline import transform


def test_transform_removes_duplicate_patient_ids():
    data = pd.DataFrame(
        [
            {"patient_id": "P001", "age": 32, "department": "cardiology", "visit_type": "outpatient"},
            {"patient_id": "P001", "age": 32, "department": "cardiology", "visit_type": "outpatient"},
        ]
    )

    result = transform(data)

    assert len(result) == 1


def test_transform_removes_invalid_age():
    data = pd.DataFrame(
        [
            {"patient_id": "P001", "age": 35, "department": "emergency", "visit_type": "emergency"},
            {"patient_id": "P002", "age": 150, "department": "emergency", "visit_type": "emergency"},
        ]
    )

    result = transform(data)

    assert result["patient_id"].tolist() == ["P001"]


def test_transform_requires_expected_columns():
    data = pd.DataFrame([{"patient_id": "P001", "age": 35}])

    with pytest.raises(ValueError):
        transform(data)

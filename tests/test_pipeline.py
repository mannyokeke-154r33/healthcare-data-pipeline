import pandas as pd
import pytest

from src.pipeline import transform


def record(patient_id="P001", age=32, department="cardiology", visit_type="outpatient"):
    return {
        "patient_id": patient_id,
        "age": age,
        "department": department,
        "visit_type": visit_type,
    }


def test_transform_removes_duplicate_patient_ids():
    result = transform(pd.DataFrame([record(), record()]))
    assert len(result) == 1


def test_transform_removes_invalid_age():
    data = pd.DataFrame([record(), record("P002", 150)])
    result = transform(data)
    assert result["patient_id"].tolist() == ["P001"]


@pytest.mark.parametrize("age", [-1, 121, "not-a-number"])
def test_transform_rejects_out_of_range_or_non_numeric_age(age):
    result = transform(pd.DataFrame([record(age=age)]))
    assert result.empty


@pytest.mark.parametrize("age", [0, 120])
def test_transform_accepts_boundary_ages(age):
    result = transform(pd.DataFrame([record(age=age)]))
    assert result["age"].tolist() == [age]


def test_transform_removes_missing_required_values():
    data = pd.DataFrame([record(), record("P002", department=None)])
    result = transform(data)
    assert result["patient_id"].tolist() == ["P001"]


def test_transform_standardizes_text_fields():
    data = pd.DataFrame([record(department="  emergency ", visit_type="  inpatient ")])
    result = transform(data)
    assert result.loc[0, "department"] == "Emergency"
    assert result.loc[0, "visit_type"] == "Inpatient"


def test_transform_requires_expected_columns():
    data = pd.DataFrame([{"patient_id": "P001", "age": 35}])
    with pytest.raises(ValueError, match="Missing required columns"):
        transform(data)


def test_transform_handles_empty_dataset_with_columns():
    data = pd.DataFrame(columns=["patient_id", "age", "department", "visit_type"])
    result = transform(data)
    assert result.empty

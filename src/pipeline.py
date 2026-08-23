"""Simple healthcare ETL pipeline used for portfolio demonstration."""

from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = {"patient_id", "age", "department", "visit_type"}


def extract(file_path: str | Path) -> pd.DataFrame:
    """Read healthcare records from a CSV file."""
    return pd.read_csv(file_path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean healthcare records."""
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates(subset=["patient_id"])
    cleaned = cleaned.dropna(subset=list(REQUIRED_COLUMNS))

    cleaned["patient_id"] = cleaned["patient_id"].astype(str).str.strip()
    cleaned["department"] = cleaned["department"].astype(str).str.strip().str.title()
    cleaned["visit_type"] = cleaned["visit_type"].astype(str).str.strip().str.title()
    cleaned["age"] = pd.to_numeric(cleaned["age"], errors="coerce")
    cleaned = cleaned.dropna(subset=["age"])
    cleaned = cleaned[cleaned["age"].between(0, 120)]
    cleaned["age"] = cleaned["age"].astype(int)

    return cleaned.reset_index(drop=True)


def main() -> None:
    input_path = Path("data/sample_healthcare_data.csv")
    output_path = Path("data/processed_healthcare_data.csv")

    raw = extract(input_path)
    cleaned = transform(raw)
    cleaned.to_csv(output_path, index=False)

    print(f"Records extracted: {len(raw)}")
    print(f"Records after validation: {len(cleaned)}")
    print(f"Processed data written to: {output_path}")


if __name__ == "__main__":
    main()

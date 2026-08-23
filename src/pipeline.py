"""Healthcare ETL pipeline for cleaning, validating, and loading visit data."""

import os
from pathlib import Path

import pandas as pd
import psycopg

REQUIRED_COLUMNS = {"patient_id", "age", "department", "visit_type"}


def extract(file_path: str | Path) -> pd.DataFrame:
    """Read healthcare records from a CSV file."""
    return pd.read_csv(file_path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Validate, standardize, and clean healthcare records."""
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    cleaned = df.copy()
    cleaned = cleaned.dropna(subset=list(REQUIRED_COLUMNS))
    cleaned["patient_id"] = cleaned["patient_id"].astype(str).str.strip()
    cleaned["department"] = cleaned["department"].astype(str).str.strip().str.title()
    cleaned["visit_type"] = cleaned["visit_type"].astype(str).str.strip().str.title()
    cleaned["age"] = pd.to_numeric(cleaned["age"], errors="coerce")
    cleaned = cleaned.dropna(subset=["age"])
    cleaned = cleaned[cleaned["age"].between(0, 120)]
    cleaned = cleaned[cleaned["patient_id"] != ""]
    cleaned = cleaned.drop_duplicates(subset=["patient_id"], keep="first")
    cleaned["age"] = cleaned["age"].astype(int)

    return cleaned.reset_index(drop=True)


def database_url() -> str:
    """Return the PostgreSQL connection URL from the environment."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy .env.example values into your shell "
            "or provide a PostgreSQL connection URL."
        )
    return url


def load_to_postgres(df: pd.DataFrame, connection_url: str) -> int:
    """Upsert cleaned records into PostgreSQL and return the number processed."""
    rows = list(
        df[["patient_id", "age", "department", "visit_type"]]
        .itertuples(index=False, name=None)
    )

    if not rows:
        return 0

    statement = """
        INSERT INTO healthcare_visits (patient_id, age, department, visit_type)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (patient_id) DO UPDATE SET
            age = EXCLUDED.age,
            department = EXCLUDED.department,
            visit_type = EXCLUDED.visit_type;
    """

    with psycopg.connect(connection_url) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(statement, rows)
        connection.commit()

    return len(rows)


def run_pipeline(input_path: str | Path, connection_url: str) -> tuple[int, int]:
    """Extract, transform, and load records into PostgreSQL."""
    raw = extract(input_path)
    cleaned = transform(raw)
    loaded = load_to_postgres(cleaned, connection_url)
    return len(raw), loaded


def main() -> None:
    input_path = Path(os.getenv("INPUT_FILE", "data/sample_healthcare_data.csv"))
    extracted, loaded = run_pipeline(input_path, database_url())

    print(f"Records extracted: {extracted}")
    print(f"Records loaded to PostgreSQL: {loaded}")


if __name__ == "__main__":
    main()

# Healthcare Data Pipeline

A healthcare data engineering project built with Python, Pandas, PostgreSQL, SQL, and automated testing.

## Overview

I built this project to explore how raw healthcare data can be cleaned, validated, transformed, and loaded into a relational database through a repeatable ETL workflow.

The pipeline applies the same data-quality rules each time it runs and uses PostgreSQL constraints as an additional layer of protection after records reach the database.

## Pipeline

```text
Raw Healthcare Data
        |
        v
     Extract
        |
        v
Transform with Python and Pandas
        |
        v
     Validate
        |
        v
Load into PostgreSQL
        |
        v
   Query with SQL
```

## Key Features

- ETL workflow for healthcare visit records
- Data cleaning and standardization with Pandas
- Required-field validation
- Duplicate patient handling
- Age and value validation
- Direct PostgreSQL loading with Psycopg
- Upserts to make repeated loads predictable
- PostgreSQL constraints for database-level validation
- SQL analysis queries
- Pytest test suite with boundary and invalid-input cases
- GitHub Actions continuous integration
- Environment-based database configuration
- Synthetic sample data for safe demonstration

## Tech Stack

- Python 3.11+
- Pandas
- PostgreSQL
- Psycopg 3
- SQL
- Pytest
- GitHub Actions
- Git and GitHub

## Project Structure

```text
healthcare-data-pipeline/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   └── sample_healthcare_data.csv
├── src/
│   └── pipeline.py
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── tests/
│   └── test_pipeline.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## How It Works

1. **Extract:** Read visit records from a CSV source.
2. **Transform:** Validate required fields, standardize text, remove duplicate patient IDs, convert ages to numeric values, and reject invalid ages.
3. **Load:** Connect to PostgreSQL and upsert cleaned records into `healthcare_visits`.
4. **Analyze:** Use SQL queries to summarize the resulting dataset.

## Data Validation

The transformation layer checks that required columns are present and filters records that do not meet expected rules.

Age values must fall between 0 and 120, required values cannot be missing, patient IDs cannot be blank, and duplicate patient IDs are reduced to one record before loading.

The PostgreSQL schema independently enforces required fields and the valid age range.

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```text
.venv\Scripts\activate
```

### 2. Install the project

```bash
pip install -e ".[test]"
```

### 3. Create the PostgreSQL database

```bash
createdb healthcare_pipeline
psql -d healthcare_pipeline -f sql/schema.sql
```

### 4. Configure the database connection

Use `.env.example` as a reference and set `DATABASE_URL` in your local environment. Do not commit a real password.

macOS/Linux example:

```bash
export DATABASE_URL="postgresql://postgres:your_password@localhost:5432/healthcare_pipeline"
```

### 5. Run the pipeline

```bash
python src/pipeline.py
```

Example output:

```text
Records extracted: 8
Records loaded to PostgreSQL: 8
```

### 6. Run the tests

```bash
pytest -q
```

GitHub Actions also runs the test suite automatically on pushes and pull requests to `main`.

## SQL Analysis

After loading the data, run the included queries with:

```bash
psql -d healthcare_pipeline -f sql/analysis_queries.sql
```

The examples include total record counts, visits grouped by department, and average age grouped by visit type.

## Why I Built It

I wanted to connect Python data processing with relational database design rather than treating them as separate skills.

Building the pipeline made me think about where data-quality rules should live. Some rules are useful during transformation because bad records can be handled before loading, while database constraints provide another safeguard once the data is stored.

I also wanted the pipeline to be safe to run repeatedly. PostgreSQL upserts allow existing patient records to be updated rather than causing duplicate-key failures during another run.

## Testing

The test suite covers transformation behavior including:

- Duplicate patient IDs
- Missing required values
- Missing required columns
- Invalid ages
- Boundary ages of 0 and 120
- Non-numeric ages
- Text standardization
- Empty datasets

## Next Steps

- Track rejected records and rejection reasons
- Add structured pipeline logging
- Add automated data-quality reports
- Add integration tests against PostgreSQL
- Add pipeline performance metrics
- Containerize the application with Docker
- Build a simple analytics dashboard

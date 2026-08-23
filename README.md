# Healthcare Data Pipeline

A healthcare data engineering project built with Python, Pandas, PostgreSQL, and SQL.

## Overview

I built this project to explore how raw healthcare data can be cleaned, validated, transformed, and prepared for reliable storage in a relational database.

The pipeline is designed around a repeatable ETL workflow so that data-processing rules can be applied consistently instead of relying on manual cleanup.

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

- ETL workflow for healthcare records
- Data cleaning and standardization with Pandas
- Required-field validation
- Duplicate record handling
- Age and value validation
- PostgreSQL schema with database constraints
- SQL queries for basic analysis
- Automated tests for transformation logic
- Synthetic sample data for safe demonstration

## Tech Stack

- Python
- Pandas
- PostgreSQL
- SQL
- Pytest
- Git and GitHub

## Project Structure

```text
healthcare-data-pipeline/
├── data/
│   └── sample_healthcare_data.csv
├── src/
│   └── pipeline.py
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── tests/
│   └── test_pipeline.py
├── requirements.txt
├── .gitignore
└── README.md
```

## How It Works

The pipeline follows three main stages:

1. **Extract** records from a CSV source.
2. **Transform** the data by validating required fields, standardizing values, removing duplicate patient IDs, and filtering invalid records.
3. **Load** the cleaned data into PostgreSQL so it can be stored and queried consistently.

## Data Validation

The transformation layer checks that required columns are present and removes records that cannot meet the expected data rules.

For example, age values must fall between 0 and 120, required fields cannot be missing, and duplicate patient IDs are removed before the processed dataset is produced.

The PostgreSQL schema adds another layer of protection by enforcing its own constraints after the data reaches the database.

## Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the pipeline

```bash
python src/pipeline.py
```

The processed dataset is written to:

```text
data/processed_healthcare_data.csv
```

### 3. Run the tests

```bash
pytest
```

### 4. Prepare PostgreSQL

Create a PostgreSQL database and run:

```bash
psql -d healthcare_pipeline -f sql/schema.sql
```

The queries in `sql/analysis_queries.sql` can then be used as starting points for exploring the processed data.

## Why I Built It

I wanted to build something that connected Python data processing with relational database design rather than treating them as separate skills.

The project gave me a practical way to think about what should happen to data before it enters a database, which rules belong in the transformation layer, and which rules should also be enforced by the database itself.

It also reinforced an important part of data engineering: a pipeline should be repeatable. The same validation and transformation rules should be applied consistently every time new data moves through the system.

## Next Steps

- Add direct PostgreSQL loading from Python
- Add detailed pipeline logging
- Track rejected records and rejection reasons
- Add automated data-quality reports
- Add pipeline performance metrics
- Containerize the application with Docker
- Add GitHub Actions for automated testing
- Build a simple analytics dashboard

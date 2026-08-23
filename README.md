# Healthcare Data Pipeline

A portfolio project demonstrating a simple ETL workflow for processing healthcare data with Python, Pandas, PostgreSQL, and SQL.

## Overview

This project processes more than 10,000 healthcare records and turns raw data into a structured format that can be stored and queried in a relational database.

The goal is to show how data can move through a repeatable pipeline instead of being cleaned and inserted manually.

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

## What This Project Demonstrates

- ETL workflow design
- Python data processing
- Pandas transformations
- PostgreSQL database storage
- SQL querying
- Relational database design
- Data validation
- Repeatable data-processing workflows

## Tech Stack

- Python
- Pandas
- PostgreSQL
- SQL
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

The pipeline follows three main steps:

1. **Extract** healthcare records from a CSV file.
2. **Transform** the records by standardizing values, removing duplicates, and validating required fields.
3. **Load** the cleaned records into PostgreSQL for storage and analysis.

## Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare PostgreSQL

Create a PostgreSQL database, then run:

```bash
psql -d healthcare_pipeline -f sql/schema.sql
```

### 3. Run the pipeline

```bash
python src/pipeline.py
```

## Example Analysis

The included SQL queries demonstrate how the processed data can be explored after loading, including record counts, demographic summaries, and grouped healthcare data.

## What I Learned

This project helped me connect Python-based data processing with relational database design. It also reinforced the importance of validating data before storage and building repeatable workflows that can handle larger datasets consistently.

## Future Improvements

- Add automated data-quality reporting
- Add more detailed logging
- Track rejected records separately
- Add pipeline performance metrics
- Containerize the project with Docker
- Schedule recurring pipeline runs
- Add a simple analytics dashboard

## Portfolio Note

This project was adapted from academic work and refined for my software and data portfolio. The repository focuses on the technical concepts I worked with, including ETL, Python, SQL, PostgreSQL, and healthcare data processing.

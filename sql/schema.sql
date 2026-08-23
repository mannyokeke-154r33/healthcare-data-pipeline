CREATE TABLE IF NOT EXISTS healthcare_visits (
    patient_id VARCHAR(50) PRIMARY KEY,
    age INTEGER NOT NULL CHECK (age BETWEEN 0 AND 120),
    department VARCHAR(100) NOT NULL,
    visit_type VARCHAR(100) NOT NULL
);

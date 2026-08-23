-- Total processed records
SELECT COUNT(*) AS total_records
FROM healthcare_visits;

-- Records by department
SELECT department, COUNT(*) AS visit_count
FROM healthcare_visits
GROUP BY department
ORDER BY visit_count DESC;

-- Average age by visit type
SELECT visit_type, ROUND(AVG(age), 1) AS average_age
FROM healthcare_visits
GROUP BY visit_type
ORDER BY visit_type;

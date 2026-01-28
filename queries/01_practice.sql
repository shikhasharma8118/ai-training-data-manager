-- ================================================
-- Practice Queries
-- ================================================

-- Q1: View all datasets
SELECT * FROM datasets ORDER BY quality_score DESC;

-- Q2: Count by category
SELECT category, COUNT(*) as total
FROM datasets
GROUP BY category
ORDER BY total DESC;

-- Q3: High quality datasets (8+)
SELECT source, category, quality_score
FROM datasets
WHERE quality_score >= 8
ORDER BY quality_score DESC;

-- Q4: Average quality score
SELECT 
    ROUND(AVG(quality_score), 2) as avg_quality,
    MIN(quality_score) as min_quality,
    MAX(quality_score) as max_quality
FROM datasets;

-- Q5: Search for "data" in content
SELECT source, category
FROM datasets
WHERE content LIKE '%data%';
-- ================================================
-- Analytics Dashboard - Complex Queries
-- ================================================

-- Q1: Datasets with all their tags (JOIN)
SELECT 
    d.id,
    d.source,
    d.category,
    d.quality_score,
    STRING_AGG(t.name, ', ') as tags
FROM datasets d
LEFT JOIN dataset_tags dt ON d.id = dt.dataset_id
LEFT JOIN tags t ON dt.tag_id = t.id
GROUP BY d.id, d.source, d.category, d.quality_score
ORDER BY d.quality_score DESC;

-- Q2: Most popular tags
SELECT 
    t.name,
    COUNT(dt.dataset_id) as dataset_count,
    ROUND(AVG(d.quality_score), 2) as avg_quality
FROM tags t
LEFT JOIN dataset_tags dt ON t.id = dt.tag_id
LEFT JOIN datasets d ON dt.dataset_id = d.id
GROUP BY t.name
ORDER BY dataset_count DESC;

-- Q3: Quality distribution by category
SELECT 
    category,
    COUNT(*) as total_datasets,
    ROUND(AVG(quality_score), 2) as avg_quality,
    MIN(quality_score) as min_quality,
    MAX(quality_score) as max_quality
FROM datasets
GROUP BY category
ORDER BY avg_quality DESC;

-- Q4: Datasets with preprocessing history
SELECT 
    d.source,
    d.category,
    COUNT(ph.id) as preprocessing_steps,
    STRING_AGG(ph.operation, ' → ') as pipeline
FROM datasets d
INNER JOIN preprocessing_history ph ON d.id = ph.dataset_id
GROUP BY d.id, d.source, d.category
ORDER BY preprocessing_steps DESC;

-- Q5: Find datasets by multiple tags (using subquery)
SELECT 
    d.source,
    d.category,
    d.quality_score
FROM datasets d
WHERE d.id IN (
    SELECT dt.dataset_id
    FROM dataset_tags dt
    INNER JOIN tags t ON dt.tag_id = t.id
    WHERE t.name IN ('machine-learning', 'beginner-friendly')
    GROUP BY dt.dataset_id
    HAVING COUNT(DISTINCT t.name) = 2
);

-- Q6: High-quality datasets with tags
SELECT 
    d.source,
    d.quality_score,
    d.word_count,
    STRING_AGG(t.name, ', ') as tags
FROM datasets d
LEFT JOIN dataset_tags dt ON d.id = dt.dataset_id
LEFT JOIN tags t ON dt.tag_id = t.id
WHERE d.quality_score >= 9
GROUP BY d.id, d.source, d.quality_score, d.word_count
ORDER BY d.quality_score DESC;

-- Q7: Category statistics with tag counts
SELECT 
    d.category,
    COUNT(DISTINCT d.id) as dataset_count,
    COUNT(DISTINCT dt.tag_id) as unique_tags,
    ROUND(AVG(d.quality_score), 2) as avg_quality
FROM datasets d
LEFT JOIN dataset_tags dt ON d.id = dt.dataset_id
GROUP BY d.category
ORDER BY dataset_count DESC;
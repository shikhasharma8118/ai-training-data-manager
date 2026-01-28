-- ================================================
-- Complete Sample Data - All Tables
-- ================================================

-- Insert 20 datasets
INSERT INTO datasets (content, source, category, quality_score, word_count) VALUES
('Machine learning is a subset of artificial intelligence that focuses on algorithms enabling computers to learn from data.', 'Wikipedia', 'AI/ML', 9, 20),
('Deep learning neural networks with multiple layers can automatically learn hierarchical representations of data.', 'Research Paper', 'AI/ML', 10, 16),
('Natural language processing enables computers to understand, interpret and generate human language.', 'Academic Journal', 'AI/ML', 9, 14),
('Reinforcement learning agents learn optimal behavior through trial and error interactions with their environment.', 'Textbook', 'AI/ML', 8, 16),
('Computer vision algorithms process digital images and videos to extract meaningful information.', 'Tech Conference', 'AI/ML', 8, 14),
('Python is a high-level interpreted programming language emphasizing code readability.', 'Python Docs', 'Programming', 9, 11),
('JavaScript is the dominant client-side scripting language for web development.', 'MDN Web Docs', 'Programming', 8, 12),
('SQL structured query language provides standardized syntax for managing relational databases.', 'Database Tutorial', 'Programming', 7, 12),
('Git distributed version control system tracks source code changes enabling collaborative development.', 'Git Documentation', 'Programming', 8, 13),
('PostgreSQL is an advanced open-source relational database featuring ACID compliance.', 'PostgreSQL Docs', 'Database', 9, 11),
('Database normalization organizes data into related tables reducing redundancy.', 'Database Textbook', 'Database', 8, 10),
('Indexing data structures optimize database query performance by providing fast lookup paths.', 'Tech Article', 'Database', 7, 13),
('Data preprocessing transforms raw data into clean structured formats.', 'Data Science Guide', 'Data Science', 8, 11),
('Feature engineering creates informative input variables from raw data using domain knowledge.', 'ML Handbook', 'Data Science', 9, 13),
('Cross-validation evaluates machine learning models by partitioning data into training and testing subsets.', 'Statistics Guide', 'Data Science', 8, 15),
('Exploratory data analysis uses statistical graphics to discover patterns and test hypotheses.', 'Analytics Book', 'Data Science', 7, 13),
('React is a JavaScript library for building component-based user interfaces.', 'React Docs', 'Web Development', 9, 11),
('RESTful APIs use HTTP methods and stateless architecture to enable scalable web services.', 'API Guide', 'Web Development', 8, 14),
('Docker containerization packages applications with dependencies into isolated portable units.', 'Docker Docs', 'DevOps', 9, 11),
('Kubernetes orchestrates containerized applications automating deployment, scaling and management.', 'K8s Documentation', 'DevOps', 8, 10);

-- Insert tags
INSERT INTO tags (name, description) VALUES
('machine-learning', 'Machine learning and ML algorithms'),
('deep-learning', 'Neural networks and deep learning'),
('nlp', 'Natural language processing'),
('computer-vision', 'Image and video processing'),
('python', 'Python programming'),
('javascript', 'JavaScript programming'),
('sql', 'SQL and databases'),
('data-preprocessing', 'Data cleaning and preparation'),
('web-dev', 'Web development'),
('devops', 'DevOps and infrastructure'),
('beginner-friendly', 'Good for beginners'),
('advanced', 'Advanced content'),
('tutorial', 'Tutorial content'),
('reference', 'Reference documentation');

-- Link datasets to tags (many-to-many)
INSERT INTO dataset_tags (dataset_id, tag_id) VALUES
-- AI/ML datasets
(1, 1), (1, 11),
(2, 1), (2, 2), (2, 12),
(3, 1), (3, 3),
(4, 1), (4, 12),
(5, 4), (5, 1),
-- Programming
(6, 5), (6, 11),
(7, 6), (7, 9),
(8, 7),
(9, 10),
-- Database
(10, 7), (10, 14),
(11, 7), (11, 12),
(12, 7),
-- Data Science
(13, 8), (13, 11),
(14, 1), (14, 8),
(15, 1),
(16, 8),
-- Web Dev
(17, 6), (17, 9),
(18, 9), (18, 14),
-- DevOps
(19, 10),
(20, 10);

-- Add preprocessing history
INSERT INTO preprocessing_history (dataset_id, operation, details) VALUES
(1, 'cleaned', 'Removed special characters'),
(1, 'tokenized', 'Split into words'),
(1, 'normalized', 'Converted to lowercase'),
(2, 'cleaned', 'Removed HTML tags'),
(2, 'spell_checked', 'Corrected spelling errors'),
(6, 'cleaned', 'Standardized formatting'),
(13, 'deduplicated', 'Removed duplicates'),
(13, 'cleaned', 'Fixed punctuation');

-- Verify data
SELECT 'Datasets:', COUNT(*) FROM datasets;
SELECT 'Tags:', COUNT(*) FROM tags;
SELECT 'Dataset-Tag links:', COUNT(*) FROM dataset_tags;
SELECT 'Preprocessing records:', COUNT(*) FROM preprocessing_history;
```

---

## **STEP 4: Execute EVERYTHING in Supabase**

**In Supabase SQL Editor:**

1. **Copy ALL of `complete_schema.sql`** → Paste → Run
2. **Copy ALL of `complete_data.sql`** → Paste → Run

**Expected output:**
```
All tables created successfully!
Datasets: 20
Tags: 14
Dataset-Tag links: 28
Preprocessing records: 8
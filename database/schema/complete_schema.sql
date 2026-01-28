-- ================================================
-- AI Training Data Manager - Complete Database Schema
-- ================================================
-- All tables with relationships
-- ================================================

-- TABLE 1: Main datasets table
CREATE TABLE datasets (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    source VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quality_score INTEGER CHECK (quality_score BETWEEN 1 AND 10),
    word_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLE 2: Tags
CREATE TABLE tags (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLE 3: Dataset-Tags junction (many-to-many)
CREATE TABLE dataset_tags (
    id BIGSERIAL PRIMARY KEY,
    dataset_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign keys
    CONSTRAINT fk_dataset FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
    CONSTRAINT fk_tag FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    
    -- Prevent duplicates
    CONSTRAINT unique_dataset_tag UNIQUE (dataset_id, tag_id)
);

-- TABLE 4: Preprocessing history (one-to-many)
CREATE TABLE preprocessing_history (
    id BIGSERIAL PRIMARY KEY,
    dataset_id BIGINT NOT NULL,
    operation VARCHAR(100) NOT NULL,
    details TEXT,
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key
    CONSTRAINT fk_preprocessing_dataset FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_datasets_category ON datasets(category);
CREATE INDEX idx_datasets_quality ON datasets(quality_score);
CREATE INDEX idx_datasets_source ON datasets(source);
CREATE INDEX idx_dataset_tags_dataset ON dataset_tags(dataset_id);
CREATE INDEX idx_dataset_tags_tag ON dataset_tags(tag_id);
CREATE INDEX idx_preprocessing_dataset ON preprocessing_history(dataset_id);

-- Success message
SELECT 'All tables created successfully!' as message;
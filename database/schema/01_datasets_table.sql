-- ================================================
-- AI Training Data Manager - Main Datasets Table
-- ================================================
-- Purpose: Store text-based AI training datasets
-- Author: Shikha
-- Date: 2026-01-28
-- ================================================

-- Create main datasets table
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

-- Add indexes for performance
CREATE INDEX idx_datasets_category ON datasets(category);
CREATE INDEX idx_datasets_quality ON datasets(quality_score);
CREATE INDEX idx_datasets_source ON datasets(source);

-- Add table documentation
COMMENT ON TABLE datasets IS 'Main table for AI training text datasets with metadata';



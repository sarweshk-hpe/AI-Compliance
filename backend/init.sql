-- Actum AI Compliance Engine Database Initialization
-- This script creates the initial database structure

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

Create tables (these will be created by SQLAlchemy, but this provides a reference)
-- The actual table creation is handled by the Python application using SQLAlchemy models

-- Note: Tables are created automatically by SQLAlchemy when the application starts
-- This file serves as documentation and can be used for manual database operations if needed

-- Example: Create a test user for development
INSERT INTO users (username, email, hashed_password, is_active, is_admin) 
VALUES ('admin', 'admin@actum.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK8i', true, true)
ON CONFLICT (username) DO NOTHING;

-- Example: Create a test policy pack
INSERT INTO policy_packs (name, version, description, is_active) 
VALUES ('EU AI Act Compliance Pack', 'pack-2025-01-01-v1', 'Default policy pack for EU AI Act compliance', true)
ON CONFLICT (version) DO NOTHING;

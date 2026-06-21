CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS chunks;
CREATE TABLE chunks (
  id bigint generated always as identity primary key,
  source text, 
  content text, 
  embedding vector(512), 
  created_at timestamptz default now()
);
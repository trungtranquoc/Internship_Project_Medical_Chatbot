-- 1. Clear Existing Tables (Use with caution in production)
DROP TABLE IF EXISTS feedbacks CASCADE;
DROP TABLE IF EXISTS elements CASCADE;
DROP TABLE IF EXISTS steps CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. Create Users Table
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    identifier TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    metadata TEXT NOT NULL,
    "createdAt" TEXT NOT NULL
);

-- 3. Create Threads Table
CREATE TABLE threads (
    id TEXT PRIMARY KEY,
    "createdAt" TEXT NOT NULL DEFAULT to_char(timezone('utc', now()), 'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"'),
    "name" TEXT,
    "userId" TEXT,
    "userIdentifier" TEXT,
    "tags" TEXT,
    metadata TEXT
);

-- 4. Create Steps Table
CREATE TABLE steps (
    id TEXT PRIMARY KEY,
    "threadId" TEXT NOT NULL,
    "parentId" TEXT,
    "name" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "streaming" BOOLEAN,
    "waitForAnswer" BOOLEAN,
    "isError" BOOLEAN,
    "metadata" TEXT,
    "tags" TEXT,
    "input" TEXT,
    "output" TEXT,
    "createdAt" TEXT NOT NULL,
    "start" TEXT,
    "end" TEXT,
    "generation" TEXT,
    "showInput" TEXT,
    "language" TEXT,
    "defaultOpen" BOOLEAN
);

-- 5. Create Elements Table
CREATE TABLE elements (
    id TEXT PRIMARY KEY,
    "threadId" TEXT,
    "type" TEXT,
    "chainlitKey" TEXT,
    "url" TEXT,
    "objectKey" TEXT,
    "name" TEXT NOT NULL,
    "display" TEXT,
    "size" TEXT,
    "language" TEXT,
    "page" INT,
    "forId" TEXT,
    "mime" TEXT,
    "props" TEXT
);

-- 6. Create Feedbacks Table
CREATE TABLE feedbacks (
    id TEXT PRIMARY KEY,
    "forId" TEXT NOT NULL,
    "value" INT NOT NULL,
    "comment" TEXT
);

-- 7. Insert Initial Admin User
INSERT INTO users (id, identifier, password, metadata, "createdAt") 
VALUES ('1', 'admin', 'admin123', '{}', '2026-03-31T09:00:00Z')
ON CONFLICT (identifier) DO NOTHING;





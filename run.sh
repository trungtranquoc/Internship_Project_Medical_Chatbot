# 1. Clear Existing Tables
"DROP TABLE IF EXISTS feedbacks CASCADE; DROP TABLE IF EXISTS elements CASCADE; DROP TABLE IF EXISTS steps CASCADE; DROP TABLE IF EXISTS threads CASCADE; DROP TABLE IF EXISTS users CASCADE;" | kubectl exec -i postgres-95c6b88c8-vhwkk -- psql -U CHAINLIT_DB -d MEDICAL_CHAT_HISTORY

# 2. Create Users Table
"CREATE TABLE users (id TEXT PRIMARY KEY, identifier TEXT UNIQUE NOT NULL, password TEXT NOT NULL, metadata TEXT NOT NULL, ""createdAt"" TEXT NOT NULL);" | kubectl exec -i postgres-95c6b88c8-vhwkk -- psql -U CHAINLIT_DB -d MEDICAL_CHAT_HISTORY

# 3. Create Threads Table
"CREATE TABLE threads (id TEXT PRIMARY KEY, ""createdAt"" TEXT NOT NULL, ""name"" TEXT, ""userId"" TEXT, ""userIdentifier"" TEXT, ""tags"" TEXT, metadata TEXT);" | kubectl exec -i postgres-95c6b88c8-vhwkk -- psql -U CHAINLIT_DB -d MEDICAL_CHAT_HISTORY

# 4. Create Steps Table
"CREATE TABLE steps (id TEXT PRIMARY KEY, ""threadId"" TEXT NOT NULL, ""parentId"" TEXT, ""name"" TEXT NOT NULL, ""type"" TEXT NOT NULL, ""streaming"" BOOLEAN, ""waitForAnswer"" BOOLEAN, ""isError"" BOOLEAN, ""metadata"" TEXT, ""tags"" TEXT, ""input"" TEXT, ""output"" TEXT, ""createdAt"" TEXT NOT NULL, ""start"" TEXT, ""end"" TEXT, ""generation"" TEXT, ""showInput"" TEXT, ""language"" TEXT, ""defaultOpen"" BOOLEAN);" | kubectl exec -i postgres-95c6b88c8-vhwkk -- psql -U CHAINLIT_DB -d MEDICAL_CHAT_HISTORY


# 5. Create Elements Table
"CREATE TABLE elements (id TEXT PRIMARY KEY, ""threadId"" TEXT, ""type"" TEXT, ""chainlitKey"" TEXT, ""url"" TEXT, ""objectKey"" TEXT, ""name"" TEXT NOT NULL, ""display"" TEXT, ""size"" TEXT, ""language"" TEXT, ""page"" INT, ""forId"" TEXT, ""mime"" TEXT, ""props"" TEXT);" | kubectl exec -i postgres-95c6b88c8-vhwkk -- psql -U CHAINLIT_DB -d MEDICAL_CHAT_HISTORY

# 6. Create Feedbacks Table
"CREATE TABLE feedbacks (id TEXT PRIMARY KEY, ""forId"" TEXT NOT NULL, ""value"" INT NOT NULL, ""comment"" TEXT);" | kubectl exec -i postgres-95c6b88c8-vhwkk -- psql -U CHAINLIT_DB -d MEDICAL_CHAT_HISTORY

# 7. Insert Initial Admin User
"INSERT INTO users (id, identifier, password, metadata, ""createdAt"") VALUES ('1', 'admin', 'admin123', '{}', '2026-03-31T09:00:00Z');" | kubectl exec -i postgres-95c6b88c8-vhwkk -- psql -U CHAINLIT_DB -d MEDICAL_CHAT_HISTORY
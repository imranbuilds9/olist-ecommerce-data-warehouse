-- checking current database name and the currently existing schema names
SELECT
    current_database() AS connected_database,
    schema_name
FROM information_schema.schemata
WHERE schema_name NOT IN (
    'pg_catalog',
    'information_schema'
)
ORDER BY schema_name;

-- creating raw schema
CREATE SCHEMA raw;

-- creating staging schema
CREATE SCHEMA staging;

-- creating warehouse schema
CREATE SCHEMA warehouse;

-- inspecting schema names
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name IN ('raw', 'staging', 'warehouse')
ORDER BY schema_name;

-- inspecting database encoding , to see if it matches the .csv file encoding
SELECT
    current_database() AS database_name,
    pg_encoding_to_char(encoding) AS database_encoding
FROM pg_database
WHERE datname = current_database();

-- Verifying the default schema search path and database collation settings.
SELECT
    name,
    setting
FROM pg_settings
WHERE name IN (
    'search_path',
    'client_encoding',
    'server_encoding'
)
ORDER BY name;

-- Inspecting the locale settings used by PostgreSQL for sorting and character classification.
SELECT
    datname AS database_name,
    datcollate AS collation,
    datctype AS character_classification
FROM pg_database
WHERE datname = current_database();

-- Verifying who owns olist_dw and whether current PostgreSQL user has the necessary permissions.
SELECT
    d.datname AS database_name,
    pg_get_userbyid(d.datdba) AS database_owner,
    has_database_privilege(current_user, d.datname,'CONNECT') AS can_connect,
    has_database_privilege(current_user, d.datname,'CREATE' ) AS can_create
FROM pg_database d
WHERE d.datname = current_database();

-- Checking whether three project schemas
--   are owned by postgres and whether current user can create objects inside them.
SELECT
    schema_name,
    schema_owner,
    has_schema_privilege( current_user, schema_name, 'USAGE' ) AS can_use,
    has_schema_privilege( current_user, schema_name, 'CREATE') AS can_create
FROM information_schema.schemata
WHERE schema_name IN ('raw', 'staging', 'warehouse')
ORDER BY schema_name;

-- postgre Extensions
SELECT
    name,
    default_version,
    installed_version,
    comment
FROM pg_available_extensions
ORDER BY name;

SELECT
    name,
    setting
FROM pg_settings
WHERE name IN (
    'default_tablespace',
    'default_table_access_method',
    'default_toast_compression'
)
ORDER BY name;

SELECT
    schemaname,
    tablename,
    tableowner
FROM pg_tables
WHERE schemaname IN ('raw', 'staging', 'warehouse')
ORDER BY schemaname, tablename;

-- database size before ingestion
SELECT
    current_database() AS database_name,
    pg_size_pretty(
        pg_database_size(current_database())
    ) AS database_size;

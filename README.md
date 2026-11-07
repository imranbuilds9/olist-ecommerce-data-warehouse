# Olist E-Commerce — Enterprise Data Warehouse & ELT Pipeline

An enterprise-style data engineering portfolio project built using the **Olist Brazilian E-Commerce Public Dataset**. The project focuses on data profiling, quality investigation, PostgreSQL raw-layer ingestion, validation, and the development of a reproducible ELT pipeline.

**Project Status:** In Progress — Raw ingestion and validation completed.

## 1. Project Overview

This project aims to build a reliable, analytics-ready data warehouse using real-world Brazilian e-commerce data.

The pipeline is being developed with an emphasis on practical data engineering principles:

- Source data profiling and quality assessment
- Relational database design
- Raw data ingestion and preservation
- Data validation and integrity checks
- Batch identification and ingestion audit metadata
- Transactional processing and failure handling
- Reproducibility and documentation

The architecture follows a layered approach:

```text
Olist CSV Source Data
        |
        v
Python Data Profiling
        |
        v
PostgreSQL — Raw Layer
        |
        v
Staging Layer (Planned)
        |
        v
Data Warehouse (Planned)
        |
        v
Analytics and Reporting (Planned)
```

## 2. Dataset

**Dataset:** Olist Brazilian E-Commerce Public Dataset

**Source:** [Kaggle — Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**License:** CC BY-NC-SA 4.0

The dataset contains Brazilian e-commerce transaction information covering customers, orders, products, sellers, payments, reviews, and geolocation.

It consists of nine CSV source files:

| Source file | Description |
|---|---|
| `olist_customers_dataset.csv` | Customer information |
| `olist_geolocation_dataset.csv` | ZIP-code geolocation information |
| `olist_orders_dataset.csv` | Order details and timestamps |
| `olist_order_items_dataset.csv` | Products included in orders |
| `olist_order_payments_dataset.csv` | Payment information |
| `olist_order_reviews_dataset.csv` | Customer reviews |
| `olist_products_dataset.csv` | Product attributes |
| `olist_sellers_dataset.csv` | Seller information |
| `product_category_name_translation.csv` | Product category translations |

**Important:** The original CSV files are excluded from this repository. Download the dataset from Kaggle and place the nine CSV files inside `data/raw/`.

## 3. Technology Stack

| Technology | Purpose | Status |
|---|---|---|
| Python 3.11 | Data profiling and ingestion | Implemented |
| Psycopg 3.3.7 | Python–PostgreSQL connectivity | Implemented |
| PostgreSQL 18.6 | Raw data storage and SQL validation | Implemented |
| SQL | Database design, validation and investigation | Implemented |
| Git and GitHub | Version control and documentation | In use |
| dbt | Data transformation and testing | Planned |
| Apache Airflow | Workflow orchestration | Planned |
| Docker | Environment and service management | Planned |
| Power BI | Analytics and visualization | Planned |
| Azure / Microsoft Fabric | Future cloud implementation | Planned |

## 4. Repository Structure

```text
olist-ecommerce-data-warehouse/
│
├── data/
│   ├── raw/                       # Local Olist source CSV files (not committed)
│   └── processed/                 # Local processed data (not committed)
│
├── python/
│   ├── 1–61                       # Data profiling and investigation scripts
│   └── 62.load_raw_data.py        # PostgreSQL raw data ingestion
│
├── sql/
│   ├── 01_environment_and_schema_setup.sql
│   ├── 02_create_raw_tables.sql
│   ├── 03_validate_raw_ingestion.sql
│   └── 04_investigate_raw_data_quality.sql
│
├── dbt/                           # Reserved for future dbt development
├── docs/                          # Reserved for future documentation
├── tests/                         # Reserved for future automated tests
│
├── requirements.txt
├── .gitignore
└── README.md
```

**Note:** The `dbt`, `docs`, and `tests` directories are currently empty placeholders for planned development.

## 5. Work Completed

### 5.1 Data Profiling and Investigation

Developed 61 Python scripts to investigate the source dataset and identify potential data quality issues.

Areas investigated include:

- Row counts and candidate key uniqueness
- Primary key and composite key validation
- Referential integrity
- Customer, seller and product relationships
- Order and order-item relationships
- Payment records and payment totals
- Order statuses and timestamp completeness
- Product attributes and category coverage
- Geolocation consistency and outliers
- Freight charges and unusual transaction values
- Seller activity and performance
- Review records and repeated review IDs

### 5.2 PostgreSQL Database Setup

Created the local PostgreSQL database `olist_dw` and established three schemas:

| Schema | Purpose |
|---|---|
| `raw` | Stores source data with original column values |
| `staging` | Reserved for data cleaning and standardization |
| `warehouse` | Reserved for analytical data models |

Created nine raw tables corresponding to the nine source CSV files.

The raw tables preserve source column names and store source values as TEXT. Additional ingestion metadata columns are included:

- `source_file`
- `ingested_at`
- `batch_id`

### 5.3 Raw Data Ingestion

Implemented `python/62.load_raw_data.py` using Python and Psycopg.

The ingestion process:

1. Validates source CSV files and their headers.
2. Generates a unique batch ID.
3. Records a UTC ingestion timestamp.
4. Removes the previous raw snapshot within a database transaction.
5. Loads the nine CSV files into their corresponding PostgreSQL tables.
6. Verifies the loaded row counts.
7. Commits the transaction only after successful validation.

The process uses a transactional full-refresh approach. If an error occurs during loading, the transaction is rolled back.

**Verified ingestion results:**

| Raw table | Rows loaded |
|---|---:|
| `raw.customers` | 99,441 |
| `raw.geolocation` | 1,000,163 |
| `raw.orders` | 99,441 |
| `raw.order_items` | 112,650 |
| `raw.order_payments` | 103,886 |
| `raw.order_reviews` | 99,224 |
| `raw.products` | 32,951 |
| `raw.sellers` | 3,095 |
| `raw.product_category_translation` | 71 |
| **Total** | **1,550,922** |

All nine tables were independently checked in PostgreSQL after ingestion.

### 5.4 Raw Data Validation and Quality Findings

The following checks were completed after ingestion:

- All nine raw tables contained the expected number of rows.
- All tables contained the expected source filename and ingestion metadata.
- All rows shared the same batch ID and ingestion timestamp.
- No missing ingestion metadata values were found.
- All 52 source columns across the nine raw tables were checked for SQL NULL values.
- All 27 ingestion metadata columns were checked for missing values.
- Empty strings were investigated separately from SQL NULL values.
- Missing product attributes and order timestamps were examined.

**Important findings:**

- The CSV ingestion preserved empty fields as empty strings rather than converting them to SQL NULL.
- Thirteen source columns contained empty-string values.
- 610 products had four descriptive attributes missing together.
- Two products had missing physical dimension attributes.
- Some delivered orders had missing timestamps.
- Missing timestamp patterns were also found among canceled and other non-delivered order statuses.

These findings are being retained as source-level data quality observations. They will inform the future staging transformations and data quality tests.

## 6. Running the Project

### Prerequisites

- Python 3.11 or compatible version
- PostgreSQL
- Git
- The Olist dataset downloaded from Kaggle

### Step 1 — Clone the repository

```powershell
git clone https://github.com/imranbuilds9/olist-ecommerce-data-warehouse.git

cd olist-ecommerce-data-warehouse
```

### Step 2 — Install Python dependencies

```powershell
pip install -r requirements.txt
```

### Step 3 — Prepare the source data

Download the dataset from Kaggle and place all nine CSV files inside:

```text
data/raw/
```

The raw dataset is intentionally excluded from Git.

### Step 4 — Prepare PostgreSQL

Create a PostgreSQL database named `olist_dw` and connect to it.

Execute the SQL scripts in this order:

1. `sql/01_environment_and_schema_setup.sql`
2. `sql/02_create_raw_tables.sql`

These are initial database setup scripts. Run them against a fresh project database; they are not designed as repeatable migrations.

### Step 5 — Run raw ingestion

From the project root:

```powershell
python .\python\62.load_raw_data.py
```

The script requests the PostgreSQL password interactively. The password is not stored in the script.

### Step 6 — Validate ingestion

Execute:

```text
sql/03_validate_raw_ingestion.sql
```

### Step 7 — Investigate data quality

Execute:

```text
sql/04_investigate_raw_data_quality.sql
```

The SQL investigation scripts contain queries for examining the ingested data and its quality characteristics.

## 7. Current Project Status

| Component | Status |
|---|---|
| Dataset acquisition and profiling | Completed |
| Python profiling scripts (1–61) | Completed |
| PostgreSQL database and schemas | Completed |
| Nine raw table definitions | Completed |
| Python raw ingestion | Implemented and verified |
| Ingestion metadata and row-count validation | Completed |
| Raw data quality investigations | Completed to date |
| Staging transformations | Pending |
| Warehouse dimensional modeling | Pending |
| dbt transformations and tests | Pending |
| Workflow orchestration | Pending |
| Analytics and reporting | Pending |
| Cloud deployment | Future stage |

## 8. Planned Development

1. Review and finalize outstanding source data quality decisions.
2. Define staging-layer data cleaning and standardization rules.
3. Implement staging transformations in PostgreSQL.
4. Design analytical warehouse models.
5. Introduce dbt for transformations and testing.
6. Develop incremental processing where appropriate.
7. Improve pipeline audit logging and failure handling.
8. Introduce orchestration and containerization.
9. Develop analytics and reporting.
10. Explore deployment using Azure or Microsoft Fabric.

## 9. Project Objective

The objective is to build a reproducible and well-documented data engineering project that demonstrates practical skills in Python, SQL, PostgreSQL, data quality engineering, ELT pipeline development, and analytical data modeling.

This repository is actively being developed. Completed components and future implementation stages are documented separately to maintain transparency about project progress.
\ No newline at end of file

# Olist E-Commerce — Enterprise Data Warehouse & ELT Pipeline

An end-to-end data engineering portfolio project built around the Olist Brazilian E-Commerce Public Dataset. The project aims to transform raw e-commerce data into a reliable, analytics-ready data warehouse through data ingestion, validation, transformation, and testing.

**Project Status:** In Progress

## Project Overview

This project explores the development of an enterprise-style data warehouse using real-world e-commerce data from Olist.

The objective is to build a structured and reliable data pipeline that handles raw data, investigates data quality issues, applies transformations, and produces analytics-ready datasets.

The project emphasizes practical data engineering principles, including:

- Data profiling and quality assessment
- Relational data modeling
- Data ingestion and transformation
- Incremental and idempotent processing
- Data validation and testing
- Audit metadata and pipeline reliability
- Documentation and reproducibility

## Dataset

**Dataset:** Olist Brazilian E-Commerce Public Dataset

**Source:** [Kaggle — Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**License:** CC BY-NC-SA 4.0

The dataset contains information about Brazilian e-commerce transactions, including customers, orders, products, sellers, payments, reviews, and geolocation.

The original dataset contains nine CSV files:

- Customers
- Geolocation
- Orders
- Order Items
- Order Payments
- Order Reviews
- Products
- Sellers
- Product Category Translation

Raw CSV files are excluded from this GitHub repository. Users must obtain the dataset from its original source and place the files in `data/raw/`.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data profiling, validation, and ingestion |
| SQL | Data analysis and database transformations |
| PostgreSQL | Planned data warehouse platform |
| dbt | Planned transformation and testing framework |
| Git and GitHub | Version control and project documentation |

Additional technologies may be introduced as the pipeline develops.

## Repository Structure

```text
olist-ecommerce-data-warehouse/
│
├── data/
│   ├── raw/              # Local source CSV files (not committed)
│   └── processed/        # Local processed data (not committed)
│
├── dbt/                  # Planned dbt project
├── docs/                 # Project documentation
├── python/               # Python profiling and validation scripts
├── sql/                  # SQL scripts and transformations
├── tests/                # Data quality and pipeline tests
│
├── .gitignore
└── README.md
```

## Work Completed So Far

### Data Profiling and Quality Investigation

Initial work has focused on understanding the dataset and identifying potential data quality issues.

Completed investigations include:

- Order and order-item relationships
- Primary key and composite key validation
- Foreign key and referential integrity checks
- Payment records and payment totals
- Order status and timestamp validation
- Product attributes and category coverage
- Seller activity and performance
- Customer and geolocation analysis
- Review records and repeated review IDs
- Freight price ratios and unusual transaction values

The project currently contains Python scripts for these profiling and validation activities.

### Example Validation Results

| Validation | Result |
|---|---:|
| Order-item records checked | 112,650 |
| Duplicate order-item composite keys | 0 |
| Missing order references | 0 |
| Missing product references | 0 |
| Missing seller references | 0 |

Repeated review IDs were also investigated. Some review IDs are associated with multiple orders, so they require careful treatment during warehouse modeling rather than being automatically classified as duplicate records.

## Running the Python Scripts

After downloading the dataset and placing the CSV files inside `data/raw/`, run scripts from the project root.

Example using PowerShell:

```powershell
python .\python\check_order_item_keys.py
```

Another example:

```powershell
python .\python\check_order_item_references.py
```

The scripts currently use Python's standard library for these profiling and validation tasks.

## Planned Development

The next development stages include:

1. Complete dataset profiling and data quality investigations.
2. Finalize source-to-target data requirements.
3. Design the warehouse architecture and database schemas.
4. Build raw and staging layers in PostgreSQL.
5. Develop Python-based ingestion processes.
6. Implement transformations and tests using dbt.
7. Introduce incremental processing and idempotency.
8. Add pipeline audit metadata and failure handling.
9. Document the architecture and execution workflow.
10. Explore cloud deployment and analytics integration.

## Project Goals

The final objective is to demonstrate practical data engineering skills through a reproducible, documented, and testable data warehouse and ELT pipeline.

This repository is a work in progress. Features and implementation details will be updated as development continues.

# Script: profile_key_uniqueness.ps1
# Purpose: Profile uniqueness of selected key columns in Olist CSV files.


if (-not (Test-Path -LiteralPath $rawDataPath)) {
    Write-Error "Raw data directory not found: $rawDataPath"
    exit 1
}

$checks = @(
    @{ File = "olist_orders_dataset.csv"; Column = "order_id" },
    @{ File = "olist_customers_dataset.csv"; Column = "customer_id" },
    @{ File = "olist_customers_dataset.csv"; Column = "customer_unique_id" },
    @{ File = "olist_products_dataset.csv"; Column = "product_id" },
    @{ File = "olist_sellers_dataset.csv"; Column = "seller_id" },
    @{ File = "olist_order_reviews_dataset.csv"; Column = "review_id" }
)

$results = foreach ($check in $checks) {

    $path = Join-Path $rawDataPath $check.File

    if (-not (Test-Path -LiteralPath $path)) {
        Write-Warning "File not found: $($check.File)"
        continue
    }

    $values = Import-Csv -LiteralPath $path |
        ForEach-Object {
            $_.PSObject.Properties[$check.Column].Value
        }

    $allValues = @($values)

    # Separate missing values from valid key values.
    $validValues = @(
        $allValues | Where-Object {
            -not [string]::IsNullOrWhiteSpace($_)
        }
    )

    $totalRows = $allValues.Count
    $missingValues = $totalRows - $validValues.Count
    $distinctValues = @(
        $validValues | Sort-Object -Unique
    ).Count

    $duplicateOccurrences = $validValues.Count - $distinctValues

    [PSCustomObject]@{
        File                  = $check.File
        Column                = $check.Column
        TotalRows             = $totalRows
        MissingValues         = $missingValues
        DistinctValues        = $distinctValues
        DuplicateOccurrences  = $duplicateOccurrences
    }
}

$results | Format-Table -AutoSize

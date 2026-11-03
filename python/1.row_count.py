
$projectRoot = $PSScriptRoot
$rawDataPath = Join-Path $projectRoot "data\raw"

if (-not (Test-Path -LiteralPath $rawDataPath)) {
    Write-Error "Raw data directory not found: $rawDataPath"
    exit 1
}

$results = foreach ($file in Get-ChildItem -LiteralPath $rawDataPath -Filter "*.csv" -File | Sort-Object Name) {
    Write-Host "Counting rows in $($file.Name) ..."

    $count = Import-Csv -LiteralPath $file.FullName |
        Measure-Object |
        Select-Object -ExpandProperty Count

    [PSCustomObject]@{
        File     = $file.Name
        DataRows = $count
    }
}

$results | Format-Table -AutoSize

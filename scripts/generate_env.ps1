Param(
    [string]$Source = "../.env.example",
    [string]$Target = "../.env"
)

Copy-Item -Path $Source -Destination $Target -Force
Write-Host "Copied $Source to $Target"

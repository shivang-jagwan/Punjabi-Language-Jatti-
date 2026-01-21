# Jatti Setup - Add to PowerShell Profile
# Run this ONCE to enable 'jatti' command globally

# Find PowerShell Profile location
$profilePath = $PROFILE
Write-Host "PowerShell Profile: $profilePath" -ForegroundColor Green

# Create profile directory if it doesn't exist
$profileDir = Split-Path $profilePath
if (!(Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

# Add jatti function to profile
$jattiFunction = @'

# Jatti Language Command
$jattiPath = "c:\Users\Mr.Singh\Desktop\jatti-lang - Copy"
function jatti {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments)
    
    # Convert relative file paths to absolute from CURRENT directory
    $processedArgs = @()
    for ($i = 0; $i -lt $Arguments.Count; $i++) {
        if ($i -eq 0) {
            $processedArgs += $Arguments[$i]
        }
        elseif ($i -eq 1 -and $Arguments[0] -in @("run", "build", "format")) {
            $filePath = $Arguments[$i]
            if (-not [System.IO.Path]::IsPathRooted($filePath)) {
                $filePath = Join-Path (Get-Location) $filePath
            }
            $processedArgs += $filePath
        }
        else {
            $processedArgs += $Arguments[$i]
        }
    }
    
    Push-Location $jattiPath
    try {
        & python cli.py @processedArgs
    }
    finally {
        Pop-Location
    }
}

'@

# Append to profile
Add-Content -Path $profilePath -Value $jattiFunction -Encoding UTF8

Write-Host "✅ Added 'jatti' command to PowerShell profile!" -ForegroundColor Green
Write-Host "`nNow restart PowerShell and use:" -ForegroundColor Yellow
Write-Host "  jatti run a.jatti" -ForegroundColor Cyan
Write-Host "  jatti build hello.jatti" -ForegroundColor Cyan
Write-Host "  jatti format test.jatti" -ForegroundColor Cyan

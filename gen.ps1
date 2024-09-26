param (
    [switch]$Recursive,
    [string[]]$Directories = @()
)

# Create a function to process a single directory
function Process-Directory {
    param (
        [string]$CurrentDir
    )
    
    $OutputFile = Join-Path -Path $CurrentDir -ChildPath 'config.yml'
    
    # Clear or create the config.yml file
    "contents:" | Set-Content -Path $OutputFile -Encoding utf8

    # Create a hashtable to track processed files
    $ProcessedFiles = @{}

    # Iterate through the current directory and files
    Get-ChildItem -Path $CurrentDir | ForEach-Object {
        $Entry = $_
        
        if ($Entry.PSIsContainer) {
            # Process subdirectories
            $DirName = $Entry.Name
            Add-Content -Path $OutputFile -Value "  - name: $DirName"
            Add-Content -Path $OutputFile -Value "    directory: $DirName"
            
            # If recursive is enabled, recursively call the function for subdirectories
            if ($Recursive) {
                Process-Directory -CurrentDir $Entry.FullName
            }
        } elseif (-not ($Entry.Name -eq 'config.yml')) {
            # Get base name
            if ($Entry.Name -like '*.cpp') {
                $BaseName = $Entry.BaseName
            } elseif ($Entry.Name -like '*-pre.tex') {
                $BaseName = $Entry.BaseName -replace '-pre$', ''
            } elseif ($Entry.Name -like '*-post.tex') {
                $BaseName = $Entry.BaseName -replace '-post$', ''
            } else {
                Write-Host "Unrecognized file: ${Entry}"
                return  # Skip other irrelevant files
            }

            # If this file has not been processed before
            if (-not $ProcessedFiles.ContainsKey($BaseName)) {
                # Mark as processed
                $ProcessedFiles[$BaseName] = $true

                # Prepare to start generating entries
                Add-Content -Path $OutputFile -Value "  - name: $BaseName"

                # Process .cpp files if they exist
                if (Test-Path (Join-Path -Path $currentDir -ChildPath "$baseName.cpp")) {
                    Add-Content -Path $outputFile -Value "    code: $baseName.cpp"
                }

                # Process pre-code and post-code files
                if (Test-Path (Join-Path -Path $currentDir -ChildPath "$baseName-pre.tex")) {
                    Add-Content -Path $outputFile -Value "    code-pre: $baseName-pre.tex"
                }
                if (Test-Path (Join-Path -Path $currentDir -ChildPath "$baseName-post.tex")) {
                    Add-Content -Path $outputFile -Value "    code-post: $baseName-post.tex"
                }
            }
        }
    }

    Write-Host "Generated config.yml file at: $OutputFile"
}

foreach ($Dir in $Directories) {
    if (Test-Path -Path $Dir -PathType Container) {
        Process-Directory -CurrentDir $Dir
    } else {
        Write-Warning "${Dir} is not a valid directory, skipping processing."
    }
}

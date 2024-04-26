Get-Content .\.dev.env | ForEach-Object {
    if ($_ -match '^(.+)=(.+)$') {
        $env:($Matches[1]) = $Matches[2]
    }
}

python -m uvicorn main:app --host $env:HOST --port $env:PORT --reload
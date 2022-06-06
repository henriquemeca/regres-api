param (
    [Parameter(Mandatory=$true,HelpMessage="To execute the script specify the execution mode.
    1: Fetches the API with specfic records per page and saves all data in a CSV file. Use -records to set the records per page and -fileName to set the file name.
    2: Fetches an ID on the API and prints its name.Use -id to set the fetched ID ")][ValidateSet(1,2)][int]$mode,
    [int]$records=12,
    [string]$fileName='users.csv',
    [int]$id=-1
 )

 function getData {
    $r = Invoke-RestMethod -method Get -uri "https://reqres.in/api/users?page=1&per_page=$records"
    $data = $r.data
    $totalPages = $r.total_pages
    Write-Host "Total pages to get $totalPages"
    for($i=2; $i -le $totalPages; $i++){
        Write-Host "Getting page:$i"
        $tempData = Invoke-RestMethod -method Get -uri "https://reqres.in/api/users?page=$i&per_page=$records"
        $data += $tempData.data
    }
    $data |Export-Csv ".\$fileName"
    Write-Host "Finished. $fileName created."
 }

function getId {
    $error.clear()
    try { $r = Invoke-RestMethod -method Get -uri "https://reqres.in/api/users?id=$id" }
    catch { Write-Host 'Id not found' }

    if (!$error) { 
        Write-Host $r.data.first_name $r.data.last_name 
    } 
}

if ($mode -eq 1){
    getData($records)
}

if ($mode -eq 2){
    getId($id)
}
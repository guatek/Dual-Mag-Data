# powershell script to open a directory dialog and select a data directory to process
# with the proc_directory.py srcipt

# Activate the dual-mag python entironoment
conda activate dual-mag

# Change to the script directory. EDIT THIS PATH to point to your script directory
cd c:\software\Guatek\Dual-Mag-Data\scripts

# Helper function to get a directory path from the user
Function Get-DirName() {
    [System.Reflection.Assembly]::LoadWithPartialName("System.windows.forms") | Out-Null
    $OpenDirDialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $OpenDirDialog.ShowDialog() | Out-Null
    return $OpenDirDialog.SelectedPath
}

# Get and check the directory
$dirName = Get-DirName

# run the script if we received a directory
if ($dirName) { 
    python proc_directory.py $dirName
    echo "Done."
}
else {
    echo "No directory selected, done"
}
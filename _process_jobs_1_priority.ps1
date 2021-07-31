Get-WmiObject Win32_process -filter 'name = "python.exe"' | foreach-object { $_.SetPriority(64) }

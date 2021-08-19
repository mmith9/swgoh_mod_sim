Get-WmiObject Win32_process -filter 'name = "python.exe"' | foreach-object { $_.SetPriority(64) }

#Get-WmiObject Win32_process -filter 'name = "HD-player.exe"' | foreach-object { $_.SetPriority(128) }

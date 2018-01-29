@echo off
echo DEPOLYING SITE....
echo ------------------
REM https://stackoverflow.com/questions/664957/can-i-mask-an-input-text-in-a-bat-file
powershell -Command $pword = read-host "Enter password" -AsSecureString ; ^
    $BSTR=[System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pword) ; ^
        [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR) > .tmp.txt
set /p password=<.tmp.txt & del .tmp.txt
python deploy_site.py %password%
pause

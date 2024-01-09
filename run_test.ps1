Remove-Item tests\.test.txt
Get-Date >> .\tests\.test.txt
python -m pytest tests --cov=fileshare >> .\tests\.test.txt
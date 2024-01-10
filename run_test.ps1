# New-Item -ItemType File -Path tests\test_database.db
Remove-Item .test.txt
Get-Date >> .test.txt
python -m pytest tests --cov=fileshare >> .test.txt
Remove-Item tests\test_database.db
# GhemBOT
> Personal Deadline Reminder Assistant

| Anggota | NIM |
| --- | --- |
|Dionisius Darryl H. | 13519058 |	
|Nathaniel Jason | 13519108 |
|Gregorius Dimas Baskara | 13519190 |

## Backend
### Activating venv
**Linux**  
```source project_env/bin/activate```

**Windows CMD**  
```./project_env_win/Scripts/activate.bat```  

**Windows PowerShell**  
```./project_env_win/Scripts/Activate.ps1```

### Deactivating venv
```deactivate```

### Adding dependencies

1. activate the venv
2. use ```pip install``` to add dependencies
3. ```pip freeze```
4. copy the result of pip freeze to ```requirements.txt```

### Installing dependencies
```pip install -r requirements.txt```

### Running flask
**Windows PowerShell**
```
$env:FLASK_APP = "main.py"
flask run
```

## Frontend

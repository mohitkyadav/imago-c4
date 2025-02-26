# imago-c4

### Run project
1. Create a .env file and put your secrets in it. See .env.example.

```commandline
pip install -r requirements.txt
flask --app server run
```

### Search endpoint parameters
| Parameter | Description                     | Default |
|-----------|---------------------------------|---------|
| query     | The search query                | None    |
| size      | The number of results to return | 10      |
| page      | The page number                 | 1       |

### Example search endpoint 
```
GET /search?query=<query>
GET /search?query=<query>&size=<size>
GET /search?query=<query>&size=<size>&page=<page>
```

### Thought Process
Look for file `./thought_process.md`

# imago-c4

### Run project
1. Create a .env file and put your secrets in it. See .env.example.

```commandline
pip install -r requirements.txt
flask --app server run
```

### Search endpoint parameters
| Parameter         | Description                     | Default |
|-------------------|---------------------------------|---------|
| query             | The search query                | None    |
| size              | The number of results to return | 10      |
| page              | The page number                 | 1       |
| filter_fotografen | Filter by photographer name     | None    |
| filter_datum      | Filter by date range            | None    |
| sort              | Sort by field.[asc, desc]       | None    |

### Example search endpoint 
```
GET /search?query=<query>
GET /search?query=<query>&size=<size>
GET /search?query=<query>&size=<size>&page=<page>

# Filters
GET /search?query=<query>&filter_fotografen=<filter_fotografen>
GET /search?query=<query>&filter_datum=2020-01-01 TO 2020-09-12

# Sort By
GET /search?query=<query>&sort=datum.desc
GET /search?query=<query>&sort=fotografen.asc

# Stats
GET /search/stats
```

### Thought Process
Look for file `./thought_process.md`

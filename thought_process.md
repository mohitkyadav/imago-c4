# Thought Process
### The problem
1. Understanding the problem.
2. Scaffolding a basic flask based server.
3. Verified that given Elasticsearch credentials are valid.

### The basic solution
1. Add search endpoint, that returns the search results.
2. Add page size to the search results. So the response time can be lowered if there are too many results.

### More filters and sorting
1. Add filters, `filter_fotografen` and `filter_datum`.
2. Add sorting, `sort`, usage: `sort=field.[asc or desc]`.

### Handling errors and validations
> [!NOTE]  
> I came up with the following validations and error handling.
> These are not hard rules, rather some examples of how I would handle them.

1. The search query must have a minimum of 3 characters.
2. The search query must not exceed 100 characters.

### Testing
1. I wrote tests for the health and search endpoint.
2. Used unittest for testing.
3. Also wrote tests for utils.

## Thoughts and learnings 
### Optimizing the solution with AI
We can use AI to predict the search query. For example if a user searches for the term
"Boy with toy weapons by ZUMA Press Wire from 20th centuary for mobile width", the AI can generate the search query for us.
In this case it would parse this and give us useful values for search and filter fields. In this case:
```json
{
    "suchtext": "Boy with toy weapons",
    "fotografen": "ZUMA Press Wire",
    "date.lte": "2000-01-01",
    "date.gte": "1900-01-01",
    "width.lte": "768"
}
```
And we can use this data to further optimize the search query.

### Further optimizations
1. We can add importance to the search fields, so the search results can be more relevant.
2. We can add ranges `{"range": {"hoehe": {"gte": 2000}}}`, to further filter images based on their target device width.
3. We can do bool query to combine multiple match queries for different fields.

### Scaling the solution
1. It can be horizontally scaled by creating more than 1 Elasticsearch clusters.
2. The search query can be cached, so the response time can be lowered.
    - We can use Redis for caching.
    - We can cache the search query and the results.
    - We can cache the search query and the results for a specific time.
    - We can cache the search query and the results for a specific location if we have access to it.


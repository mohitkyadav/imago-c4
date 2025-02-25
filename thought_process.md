# Thought Process
### The problem
1. Understanding the problem.
2. Scaffolding a basic flask based server.
3. Verified that given Elasticsearch credentials are valid.

### The basic solution
1. Add search endpoint, that returns the search results.
2. Add pagination to the search results.

### Handling errors and validations
> [!NOTE]  
> I came up with the following validations and error handling.
> These are not hard rules, rather some examples of how I would handle them.

1. The search query must have a minimum of 3 characters.
2. The search query must not exceed 100 characters.

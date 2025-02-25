def validate_query_text(query):
    print(len(query))
    if not query:
        return {'error': 'Search query is required'}, 400

    if len(query) < 3:
        return {'error': 'Search query must be at least 3 characters long'}, 400
    
    if len(query) > 100:
        return {'error': 'Search query must be at most 100 characters long'}, 400

    return None
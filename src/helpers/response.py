def make_response(body={'message': 'Success!'}, code=200):
    '''
    Make a JSON-String response
    :params payload: list of lightning events
    '''
    import json
    return {
        'statusCode': code,
        'body': json.dumps(body)
    }

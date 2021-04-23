import json
def make_response(body={'message': 'Success!'}, code=200, cors=False):
    '''
    Return a response with a code and message
    :params code: int, HTTP code of error or success. default = 200, success
    :params body: dict, dictionary on JSON format to be sent onwards
    '''
    response = {
        "statusCode": code,
        "body": json.dumps(body)
    }
    if cors:
        response['headers']={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
            }
    return response


def send_request(url, params={}):
    '''
    
    '''
    import requests
    try: 
        return requests.get(url, params, timeout=20)
    except TimeoutError:
        print(f"Timeout: {url}")
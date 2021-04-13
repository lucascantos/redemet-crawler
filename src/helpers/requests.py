
def send_request(url, params={}):
    '''
    
    '''
    import requests
    try: 
        return requests.get(url, params, timeout=20)
    except TimeoutError:
        print(f"Timeout: {url}")
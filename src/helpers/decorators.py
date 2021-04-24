def retry_request(func):
    '''
    Decorator for retrying a function
    '''
    from time import sleep
    MAX_RETRIES: 3
    wait_time = 2
    def wrapper(args, kwargs):
        for i in range(MAX_RETRIES):
            try:
                response = func(args)
            except:
                print(f'Fail {i+1}. Retrying in {wait_time}s')
                sleep(wait_time)
                continue
            return response        
        raise TimeoutError
    return wrapper


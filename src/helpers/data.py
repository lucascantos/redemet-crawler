def image_base64(image_bytes):
    '''
    Converts image to Base64 string
    :params image_bytes: Image data in bytes format
    '''
    import base64
    base64_bytes = base64.b64encode(image_bytes)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

def decode_base64(base64_string):
    '''
    Converts Base64 string image into Image
    :params image_bytes: Image data in bytes format
    '''
    import base64
    decodedBytes = base64.b64decode(base64_string)
    return str(decodedBytes, "utf-8")


def multi_threading(func, args):
    '''
    Run multitreading of a functions
    :params func: Function to be run
    :params args: Arguments of function. Each argument must be a list of entries
    '''
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if func.__code__.co_argcount >= 2 :
            return executor.map(lambda args: func(**args), args)
        else:
            return executor.map(func, args)

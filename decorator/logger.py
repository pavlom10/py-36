from datetime import datetime

def logger(file_name):
    def decorator(foo):
        def new_function(*args, **kwargs):
            result = foo(*args, **kwargs)

            with open(file_name, 'a') as file:
                file.write(f"Today's date: {datetime.now()}")
                file.write(f" | Function: {foo.__name__}")
                file.write(f" | Args: {args} {kwargs}")
                file.write(f" | Result: {result}")
                file.write('\n')

            return result
        return new_function
    return decorator



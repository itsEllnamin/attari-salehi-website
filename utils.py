def create_random_code(count):
    from random import randint
    return randint(10**(count-1), 10**count-1)

def send_sms(mobile_number, message):
    pass
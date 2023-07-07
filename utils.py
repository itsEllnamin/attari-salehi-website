def create_random_code(count):
    from random import randint
    return randint(10**(count-1), 10**count-1)

def send_sms(template, mobile_number, message):
    # from kavenegar import KavenegarAPI, APIException, HTTPException
    # try:
    #     api = KavenegarAPI('7A41476C576F4F654458567330793652384B596B576950522B6643794B536B757634736B324342525464733D')
    #     params = {
    #         'receptor': mobile_number,
    #         'template': template,
    #         'token': message,
    #         'token2': '',
    #         'token3': '',
    #         'type': 'sms',#sms vs call
    #     }   
    #     response = api.verify_lookup(params)
    #     print(response)
    # except APIException as e: 
    #     print(e)
    # except HTTPException as e: 
    #     print(e)
    pass
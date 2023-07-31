def page_path(appname, filename):
    return f"{appname}/{filename}.html"

def partial_path(appname, filename):
    return f"{appname}/partials/{filename}.html"

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

class FileManager():
    def __init__(self, filetype, app_name, prefix):
        self.filetype = filetype
        self.app_name = app_name
        self.prefix = prefix
    
    def upload_to(self, instance, filename):
        from os.path import splitext
        from uuid import uuid4
        
        filename, ext = splitext(filename)
        file_name = f'{instance}{uuid4()}{ext}'
        self.file_path = f'{self.filetype}/{self.app_name}/{self.prefix}/{file_name}'
        return self.file_path

    def remove_file(self):
        import os
        from django.conf import settings
        
        media_root = settings.MEDIA_ROOT
        file_path = media_root+self.file_path
        folder_path = os.path.split(file_path)[0]
        if  os.path.exists(file_path) and os.path.isfile(file_path)  :
            os.remove(file_path)
        if  os.path.exists(folder_path) and os.path.isdir(folder_path)  :
            files = os.listdir(folder_path)
            if  len(files) == 0  :
                os.rmdir(folder_path)


def factor_details(total_price, order_discount=0):
    delivery_cost = 25000
    if  total_price >= 200000 :
        delivery_cost = 0
    # tax  =  int(0.09 * (total_price+delivery_cost))
    final_price  =  total_price + delivery_cost# + tax
    if  order_discount > 0  :
        final_price  =  final_price - (int(final_price*order_discount/100))
    return delivery_cost, final_price#, tax
import json
import time
import os
from random import randrange
import requests
from dotenv import load_dotenv
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll


load_dotenv()
TOKEN = os.getenv('TOKEN')
vk_sesion = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_sesion)
vk = vk_sesion.get_api()

url = f"https://cataas.com/cat/says/{'wtf'}?t=${time.time()}"


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.from_user:
        if event.text=='кот':                    
            responseArt = requests.get(url)
            img_file = open(f"random_cat.png" , 'wb')
            img_file.write(responseArt.content)
                    
            pfile = requests.post(vk.photos.getMessagesUploadServer(peer_id = event.user_id)['upload_url'], files = {'photo': open('random_cat.png', 'rb')}).json()
            photo = vk.photos.saveMessagesPhoto(server = pfile['server'], photo = pfile['photo'], hash = pfile['hash'])[0]
                    
            vk.messages.send(user_id=event.user_id, random_id=randrange(1,100000000), attachment ='photo%s_%s,'%(photo['owner_id'], photo['id'])) 

        else:
           vk.messages.send(user_id=event.user_id, message = 'Покемон не найден :(', random_id=randrange(1,100000000))

                    
                   

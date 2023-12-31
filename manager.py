import random
import wikipedia

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import vk_api

from tools.settings import config
from tools.utils import send_mess, send_mess_kb, get_weather, get_random_id, send_stat, add_user_to_list

from models.user import User 
from models.content import all_tests, all_tests_desription 
from models.keyboards import *

import enum
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def drive_test(event: VkLongPoll.DEFAULT_EVENT_CLASS, user: User, vk_api_method, longpoll):
    
    send_mess_kb(event=event, vk_api_method=vk_api_method,
                 keyboard=test_choice_keyboard,
                 message='Type exit or...\n'+all_tests_desription)
    
    position='test_choice'
    for event in longpoll.listen():
        
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            
            if position=='test_choice' and event.text in all_tests:

                good_info = user.run_test(test_name=event.text, event=event, longpoll=longpoll, vk_api_method=vk_api_method)
                
                send_mess_kb(event=event, vk_api_method=vk_api_method, keyboard=test_choice_keyboard,
                            message="You have done test! Congrats!\n"+good_info)
                
            elif event.text == 'Exit':
                break
            else:
                send_mess_kb(event=event, vk_api_method=vk_api_method,
                            keyboard=test_choice_keyboard,
                            message=f"Comand not found")
                
    
def welcome(event: VkLongPoll.DEFAULT_EVENT_CLASS, vk_api_method, longpoll):
    
    send_mess_kb(event=event, vk_api_method=vk_api_method,
                 keyboard=welcome_keyboard,
                 message='You are on welcome page of Test! Lets go? (GO! / exit)')
    
    position='start'
    user = User(event.user_id)
    
    for event in longpoll.listen():
        
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            
            if event.text.lower() == 'exit':
                break
            
            elif position=='start' and event.text=='GO!':
                vk_api_method.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    message='Lets make auth. What is your name?'
                )
                position='wait for name'
                
            elif position=='start' and event.text!='GO!':
                vk_api_method.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    message='Command not found. Type GO! or exit'
                )
                position='start'
                
            elif position=='wait for name' and event.text!='GO!':
                user.name = event.text
                send_mess_kb(event=event, vk_api_method=vk_api_method,keyboard=menu_keyboard, message=f"Hi, {user.name}. Here is the main menu:")
                add_user_to_list()
                position='menu'
            
            # Menu
            elif position=='menu':
                if event.text == 'Profile':
                    send_mess(event=event, vk_api_method=vk_api_method,
                              message=f'Your profile: {user}')
                    send_mess_kb(event=event, vk_api_method=vk_api_method,keyboard=menu_keyboard, message=f"Here is the main menu:")
                    position='menu'
                    
                elif event.text == 'Tests':
                    send_mess(event=event, vk_api_method=vk_api_method,
                              message=f'Lets start doing. We have some tests. Look!')
                    drive_test(event=event, user=user, vk_api_method=vk_api_method, longpoll=longpoll)
                    send_mess_kb(event=event, vk_api_method=vk_api_method,keyboard=menu_keyboard, message=f"Here is the main menu:")
                    position = 'menu'
                    
                elif event.text == 'Statistic':
                    if user.get_statistic():
                        send_mess(event=event, vk_api_method=vk_api_method, 
                                  message='Statistic is loading...')
                        send_stat(user=user,event=event, vk_api_method=vk_api_method, f_name='score_stat')
                        send_stat(user=user, event=event, vk_api_method=vk_api_method, f_name='time_stat')
                        
                        send_mess(event=event, vk_api_method=vk_api_method, 
                                  message='Avarage results:\n'+user.statistic.average_each())
                        
                    send_mess_kb(event=event, vk_api_method=vk_api_method,keyboard=menu_keyboard, message=f"Here is the main menu:")
                    position='menu'
                    
                else:
                    send_mess(event=event, vk_api_method=vk_api_method,
                        message=f'Command not found'
                    )
                    send_mess_kb(event=event, vk_api_method=vk_api_method,keyboard=menu_keyboard, message=f"Here is the main menu:")
                    position='menu'

                          
    send_mess(event=event, vk_api_method=vk_api_method, message="Finishing all progress")
    

def manage_event(event: VkLongPoll.DEFAULT_EVENT_CLASS, vk_api_method, longpoll):

    message = event.text
    if event.text.startswith('help'):
        logging.info('help event')
        message = 'What i can do: \n wikipedia: ... \n weather: ... \n tests:...'
        
    elif event.text.startswith('tests'):
        logging.info('tests event')
        welcome(event=event, vk_api_method=vk_api_method, longpoll=longpoll)
        return
    
    elif event.text.startswith('+'):
        logging.info('event plus!')
        message = 'oh, plus'
        
    elif event.text.startswith('echo'):
        logging.info('echo event')
        message = event.text.split()[1:]
        
    elif event.text.startswith('wikipedia'):
        logging.info('wikipedia event')
        subject = ' '.join(event.text.split()[1:])
        try:
            message = wikipedia.summary(subject)
        except:
            message = 'subject not found'
            
    elif event.text.startswith('keyboard'):
        logging.info('event keyboard')
        vk_api_method.messages.send(keyboard=test_keyboard.get_keyboard(),
            key= (config.keyboard_key),
            server= ("https://lp.vk.com/whp/222723275"),
            ts = ("121"),
            user_id = event.user_id,
            random_id = get_random_id(),
            message='Keyboard:'
        )
        return
        
    elif event.text.startswith('weather'):
        logging.info('weather event')
        city = ' '.join(event.text.split()[1:])
        message = get_weather(city)
        
    else:
        pass
    
    vk_api_method.messages.send(user_id = event.user_id,
                       random_id = get_random_id(),
                       message = message
                       )
            
    


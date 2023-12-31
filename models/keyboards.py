from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Hello', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Goodbay', color=VkKeyboardColor.NEGATIVE)
keyboard.add_line()
keyboard.add_location_button()
keyboard.add_line()
keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=222723275")


test_keyboard = VkKeyboard(inline=True)
test_keyboard.add_button('A')
test_keyboard.add_button('B')
test_keyboard.add_button('C')
test_keyboard.add_button('D')

welcome_keyboard = VkKeyboard(one_time=True)
welcome_keyboard.add_button('GO!', color=VkKeyboardColor.POSITIVE)

menu_keyboard = VkKeyboard(one_time=True)
menu_keyboard.add_button('Tests')
menu_keyboard.add_button('Profile')
menu_keyboard.add_button('Statistic')
menu_keyboard.add_button('exit', color=VkKeyboardColor.NEGATIVE)

profile_keyboard = VkKeyboard(one_time=True)
profile_keyboard.add_button('Edit name', color=VkKeyboardColor.POSITIVE)
profile_keyboard.add_button('Edit email', color=VkKeyboardColor.NEGATIVE)


all_tests = ['Geography', 'Counting', 'Simple numbers']

test_choice_keyboard = VkKeyboard(one_time=True)
for test_name in all_tests:
    test_choice_keyboard.add_button(test_name)
    
test_choice_keyboard.add_button('Exit', color=VkKeyboardColor.NEGATIVE)

logging.info('keyboards created')
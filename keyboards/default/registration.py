from aiogram.types import KeyboardButton

btn_registration = [["Start Registration"]]
btn_phone_number = [[KeyboardButton("Phone number", request_contact=True)]]

btn_menu_user_with_resume = [
    ["Update Resume", "Send to Moderator"],
    ["Get My Resume", "Settings"]
]

btn_menu_user_without_resume = [
    ["Create Resume", "Send to Moderator"],
    ["Get My Resume", "Settings"]
]

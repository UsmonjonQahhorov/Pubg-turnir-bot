import json


class AdminPanel:
    def __init__(self):
        self.chat_ids = {}
        self.last_user_id = 1  # Boshlanish raqami

    def generate_user_id(self):
        new_user_id = self.last_user_id
        self.last_user_id += 1
        return new_user_id

    def add_chat_id(self, chat_id):
        user_id = self.generate_user_id()  # Avtomatik user_id yaratish
        self.chat_ids[str(user_id)] = chat_id

    # Yoki, user_id berilganida
    def add_chat_id_with_user_id(self, user_id, chat_id):
        self.chat_ids[str(user_id)] = chat_id

    def save_to_json(self, filename):
        with open("admins.json", 'w') as json_file:
            json.dump(self.chat_ids, json_file, indent=4)

    def load_from_json(self, filename):
        try:
            with open("admins.json", 'r') as json_file:
                self.chat_ids = json.load(json_file)
        except FileNotFoundError:
            self.chat_ids = {}


admin_panel = AdminPanel()

# Yangi chat ID ni qo'shish
# admin_panel.add_chat_id(chat_id=456)
# admin_panel.add_chat_id(chat_id=987)
# admin_panel.add_chat_id(chat_id=3453)

# JSON faylga saqlash
admin_panel.save_to_json('admins.json')

# JSON fayldan o'qish
admin_panel.load_from_json('admins.json')

# Chat ID larni ko'rish
print(admin_panel.chat_ids)

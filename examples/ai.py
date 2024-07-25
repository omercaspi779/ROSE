import signal

import pygame
import json
import os
from examples.get_user_db import get_user_data_dir
import subprocess
global process
pygame.init()
pygame.mixer.init()
global json_file_path
SCREEN_HEIGHT = 659
SCREEN_WIDTH = 1280
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Crest')

back_img = pygame.image.load("רקע.jpg")
back_img = pygame.transform.scale(back_img, screen_size)
icon_ = pygame.image.load('icon_.jpg')
pygame.display.set_icon(icon_)

color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

smallfont_2 = pygame.font.SysFont('Marlett', 130)
smallfont_3 = pygame.font.SysFont('ebrima', 64)
smallfont_4 = pygame.font.SysFont('Corbel', 40)
smallfont_5 = pygame.font.SysFont('Corbel', 25)

welcome_text = smallfont_2.render('welcome to Crest', True, (135, 206, 235))
welcome_text_2 = smallfont_3.render('to start the game please log in or sign up', True, (135, 206, 235))

screen_center_x = SCREEN_WIDTH // 2
screen_center_y = SCREEN_HEIGHT // 2
button_width = 200
button_height = 100
button_x = screen_center_x - button_width // 2
button_y = screen_center_y - button_height // 2
#
#
# sound_effect = pygame.mixer.Sound("error.mp3")
# sound_effect4 = pygame.mixer.Sound("Futuristic interface  HUD sound effects.mp3")


class Button:
    def _init_(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def drew_text(self, text, font, font_size, color_):
        font_ = pygame.font.SysFont('Marlett', font_size)
        text_ = font_.render(text, True, color_)
        text_rect = text_.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_, text_rect)

    def mouse_over_button(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

    def drew_rec(self, mouse_over_button):
        if mouse_over_button:
            icon = pygame.image.load("button.png")
            icon = pygame.transform.scale(icon, (self.width, self.height))
            icon_rect = icon.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(icon, icon_rect)
        else:
            icon = pygame.image.load("noBackground.png")
            icon = pygame.transform.scale(icon, (self.width, self.height))
            icon_rect = icon.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(icon, icon_rect)


class Coustum_button:
    def _init_(self, width, height, x, y, icon):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.icon = icon

    def drew_icon(self):
        icon_rect = self.icon.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(self.icon, icon_rect)

    def drew_rec(self):
        screen.blit(self.icon, (self.x, self.y))


class User:
    def _init_(self, user_name, password):
        self.user_name = user_name
        self.password = password
        self.level = "1"
        self.points = 14
        self.connected = False
        # self.ip = n.get_target_ip()

    def get_user_name(self):
        return self.user_name

    def get_password(self):
        return self.password

    def set_user_name(self, user_name):
        self.user_name = user_name

    def set_password(self, password):
        self.password = password

    def get_connected(self):
        return self.connected

    def set_connected(self, connect):
        self.connected = connect

    def is_username_connected(self):
        return self.connected

    def get_points(self):
        return self.points

    # def get_ip(self):
    #     return self.ip

    def save_data(self):
        global json_file_path
        user_data_dir = get_user_data_dir()
        json_file_path = user_data_dir / 'crest_data' / 'user-data.json'
        json_file_path.parent.mkdir(parents=True, exist_ok=True)
        data = []
        user_exists = False

        try:
            if json_file_path.exists() and json_file_path.stat().st_size > 0:
                with json_file_path.open('r') as f:
                    existing_data = json.load(f)
                    for user in existing_data:
                        if user["username"] == self.user_name:
                            user["gameLevel"] = self.level
                            user["gamePoints"] = self.points
                            user_exists = True
                        data.append(user)

            if not user_exists:
                new_user_data = {
                    "username": self.user_name,
                    "password": self.password,
                    "gameLevel": self.level,
                    "gamePoints": self.points,
                }
                data.append(new_user_data)

            # Use a temporary file to avoid data loss if write fails
            temp_file = json_file_path.with_suffix('.tmp')
            with temp_file.open('w') as f:
                json.dump(data, f, indent=4)

            # If successful, replace the original file
            temp_file.replace(json_file_path)

            print(f"Data saved successfully to {json_file_path}")

        except json.JSONDecodeError:
            print(f"Error reading JSON from {json_file_path}. File might be corrupted.")
        except PermissionError as e:
            print(f"Permission denied when trying to write to {json_file_path}")
            print(f"Error details: {str(e)}")
            print("\nTroubleshooting steps:")
            print("1. Ensure you have write permissions for the directory.")
            print("2. Try running the program with administrator privileges.")
            print("3. Check if any other program is using the file.")
            print(f"4. Manually create the directory: {json_file_path.parent}")
        except Exception as e:
            print(f"An error occurred while saving data: {str(e)}")

    def load_data_to_user_variables(self):
        global json_file_path
        with json_file_path.open("user-data.json", "r") as f:
            data = json.load(f)
            for user in data:
                if user["username"] == self.user_name:
                    self.user_name = user["username"]
                    self.password = user["password"]
                    self.level = user["gameLevel"]
                    self.points = user["gamePoints"]
                    self.ip = user["ip"]

    def connect(self):
        self.connected = True

    def add_point(self):
        self.points += 1

    def print_details(self):
        print(f"{self.user_name}, {self.password}, {self.level}, {self.points}, {self.ip}")


class TextBox:
    def _init_(self, x, y, width, height, font, user_text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 0, 0)
        self.user_text = user_text
        self.font = font
        self.active = True

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, 2)


def load_data():
    global users
    users = []
    if os.path.isfile('users_data.json') and os.path.getsize('users_data.json') > 0:
        with open("users_data.json", "r") as f:
            data = json.load(f)
            for user_data in data:
                user = User(user_data["username"], user_data["password"])
                users.append(user)


global users
users = []
global username_text_log_in
username_text_log_in = ''
global password_text_log_in
password_text_log_in = ''
global confirm_username_log_in
confirm_username_log_in = False
global confirm_password_log_in
confirm_password_log_in = False
global new_text_log_in
new_text_log_in = ''
global new_text_log_in_
new_text_log_in_ = ''
global username_text_sign_up
username_text_sign_up = ''
global password_text_sign_up
password_text_sign_up = ''
global confirm_username_sign_up
confirm_username_sign_up = False
global confirm_password_sign_up
confirm_password_sign_up = False
global new_text_sign_up
new_text_sign_up = ''
global new_text_sign_up_
new_text_sign_up_ = ''
global username_text_war
username_text_war = ''
global password_text_war
password_text_war = ''
global confirm_username_war
confirm_username_war = False
global confirm_password_war
confirm_password_war = False
global new_text_war
new_text_war = ''
global new_text_war_
new_text_war_ = ''
global c
c = False

def start_screen():
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(back_img, (0, 0))
    log_in_button = Button(150, 50, 950, 10)
    log_in_button.drew_rec(log_in_button.mouse_over_button(mouse_pos))
    log_in_button.drew_text("log in", 'Corbel', 30, color)
    sign_up_button = Button(150, 50, 1110, 10)
    sign_up_button.drew_rec(sign_up_button.mouse_over_button(mouse_pos))
    sign_up_button.drew_text("sign up", 'Corbel', 30, color)
    screen.blit(welcome_text, (270, SCREEN_HEIGHT / 2 - 70))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'quit'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if log_in_button.mouse_over_button(mouse_pos):
                return "log in"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if sign_up_button.mouse_over_button(mouse_pos):
                return "sign up"
    return 'start'


def sign_up_screen():
    global sound_effect
    global users
    global username_text_sign_up
    global password_text_sign_up
    global confirm_username_sign_up
    global confirm_password_sign_up
    global new_text_sign_up
    global new_text_sign_up_
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(back_img, (0, 0))
    back_to_start_button = Button(150, 50, 1117, 12)
    back_to_start_button.drew_rec(back_to_start_button.mouse_over_button(mouse_pos))
    back_to_start_button.drew_text("Back to home", 'Corbel', 30, color)
    username_box = TextBox(200, 250, 1000, 50, smallfont_3, username_text_sign_up)
    password_box = TextBox(200, 450, 1000, 50, smallfont_3, password_text_sign_up)
    password_box.draw()
    password_text = smallfont_4.render(f'enter password:', True, color)
    screen.blit(password_text, (200, 380))
    username_box.draw()
    username_text_ = smallfont_4.render(f'enter username:', True, color)
    screen.blit(username_text_, (200, 180))
    load_data()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'quit'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_to_start_button.mouse_over_button(mouse_pos):
                username_text_sign_up = ''
                password_text_sign_up = ''
                new_text_sign_up = ''
                new_text_sign_up_ = ''
                confirm_username_sign_up = False
                confirm_password_sign_up = False
                return "start"
        if event.type == pygame.TEXTINPUT:
            if confirm_username_sign_up is False:
                new_text_sign_up += event.text
            elif confirm_password_sign_up is False:
                new_text_sign_up_ += event.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if confirm_username_sign_up is False:
                    try:
                        new_text_sign_up = new_text_sign_up[:-1]
                    except IndexError:
                        pass
                elif confirm_password_sign_up is False:
                    try:
                        new_text_sign_up_ = new_text_sign_up_[:-1]
                    except IndexError:
                        pass
            if event.key == pygame.K_RETURN:
                if confirm_username_sign_up is False and len(new_text_sign_up) > 0:
                    for user in users:
                        if new_text_sign_up == user.get_user_name():
                            new_text_sign_up = ''
                            return 'sign up'
                    confirm_username_sign_up = True
                elif confirm_password_sign_up is False and len(new_text_sign_up_) > 0 and len(new_text_sign_up) > 0:
                    confirm_password_sign_up = True
                    user = User(username_text_sign_up, password_text_sign_up)
                    users.append(user)
                    user.save_data()
                    username_text_sign_up = ''
                    password_text_sign_up = ''
                    new_text_sign_up = ''
                    new_text_sign_up_ = ''
                    confirm_username_sign_up = False
                    confirm_password_sign_up = False
    text_width_ = smallfont_4.size(new_text_sign_up_)[0]
    if text_width_ <= 990 and confirm_password_sign_up is False:
        password_text_sign_up = new_text_sign_up_
    text_width_2 = smallfont_4.size(new_text_sign_up)[0]
    if text_width_2 <= 990 and confirm_username_sign_up is False:
        username_text_sign_up = new_text_sign_up
    text_3 = smallfont_4.render(password_text_sign_up, True, color)
    text_rect_ = text_3.get_rect(topleft=(password_box.rect.x + 5, password_box.rect.y + 5))
    if text_rect_.w <= 990:
        screen.blit(text_3, (password_box.rect.x + 5, password_box.rect.y + 8))
    text_2 = smallfont_4.render(username_text_sign_up, True, color)
    text_rect = text_2.get_rect(topleft=(username_box.rect.x + 5, username_box.rect.y + 5))
    if text_rect.w <= 990:
        screen.blit(text_2, (username_box.rect.x + 5, username_box.rect.y + 8))
    return 'sign up'



def log_in_screen():
    global c
    global sound_effect
    global users
    global username_text_log_in
    global password_text_log_in
    global confirm_username_log_in
    global confirm_password_log_in
    global new_text_log_in
    global new_text_log_in_
    global clients_connected
    global current_user
    global current_username
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(back_img, (0, 0))
    back_to_start_button = Button(150, 50, 1117, 12)
    back_to_start_button.drew_rec(back_to_start_button.mouse_over_button(mouse_pos))
    back_to_start_button.drew_text("Back to home", 'Corbel', 30, color)
    username_box_2 = TextBox(200, 250, 1000, 50, smallfont_3, username_text_log_in)
    password_box_2 = TextBox(200, 450, 1000, 50, smallfont_3, password_text_log_in)
    password_box_2.draw()
    password_text_2 = smallfont_4.render(f'enter password:', True, color)
    screen.blit(password_text_2, (200, 380))
    username_box_2.draw()
    username_text_2 = smallfont_4.render(f'enter username:', True, color)
    screen.blit(username_text_2, (200, 180))
    load_data()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return 'quit'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_to_start_button.mouse_over_button(mouse_pos):
                username_text_log_in = ''
                password_text_log_in = ''
                new_text_log_in = ''
                new_text_log_in_ = ''
                confirm_username_log_in = False
                confirm_password_log_in = False
                return "start"
        if event.type == pygame.TEXTINPUT:
            if confirm_username_log_in is False:
                new_text_log_in += event.text
            elif confirm_password_log_in is False:
                new_text_log_in_ += event.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if confirm_username_log_in is False:
                    try:
                        new_text_log_in = new_text_log_in[:-1]
                    except IndexError:
                        pass
                elif confirm_password_log_in is False:
                    try:
                        new_text_log_in_ = new_text_log_in_[:-1]
                    except IndexError:
                        pass
            if event.key == pygame.K_RETURN:
                if confirm_username_log_in is False and len(new_text_log_in) > 0:
                    confirm_username_log_in = True
                    confirm_password_log_in = False
                elif confirm_password_log_in is False and len(new_text_log_in_) > 0:
                    confirm_password_log_in = True
                    login_successful = False
                    for user in users:
                        if new_text_log_in == user.get_user_name() and new_text_log_in_ == user.get_password() and len(new_text_log_in_) > 0 and len(new_text_log_in) > 0:
                            if user.is_username_connected():
                                sound_effect.play()
                                username_text_log_in = ''
                                password_text_log_in = ''
                                new_text_log_in = ''
                                new_text_log_in_ = ''
                                confirm_username_log_in = False
                                confirm_password_log_in = False
                                return 'log in'
                            else:
                                user.connect()
                                current_username = user.get_user_name()
                                current_user = user
                                username_text_log_in = ''
                                password_text_log_in = ''
                                new_text_log_in = ''
                                new_text_log_in_ = ''
                                confirm_username_log_in = False
                                confirm_password_log_in = False
                                c = True
                                login_successful = True
                                return "start2"
                    if not login_successful:
                        username_text_log_in = ''
                        password_text_log_in = ''
                        new_text_log_in = ''
                        new_text_log_in_ = ''
                        confirm_username_log_in = False
                        confirm_password_log_in = False
    text_width_2 = smallfont_4.size(new_text_log_in_)[0]
    if text_width_2 <= 990 and confirm_password_log_in is False:
        password_text_log_in = new_text_log_in_
    text_width2 = smallfont_4.size(new_text_log_in)[0]
    if text_width2 <= 990 and confirm_username_log_in is False:
        username_text_log_in = new_text_log_in

    text_5 = smallfont_4.render(password_text_log_in, True, color)
    text_rect_ = text_5.get_rect(topleft=(password_box_2.rect.x + 5, password_box_2.rect.y + 5))
    if text_rect_.w <= 990:
        screen.blit(text_5, (password_box_2.rect.x + 5, password_box_2.rect.y + 8))
    text_1 = smallfont_4.render(username_text_log_in, True, color)
    text_rect = text_1.get_rect(topleft=(username_box_2.rect.x + 5, username_box_2.rect.y + 5))
    if text_rect.w <= 990:
        screen.blit(text_1, (username_box_2.rect.x + 5, username_box_2.rect.y + 8))
    return 'log in'


def start_screen_2():
    global current_user
    global current_username
    global users
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(back_img, (0, 0))
    log_in_button = Button(button_width, button_height, 112, 292 - button_height)
    log_in_button.drew_rec(log_in_button.mouse_over_button(mouse_pos))
    log_in_button.drew_text("START SERVER", 'Corbel', 50, color)
    back_to_start_button = Button(button_width, button_height, 110, 322)
    back_to_start_button.drew_rec(back_to_start_button.mouse_over_button(mouse_pos))
    back_to_start_button.drew_text("LOG OUT", 'Corbel', 50, color)
    lobby_button = Button(button_width, button_height, 100, 452)
    lobby_button.drew_rec(lobby_button.mouse_over_button(mouse_pos))
    lobby_button.drew_text("CONNECT DRIVER", 'Corbel', 50, color)
    load_data()
    if current_user.get_connected():
        text_width = smallfont_4.size(current_username)[0]
        user_name_text = smallfont_4.render(f'welcome! {current_username}', True, (135, 206, 235))
        screen.blit(user_name_text, (1130 - text_width - 150, 58))
    image = pygame.image.load("user.png")
    image = pygame.transform.scale(image, (100, 80))
    user_button = Coustum_button(150, 150, 1130, 5, image)
    user_button.drew_icon()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # n.send("disconnect")
            return 'quit'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if log_in_button.mouse_over_button(mouse_pos):
                return "open server"
            if back_to_start_button.mouse_over_button(mouse_pos):
                current_user.set_connected(False)
                # n.send("disconnect")  # Send a disconnect message to the server
                current_username = ""
                return "start"
            if lobby_button.mouse_over_button(mouse_pos):
                return "connect client"
    return 'start2'


def open_server():
    global process
    mouse_pos = pygame.mouse.get_pos()
    im = pygame.image.load("רקע_2.jpg")
    im = pygame.transform.scale(im, screen_size)
    screen.blit(im, (0, 0))
    back_to_start_button = Button(150, 50, 25, 12)
    back_to_start_button.drew_rec(back_to_start_button.mouse_over_button(mouse_pos))
    back_to_start_button.drew_text("Back to lobby", 'Corbel', 30, color)
    font = pygame.font.Font(None, 35)
    text_ = font.render(f"waiting for other player to connect.....", True, (255, 255, 255))
    screen.blit(text_, (450, 300))
    os.chdir(r"C:\Users\user\Desktop\red hut camp")
    venv_python = r".venv\rose\Scripts\activate"
    subprocess.run(
        f'cmd /c "{venv_python} && echo Activation successful && set"',
        cwd=r"C:\Users\user\Desktop\red hut camp",
        capture_output=True,
        text=True,
        shell=True
    )
    os.chdir(r"C:\Users\user\Desktop\red hut camp\ROSE")
    process = subprocess.Popen(['python', "rose-server"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_to_start_button.mouse_over_button(mouse_pos):
                os.kill(process.pid, signal.SIGINT)
                return "start2"
        if event.type == pygame.QUIT:
            os.kill(process.pid, signal.SIGINT)
            return 'quit'
    return "connect client come from start server"



global ip_text
ip_text = ''
global path_text
path_text = ''
global new_text_client
new_text_client = ''
global new_text_client_
new_text_client_ = ''
global complete_ip
complete_ip = False
global complete_path
complete_path = False

def process2():
    venv_ =r".venv\rose\Scripts\activate"
    process2 = subprocess.Popen(
        ['python', "rose-client", "-s", "127.0.0.1", r"C:\Users\user\Desktop\red hut camp\ROSE\examples\none.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    return process2

def connect_client(come_from_server):
    global ip_text
    global complete_path
    global complete_ip
    global path_text
    global new_text_client
    global new_text_client_
    global process
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(back_img, (0, 0))
    back_to_start_button = Button(150, 50, 1117, 12)
    back_to_start_button.drew_rec(back_to_start_button.mouse_over_button(mouse_pos))
    back_to_start_button.drew_text("Back to home", 'Corbel', 30, color)
    username_box_2 = TextBox(200, 250, 1000, 50, smallfont_3, ip_text)
    password_box_2 = TextBox(200, 450, 1000, 50, smallfont_3, path_text)
    password_box_2.draw()
    password_text_2 = smallfont_4.render(f'enter driver file path:', True, color)
    screen.blit(password_text_2, (200, 380))
    username_box_2.draw()
    username_text_2 = smallfont_4.render(f'enter server ip(if the server is on your computer just press enter):', True, color)
    screen.blit(username_text_2, (200, 180))
    load_data()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.kill(process.pid, signal.SIGINT)
            os.kill(process2().pid, signal.SIGINT)
            return 'quit'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_to_start_button.mouse_over_button(mouse_pos):
                ip_text = ''
                path_text = ''
                new_text_client = ''
                new_text_client_ = ''
                complete_path = False
                complete_ip = False
                os.kill(process.pid, signal.SIGINT)
                os.kill(process2().pid, signal.SIGINT)
                return "start2"
        if event.type == pygame.TEXTINPUT:
            if complete_ip is False:
                new_text_client += event.text
            elif complete_path is False:
                new_text_client_ += event.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if complete_ip is False:
                    try:
                        new_text_client = new_text_client[:-1]
                    except IndexError:
                        pass
                elif complete_path is False:
                    try:
                        new_text_client_ = new_text_client_[:-1]
                    except IndexError:
                        pass
            if event.key == pygame.K_RETURN:
                if complete_ip is False and len(new_text_client) > 0 or complete_ip is False and come_from_server:
                    complete_ip = True
                    complete_path = False
                    new_text_client = "127.0.0.1"
                elif complete_path is False and len(new_text_client_) > 0:
                    complete_path = True
    text_width_2 = smallfont_4.size(new_text_client_)[0]
    if text_width_2 <= 990 and complete_path is False:
        path_text = new_text_client_
    text_width2 = smallfont_4.size(new_text_client)[0]
    if text_width2 <= 990 and complete_ip is False:
        ip_text = new_text_client
    text_5 = smallfont_4.render(path_text, True, color)
    text_rect_ = text_5.get_rect(topleft=(password_box_2.rect.x + 5, password_box_2.rect.y + 5))
    if text_rect_.w <= 990:
        screen.blit(text_5, (password_box_2.rect.x + 5, password_box_2.rect.y + 8))
    text_1 = smallfont_4.render(ip_text, True, color)
    text_rect = text_1.get_rect(topleft=(username_box_2.rect.x + 5, username_box_2.rect.y + 5))
    if text_rect.w <= 990:
        screen.blit(text_1, (username_box_2.rect.x + 5, username_box_2.rect.y + 8))
    os.chdir(r"C:\Users\user\Desktop\red hut camp")
    venv_python = r".venv\rose\Scripts\activate"
    subprocess.run(
        f'cmd /c "{venv_python} && echo Activation successful && set"',
        cwd=r"C:\Users\user\Desktop\red hut camp",
        capture_output=True,
        text=True,
        shell=True
    )

    os.chdir(r"C:\Users\user\Desktop\red hut camp\ROSE")
    process2()

    if come_from_server:
        return "connect client come from start server"
    else:
        return "connect client"


# Main game loop
running = True
current_screen = "start"
global kill
kil = 0
while running:
    global process
    global kill
    # if kil == 0:
    #     kill += 1
    if current_screen == "start":
        current_screen = start_screen()
    elif current_screen == "log in":
        current_screen = log_in_screen()
    elif current_screen == "sign up":
        current_screen = sign_up_screen()
    elif current_screen == "start2":
        current_screen = start_screen_2()
    elif current_screen == "quit":
        # kill = 0
        running = False
    elif current_screen == "open server":
        current_screen = open_server()
    elif current_screen == "connect client":
        current_screen = connect_client(False)
    elif current_screen == "connect client come from start server":
        current_screen = connect_client(True)
    pygame.display.update()
pygame.quit()
# Import necessary modules and packages
from kivymd.app import MDApp
from kivy.lang import Builder
from plyer import filechooser
from obs import ObsClient, CorsRule, Options
from datetime import datetime 
from PIL import Image
import os
from kivy.uix.image import AsyncImage
import io
from io import BytesIO
from kivy.uix.button import Button
import numpy as np
import random
from kivy.clock import Clock
from kivymd.uix.button import MDRectangleFlatButton
import uuid
import shutil

# Huawei Cloud OBS (Object Storage Service) access keys and bucket name
endpoint = "http://obs.eu-west-101.myhuaweicloud.eu"
server="obs.eu-west-101.myhuaweicloud.eu"
access_key = "JAKGEFBQBLHWUNWWGIGI" #inserting hardcoded user access_key and secret_key for checking purposes
secret_key = "3lRysHwqAlRnw7kVFSWRCZFuIbdHau6UYHfzObz3"
bucket_name = "clothes"

# Create an OBS client object with the access keys and server URL
obsClient = ObsClient(access_key_id=access_key, secret_access_key=secret_key, server='obs.eu-west-101.myhuaweicloud.eu')

# Kivy language string that describes the user interface
KV="""

MDFloatLayout:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
    MDCard:
        size_hint: .45, .8
        pos_hint: {"center_x": .5, "center_y": .5}
        Carousel:
            id: slide
            MDFloatLayout:
                MDTextField:
                    id: username
                    hint_text: "Username"
                    size_hint_x: .8
                    pos_hint: {"center_x": .5, "center_y": .48}
                MDTextField:
                    id: password
                    hint_text: "Password"
                    size_hint_x: .8
                    pos_hint: {"center_x": .5, "center_y": .36}
                    password: True
                MDRaisedButton:
                    text: "REGISTER"
                    size_hint_x: .39
                    pos_hint: {"center_x": .3, "center_y": .2}
                    on_release: app.register()
                MDRaisedButton:
                    text: "LOGIN"
                    size_hint_x: .39
                    pos_hint: {"center_x": .7, "center_y": .2}
                    on_release: app.login()     
            MDFloatLayout:
                MDLabel:
                    text: "What is the predominant color?"
                    bold: True
                    halign: "center"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    font_style: "H4"
                MDRaisedButton:
                    text: "Black"
                    size_hint_x: .20
                    pos_hint: {"center_x": .2, "center_y": .3}
                    md_bg_color: 0, 0, 0, 1
                    on_release: app.next1(self.text)
                MDRaisedButton:
                    text: "White"
                    size_hint_x: .20
                    pos_hint: {"center_x": .50, "center_y": .3}
                    md_bg_color: 1, 1, 1, 1
                    text_color: 0, 0, 0, 1
                    on_release: app.next1(self.text)
                MDRaisedButton:
                    text: "Grey"
                    size_hint_x: .20
                    pos_hint: {"center_x": .80, "center_y": .3}
                    md_bg_color: 0.5, 0.5, 0.5, 1
                    text_color: 0, 0, 0, 1
                    on_release: app.next1(self.text)
                MDRaisedButton:
                    text: "Red"
                    size_hint_x: .20
                    pos_hint: {"center_x": .2, "center_y": .2}
                    md_bg_color: 1, 0, 0, 1
                    text_color: 0, 0, 0, 1
                    on_release: app.next1(self.text)
                MDRaisedButton:
                    text: "Blue"
                    size_hint_x: .20
                    pos_hint: {"center_x": .50, "center_y": .2}
                    md_bg_color: 0, 0, 1, 1
                    on_release: app.next1(self.text)
                MDRaisedButton:
                    text: "Green"
                    size_hint_x: .20
                    pos_hint: {"center_x": .80, "center_y": .2}
                    md_bg_color: 0, 1, 0, 1
                    text_color: 0, 0, 0, 1
                    on_release: app.next1(self.text)
                MDRaisedButton:
                    text: "Pink"
                    size_hint_x: .20
                    pos_hint: {"center_x": .2, "center_y": .1}
                    md_bg_color: 1, 0.75, 0.8, 1
                    text_color: 0, 0, 0, 1
                    on_release: app.next1(self.text)
                MDRaisedButton:
                    text: "Purple"
                    size_hint_x: .20
                    pos_hint: {"center_x": .50, "center_y": .1}
                    md_bg_color: 0.73, 0.16, 0.96, 1
                    text_color: 0, 0, 0, 1
                    on_release: app.next1(self.text)
                MDRaisedButton:
                    text: "Yellow"
                    size_hint_x: .20
                    pos_hint: {"center_x": .80, "center_y": .1}
                    md_bg_color: 1, 1, 0, 1
                    text_color: 0, 0, 0, 1
                    on_release: app.next1(self.text)

            MDFloatLayout:
                MDLabel:
                    text: "What clothing item do you want to upload?"
                    bold: True
                    halign: "center"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    font_style: "H4"
                MDRaisedButton:
                    text: "Sweater"
                    size_hint_x: .39
                    pos_hint: {"center_x": .3, "center_y": .3}
                    on_release: app.next2(self.text)
                MDRaisedButton:
                    text: "T-Shirt"
                    size_hint_x: .39
                    pos_hint: {"center_x": .7, "center_y": .3}
                    on_release: app.next2(self.text)
                MDRaisedButton:
                    text: "Trousers"
                    size_hint_x: .39
                    pos_hint: {"center_x": .3, "center_y": .2}
                    on_release: app.next2(self.text)
                MDRaisedButton:
                    text: "Shorts"
                    size_hint_x: .39
                    pos_hint: {"center_x": .7, "center_y": .2}
                    on_release: app.next2(self.text)
                MDRaisedButton:
                    text: "Skip"
                    size_hint_x: .20
                    pos_hint: {"center_x": .7, "center_y": .1}
                    on_release: app.skip()
                MDRaisedButton:
                    text: "Previous"
                    size_hint_x: .20
                    pos_hint: {"center_x": .3, "center_y": .1}
                    on_release: app.previous()
                
            MDFloatLayout:
                MDLabel:
                    text: "How is the temperature?"
                    bold: True
                    halign: "center"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    font_style: "H4"
                MDRaisedButton:
                    text: "Hot"
                    size_hint_x: .39
                    pos_hint: {"center_x": .5, "center_y": .3}
                    md_bg_color: 1, 0, 0, 1
                    on_release: app.next3(self.text)
                MDRaisedButton:
                    text: "Cold"
                    size_hint_x: .39
                    pos_hint: {"center_x": .5, "center_y": .2}
                    md_bg_color: 0, 0, 1, 1
                    on_release: app.next3(self.text)
                MDRaisedButton:
                    text: "Previous"
                    size_hint_x: .20
                    pos_hint: {"center_x": .5, "center_y": .1}
                    on_release: app.previous()
            MDFloatLayout:
                MDLabel:
                    text: "Here's your outfit"
                    bold: True
                    pos_hint: {"center_x": .6, "center_y": .6}
                    font_style: "H6"
                MDRaisedButton:
                    text: "Generate"
                    size_hint_x: .10
                    pos_hint: {"center_x": .7, "center_y": .6}
                    on_release: app.next4(self.text)
    MDLabel:
        text: "A Cloud Closet"
        bold: True
        pos_hint: {"center_x": .86, "center_y": .8}
        font_style: "H4"
        
    MDLabel:
        id: Name
        text: "Login"
        pos_hint: {"center_x": .790, "center_y": .7}
        font_style: "H6"
        theme_text_color: "Custom"
    MDIconButton:
        id:name
        icon: "numeric-1-circle"
        pos_hint: {"center_x": .32, "center_y": .65}
        user_font_size: "35sp"
        theme_text_color: "Custom"
    MDLabel:
        id: Color
        text: "Color"
        pos_hint: {"center_x": .870, "center_y": .7}
        font_style: "H6"
        theme_text_color: "Custom"
    MDIconButton:
        id: color
        icon: "numeric-2-circle"
        pos_hint: {"center_x": .41, "center_y": .65}
        user_font_size: "35sp"
        theme_text_color: "Custom"
    MDLabel:
        id: Upload
        text: "Choose"
        pos_hint: {"center_x": .950, "center_y": .7} 
        font_style: "H6"
        theme_text_color: "Custom"
    MDIconButton:
        id: upload
        icon: "numeric-3-circle"
        pos_hint: {"center_x": .5, "center_y": .65}
        user_font_size: "35sp"
        theme_text_color: "Custom"
    MDLabel:
        id: Submit
        text: "Upload"
        pos_hint: {"center_x": 1.055, "center_y": .7}
        font_style: "H6"
        theme_text_color: "Custom"
    MDIconButton:
        id: submit
        icon: "numeric-3-circle"
        pos_hint: {"center_x": .59, "center_y": .65}
        user_font_size: "35sp"
        theme_text_color: "Custom"
    MDLabel:
        id: Outfit
        text: "Outfit"
        pos_hint: {"center_x": 1.150, "center_y": .7}
        font_style: "H6"
        theme_text_color: "Custom"
    MDIconButton:
        id: outfit
        icon: "numeric-4-circle"
        pos_hint: {"center_x": .68, "center_y": .65}
        user_font_size: "35sp"
        theme_text_color: "Custom"

"""
# Create a dictionary of users and their passwords
users={"admin":"psw"}

#Create list of filepaths created when new outfit generated and delete all of them when app is closed
filepaths=[]

# Initialize variables for storing user choices
chosen_color=""
chosen_temperature=""

class ProjectApp(MDApp):
    # The main application class. MDApp is a class from KivyMD library.
    # It provides a framework for building mobile and desktop applications.
    # The class inherits from the MDApp class.

    def build(self):
        # This method is used to build the user interface.
        # It loads the KV file as a string and returns the root widget.

        kv = Builder.load_string(KV)
        return kv

    def register(self):
        # This method is called when the "Register" button is pressed.
        # It retrieves the username and password entered by the user and stores
        # them in a dictionary called "users".
        # The "users" dictionary is defined at the beginning of the code.
        # The username is the key, and the password is the value.
        # The dictionary is used to store user credentials.

        username = self.root.ids.username.text
        password = self.root.ids.password.text

        users[username]=password


    def login(self):
        # This method is called when the "Login" button is pressed.
        # It retrieves the username and password entered by the user and checks if they match a known user.
        # If the username and password are correct, the user is logged in and the next slide is loaded.
        # Otherwise, an error message is displayed.

        username = self.root.ids.username.text
        password = self.root.ids.password.text

        # Check if the username and password match a known user
        #if username == "admin" and password == "psw":
        if username in users and users[username]==password:
            print("Login successful!")
            self.root.ids.slide.load_next(mode="next")
        else:
            print("Login failed.")
            self.root.ids.password.error_message ='Incorrect username or password'
    
    def next1(self, color):
        # This method is called when a color is selected on the second slide.
        # It sets the global variable "chosen_color" to the selected color.

        global chosen_color
        chosen_color = str(color)
        self.root.ids.slide.load_next(mode="next")

        
    def next2(self, item):
        # This method is called when an item is selected on the third slide.
        # It opens a file chooser dialog box, allowing the user to select an image file.
        # Once a file is selected, it retrieves the file path and stores the image file in the cloud storage using the OBS SDK.
        # The image file is stored in the "clothes" bucket with a filename that includes the selected color and a timestamp.
        # The timestamp is used to ensure that the filename is unique.
        # Once the file is uploaded, it loads the next slide.

        file_name=filechooser.open_file(on_selection=self.selected)
        file_path=file_name[0]

        #Getting the current date and time
        dt = datetime.now()

        # getting the timestamp
        ts = datetime.timestamp(dt)
        
        obsClient.putFile('clothes',item +'/'+chosen_color+'_'+str(ts), file_path)
        self.root.ids.slide.load_next(mode="next")

    def selected(self, selection):
        # This method is called when an image file is selected in the file chooser dialog box.
        # It retrieves the selected file path and returns it.

        if selection:
            return selection[0]

    def next3(self, temperature):
        # This method is called when a temperature range is selected on the fourth slide.
        # It sets the global variable "chosen_temperature" to the selected temperature range.

        global chosen_temperature
        chosen_temperature = str(temperature)
        self.root.ids.slide.load_next(mode="next")
    
    def next4(self, text):
        # Clear all widgets currently in the slide layout
        self.root.ids.slide.clear_widgets()

         # Initialize an empty list and get a list of all objects in the 'outfits' bucket with the chosen_temperature prefix
        li=[]
        resp = obsClient.listObjects("outfits", chosen_temperature)
        for outfit in resp['body']['contents']:
            li.append(str(outfit))
        del li[0]

        # Choose a random object from the list and download it to a local file named "temp_outfit.jpeg"
        random_element = random.choice(li)

        # Download the random object to a local file named "temp_outfit.jpeg"
        # filename = "temp_outfit.jpeg"
        filename = f"{str(uuid.uuid4())}.jpeg"
        folder_name = "styles"
        local_path = os.path.abspath(os.path.join(folder_name, filename))
        filepaths.append(local_path)
        print(filepaths)

        res = obsClient.getObject("outfits", random_element ,local_path)
        
        # Create an AsyncImage widget with the downloaded image and add it to the slide layout
        image = AsyncImage(source=local_path, size_hint=(0.8, 0.8), pos_hint={"center_x": 0.5, "center_y": 0.3})
        self.root.ids.slide.add_widget(image)

        li=[]
        # Create a button widget and add it to the widget tree
        # Clock.schedule_once(lambda dt: self.root.ids.slide.clear_widgets(), 8)
        Clock.schedule_once(lambda dt: self.create_button(), 1)
        
    def create_button(self):
        # Create a button widget and add it to the widget tree
        button = MDRectangleFlatButton(text="Generate again", pos_hint={"center_x": 0.5, "center_y": 0.55}, md_bg_color=(0, 0.5, 1, 1), text_color=(1, 1, 1, 1))
        button.bind(on_press=self.next4)
        self.root.add_widget(button)
        
    
    def skip(self):
        # Move to the next slide using the 'load_next' method of the slide layout
        self.root.ids.slide.load_next(mode="next")

    def previous(self):
        # Move to the previous slide using the 'load_previous' method of the slide layout
        self.root.ids.slide.load_previous()
    
    def on_stop(self):
        # Delete the files when the app is stopped
        styles_dir = os.path.abspath("styles")
        shutil.rmtree(styles_dir)
# Create a ProjectApp instance and run the app
app = ProjectApp()
app.run()
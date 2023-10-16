from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
import cv2
import pytesseract
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from pdf2image import convert_from_path
from kivy.uix.modalview import ModalView


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        login_button = Button(text='Login')
        login_button.bind(on_release=self.login)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Login Page', size_hint=(None, None), size=(300, 50)))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if self.check_credentials(username, password):
            self.username_input.text = ''
            self.password_input.text = ''
            self.manager.current = 'home'
        else:
            self.display_message("Invalid credentials")

    def check_credentials(self, username, password):
        # Retrieve user data from the text file and check credentials
        with open('user_data.txt', 'r') as file:
            for line in file:
                stored_username, stored_password = line.strip().split(':')
                if username == stored_username and password == stored_password:
                    return True
        return False

    def display_message(self, message):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text=message))
        login_button = Button(text='Login')
        login_button.bind(on_release=self.login)
        layout.add_widget(login_button)
        self.add_widget(layout)

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        signup_button = Button(text='Sign Up')
        signup_button.bind(on_release=self.signup)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Signup Page', size_hint=(None, None), size=(300, 50)))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(signup_button)

        self.add_widget(layout)

    def signup(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        self.store_credentials(username, password)
        self.manager.current = 'login'

    def store_credentials(self, username, password):
        # Store user data in a text file
        with open('user_data.txt', 'a') as file:
            file.write(f'{username}:{password}\n')

class MenuButton(Button):
    pass

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(Label(text='Welcome to the Home Page', size_hint=(None, None), size=(300, 50)))
        self.add_widget(layout)

        self.username_label = Label(text="Username")
        layout.add_widget(self.username_label)

        recently_ordered_button = MenuButton(text="Recently Ordered Medicines")
        recently_ordered_button.bind(on_release=self.show_recently_ordered)
        layout.add_widget(recently_ordered_button)

        scan_prescriptions_button = MenuButton(text="Scan Prescriptions")
        scan_prescriptions_button.bind(on_release=self.scan_prescriptions)
        layout.add_widget(scan_prescriptions_button)
        
    def show_recently_ordered(self, instance):
        self.manager.current = 'recently_ordered'

    def scan_prescriptions(self, instance):
        self.manager.current = 'upload_prescription'

class RecentlyOrderedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Recently Ordered Medicines Page"))
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.filechooser import FileChooserListView
class CustomFileChooserIconView(FileChooserIconView):
    def is_hidden(self, filename):
        if filename.lower().endswith(('.sys', '.dll', '.tmp', '.ini')):
            return False
        return super(CustomFileChooserIconView, self).is_hidden(filename)

class CustomFileChooserListView(FileChooserListView):
    def is_hidden(self, filename):
        if filename.lower().endswith(('.sys', '.dll', '.tmp', '.ini')):
            return False
        return super(CustomFileChooserListView, self).is_hidden(filename)

from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooserIconView
  # Import the necessary class



class UploadPrescriptionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(Label(text='Upload Prescription', size_hint=(None, None), size=(300, 50)))
        
        # Create the file chooser and a button to open it
        self.file_chooser = FileChooserIconView()
        self.select_file_button = Button(text="Select File")
        self.select_file_button.bind(on_release=self.show_file_chooser)
        
        # Add widgets to the layout
        layout.add_widget(self.select_file_button)
        layout.add_widget(self.file_chooser)
        
        # Create a label to display the selected file
        self.selected_file_label = Label(text="Selected File: No file selected")
        layout.add_widget(self.selected_file_label)
        
        # Add a button to perform OCR and display the result
        self.scan_button = Button(text="Scan Prescription")
        self.scan_button.disabled = True
        self.scan_button.bind(on_release=self.scan_prescription)
        layout.add_widget(self.scan_button)
        
        self.add_widget(layout)

    def show_file_chooser(self, instance):
        file_chooser_view = ModalView(size=(0.9, 0.9))
        file_chooser = FileChooserIconView()
    
    # Create a callback function for the "Select" button
        def select_callback(instance):
            selected_file = file_chooser.selection and file_chooser.selection[0]
            if selected_file:
            # Process the selected image using OCR
                img = Image.open(selected_file)
                ocr_text = pytesseract.image_to_string(img)

            # Display OCR output on the screen
                ocr_label = Label(text=ocr_text)
                file_chooser_view.add_widget(ocr_label)

            # Save the OCR output to a text file with the current date as the filename
                current_date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                filename = f"OCR_Output_{current_date}.txt"
                with open(filename, "w") as text_file:
                    text_file.write(ocr_text)
        
        select_button = Button(text="Select")
        select_button.bind(on_release=select_callback)
    
        file_chooser_view.add_widget(file_chooser)
        file_chooser_view.add_widget(select_button)
        file_chooser_view.open()



    def scan_prescription(self, instance):
        if self.captured_image_path:
            # Perform OCR on the uploaded file
            prescription_text = self.perform_ocr(self.captured_image_path)
            if prescription_text:
                self.prescription_text.text = f'Prescription Text:\n{prescription_text}'
            else:
                self.prescription_text.text = 'OCR could not recognize text from the file'

    def select_file(self, selection):
        if selection:
            selected_file = selection[0]
            self.file_chooser_view.dismiss()  # Close the modal view
            self.selected_file_label.text = f"Selected File: {selected_file}"
            self.scan_button.disabled = False  # Enable the scan button
            self.captured_image_path = selected_file




class LoginSignupApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        recently_ordered_screen = RecentlyOrderedScreen(name='recently_ordered')
        sm.add_widget(recently_ordered_screen)
        upload_prescription_screen = UploadPrescriptionScreen(name='upload_prescription')
        sm.add_widget(upload_prescription_screen)
        return sm

if __name__ == '__main__':
    app = LoginSignupApp()
    app.run()

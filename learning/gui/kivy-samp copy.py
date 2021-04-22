import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
# from kivy.uix.widget import Widget


class MyGrid(GridLayout):
    # Hard Version: use the css type one .kv
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        self.cols = 1

        self.inputsLayout = GridLayout()
        self.inputsLayout.cols = 2

        self.fnameLabel = Label(text='First Name: ')
        self.inputsLayout.add_widget(self.fnameLabel)
        self.fname = TextInput(multiline=False)
        self.inputsLayout.add_widget(self.fname)

        self.inputsLayout.add_widget(Label(text='Last Name: '))
        self.lname = TextInput(multiline=False)
        self.inputsLayout.add_widget(self.lname)

        self.inputsLayout.add_widget(Label(text='Email: '))
        self.email = TextInput(multiline=False)
        self.inputsLayout.add_widget(self.email)

        self.add_widget(self.inputsLayout)

        self.buttonLayout = GridLayout()
        self.buttonLayout.cols = 1
        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.buttonLayout.add_widget(self.submit)

        self.add_widget(self.buttonLayout)

    def pressed(self, instance):
        fname = self.fname.text
        lname = self.lname.text
        email = self.email.text

        self.fnameLabel.text += " " + fname

        print(fname + lname + email)


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()

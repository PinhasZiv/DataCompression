import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.label import Label
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.bubble import Button
# from kivy.uix.widget import Widget
# from kivy.properties import ObjectProperty
#

# class MyGrid(Widget):
#     first = ObjectProperty(None)
#     last = ObjectProperty(None)
#
#     def btn(self):
#         print("First Name:", self.first.text, ", Last Name:", self.last.text)
#         self.first.text = ""
#         self.last.text = ""
#

class CompressorApp(App):

    def build(self):
        return FloatLayout()


if __name__ == "__main__":
    CompressorApp().run()
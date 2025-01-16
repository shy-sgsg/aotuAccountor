'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-16 16:40:01
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-16 16:40:41
FilePath: \autoAccountor\mobile_app\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.label = Label(text='Enter your message:')
        layout.add_widget(self.label)

        self.text_input = TextInput(multiline=False)
        layout.add_widget(self.text_input)

        self.button = Button(text='Submit')
        self.button.bind(on_press=self.on_button_press)
        layout.add_widget(self.button)

        self.result_label = Label(text='')
        layout.add_widget(self.result_label)

        return layout

    def on_button_press(self, instance):
        message = self.text_input.text
        self.result_label.text = f'You entered: {message}'
        # Here you can add the logic to process the message and send it to the server

if __name__ == '__main__':
    MainApp().run()

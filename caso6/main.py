import webbrowser
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class ChatbotApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

# Botón para abrir el chatbot en el navegador
        open_button = Button(text="Abrir Chatbot", size_hint=(1, 0.1))
        open_button.bind(on_press=self.open_chatbot)
        layout.add_widget(open_button)
        return layout

    def open_chatbot(self, instance):


# Abre el chatbot en el navegador predeterminado
# webbrowser.open("https://widget.kommunicate.io/chat")
        webbrowser.open("https://widget.kommunicate.io/chat?appId=1ef0018ec23321811284bcdb1b4194c87")


if __name__ == '__main__':
    ChatbotApp().run()

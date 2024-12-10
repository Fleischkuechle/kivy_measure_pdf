from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window


class MouseFollowApp(App):
    def build(self):
        self.layout = FloatLayout()
        self.label = Label(
            text="I follow the mouse!", size_hint=(None, None), size=(200, 50)
        )
        self.layout.add_widget(self.label)
        Window.bind(mouse_pos=self.on_mouse_move)
        return self.layout

    def on_mouse_move(self, window, pos):
        # Update label position to follow the mouse
        self.label.pos = (pos[0] - self.label.width / 2, pos[1] - self.label.height / 2)


if __name__ == "__main__":
    MouseFollowApp().run()

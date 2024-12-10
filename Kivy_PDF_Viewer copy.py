import fitz  # PyMuPDF
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Line


class PDFViewer(FloatLayout):
    def __init__(self, pdf_path, **kwargs):
        super().__init__(**kwargs)
        self.pdf_document = fitz.open(pdf_path)
        self.current_page = 0
        self.image_widget = Image()
        self.add_widget(self.image_widget)
        self.load_page()

        self.points = []
        self.bind(on_touch_down=self.on_touch_down)

    def load_page(self):
        page = self.pdf_document[self.current_page]
        pix = page.get_pixmap()
        self.image_widget.texture = self.create_texture(pix)
        self.image_widget.size = (pix.width, pix.height)
        self.image_widget.size_hint = None, None

    def create_texture(self, pix):
        from kivy.graphics.texture import Texture

        texture = Texture.create(size=(pix.width, pix.height))
        texture.blit_buffer(pix.samples, colorfmt="rgb", bufferfmt="ubyte")
        return texture

    def on_touch_down(self, touch):
        if self.image_widget.collide_point(touch.x, touch.y):
            self.points.append((touch.x, touch.y))
            if len(self.points) == 2:
                self.measure_distance()
                self.points = []  # Reset points after measuring

            with self.canvas:
                Color(1, 0, 0, 1)  # Red color for the line
                Line(points=[touch.x, touch.y, touch.x, touch.y], width=2)

    def measure_distance(self):
        p1, p2 = self.points
        distance = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
        print(f"Distance: {distance:.2f} pixels")


class PDFApp(App):
    def build(self):
        pdf_path: str = r"D:\11\02\13\pdf_utils\outputs\Draw_Wallet_test.pdf"
        pdf_viewer: PDFViewer = PDFViewer(pdf_path=pdf_path)
        return pdf_viewer


if __name__ == "__main__":
    PDFApp().run()

import fitz  # PyMuPDF
from kivy.app import App
from kivy.modules import screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Line, Ellipse, Canvas
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.core.window import Window
import fitz  # PyMuPDF
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image


# class PDFViewer(FloatLayout):
class PDFViewer(GridLayout):

    # def build(self):
    #     # Create a ScrollView
    #     scroll_view = ScrollView()
    #     layout = GridLayout(cols=1, size_hint_y=None)
    #     layout.bind(minimum_height=layout.setter("height"))

    #     # Open the PDF file
    #     pdf_document = fitz.open("your_pdf_file.pdf")

    #     # Load each page as an image and add it to the layout
    #     for page_number in range(len(pdf_document)):
    #         page = pdf_document.load_page(page_number)
    #         pix = page.get_pixmap()  # Render page to an image
    #         img = Image(texture=pix.tobytes())  # Convert image to texture
    #         layout.add_widget(img)

    #     scroll_view.add_widget(layout)
    #     return scroll_view

    def __init__(self, pdf_path, **kwargs):
        super().__init__(**kwargs)
        self.scroll_view = ScrollView()
        # self. = GridLayout(cols=1, size_hint_y=None)
        self.bind(minimum_height=self.setter("height"))
        self.label = Label(
            text="Hello",
            # size_hint=(0, 0.2),
            size=(200, 50),
        )
        self.label.color = (0, 0, 0, 1)  # black
        Window.bind(mouse_pos=self.on_mouse_move)
        self.add_widget(self.label)

        self.pdf_document = fitz.open(pdf_path)
        # Load each page as an image and add it to the layout
        for page_number in range(len(self.pdf_document)):
            image_widget: Image
            page, image_widget = self.load_page(page_number)
            # pix = page.get_pixmap()  # Render page to an image
            # img = Image(texture=pix.tobytes())  # Convert image to texture
            self.add_widget(image_widget)

        self.scroll_view.add_widget(self)
        # self.current_page: int = 0
        self.image_widget: Image = Image()
        # self.add_widget(self.image_widget)
        # self.page: fitz.Page = self.load_page()
        # self.horizontal_DPI: float = 0
        # self.vertical_DPI: float = 0
        # self.width_in_millimeters: float = 0
        # self.height_in_millimeters: float = 0
        # (
        #     self.horizontal_DPI,
        #     self.vertical_DPI,
        #     self.width_in_millimeters,
        #     self.height_in_millimeters,
        # ) = self.get_pdf_dpi_and_mm(page=self.page)

        self.points = []

    def load_page(self, page_number: int = 0) -> tuple[fitz.Page, Image]:
        """
        Loads the specified page from the PDF document and displays it in the image widget.

        This method retrieves the current page from the PDF document, converts it to a pixmap,
        and then sets the texture and size of the image widget to display the page content.
        """
        page: fitz.Page = self.pdf_document[page_number]  # Retrieve the current page
        # page.rect  # You can use this to access the page's rectangle if needed

        pix: fitz.Pixmap = page.get_pixmap()  # Convert the page to a pixmap
        image_widget: Image = Image()
        image_widget.texture = self.create_texture(
            pix
        )  # Set the image widget's texture
        image_widget.size = (pix.width, pix.height)  # Set the image widget's size
        image_widget.size_hint = (
            None,
            None,
        )  # Disable size hints for manual control
        return page, image_widget

    def create_texture(self, pix: fitz.Pixmap):
        """
        Creates a Kivy texture from a PyMuPDF Pixmap, flipping it vertically.

        This method converts a PyMuPDF Pixmap object into a Kivy Texture.
        It also flips the texture vertically to match the standard Kivy coordinate system.
        """
        texture: Texture = Texture.create(size=(pix.width, pix.height))
        texture.blit_buffer(pix.samples, colorfmt="rgb", bufferfmt="ubyte")
        # Flip the texture vertically
        texture.flip_vertical()
        return texture

    def on_mouse_move(self, window, pos):
        # Update label position to follow the mouse
        center_position: tuple[float, float] = (
            pos[0] - self.label.width / 2,
            pos[1] - self.label.height / 2,
        )
        center_below_mouse_position: tuple[float, float] = (
            pos[0] - self.label.width / 2 - 10,
            pos[1] - self.label.height / 2 - 70,
        )
        # self.label.pos = center_position  # (pos[0] - self.label.width / 2, pos[1] - self.label.height / 2)
        self.label.pos = center_below_mouse_position

    def draw_red_point(
        self,
        canvas: Canvas,
        position: tuple[int, int] = (100, 100),
        size: tuple[int, int] = (5, 5),
    ) -> None:
        """Draws a red point (small ellipse) on the canvas.

        Args:
            canvas: The canvas object to draw on.
            position: A tuple representing the x, y coordinates of the point's center. Defaults to (100, 100).
            size: A tuple representing the width and height of the point. Defaults to (10, 10).
        """
        with canvas:
            Color(1, 0, 0)  # RGB for red
            self.point = Ellipse(
                pos=(position[0] - size[0] / 2, position[1] - size[1] / 2), size=size
            )

    def remove_last_drawing(self):
        """Removes the last drawn line and point from the canvas."""
        if len(self.canvas.children) > 3:
            # Remove the last instruction (usually the line)
            self.canvas.remove(self.canvas.children[-1])
            # Remove the second-to-last instruction (usually the point)
            self.canvas.remove(self.canvas.children[-1])
            self.canvas.remove(self.canvas.children[-1])

    def on_touch_down(self, touch):
        # Check if the touch event is from a mouse and if it's a scroll event
        if touch.is_mouse_scrolling:
            return False  # Ignore mouse scroll events

        if self.image_widget.collide_point(touch.x, touch.y):
            self.points.append((touch.x, touch.y))
            if len(self.points) == 2:
                self.measure_distance()

                with self.canvas:
                    # Color(1, 0, 0, 1)  # Red color for the line
                    Color(0, 0, 1, 1)  # blue color for the line
                    # Line(points=[touch.x, touch.y, touch.x, touch.y], width=2)
                    Line(points=self.points, width=2)

                    return super().on_touch_down(
                        touch
                    )  # Ensure other touch events are handled
            if len(self.points) == 3:
                self.remove_last_drawing()
                self.points = []  # Reset points after measuring
                self.points.append((touch.x, touch.y))
            if len(self.points) == 1:
                self.draw_red_point(
                    canvas=self.canvas,
                    position=(self.points[0]),
                )
        return super().on_touch_down(touch)  # Ensure other touch events are handled

    def measure_distance(self):
        """
        Measures the distance between two points in pixels, DPI, millimeters, and inches.

        This method calculates the Euclidean distance between two points provided in the `self.points` attribute.
        It then converts the pixel distance to DPI, millimeters, and inches based on the page's DPI.
        """
        p1: tuple[float, float] = self.points[0]  # First point (x, y) in pixels
        p2: tuple[float, float] = self.points[1]  # Second point (x, y) in pixels

        # Calculate the Euclidean distance in pixels
        distance_pixels: float = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

        # Get the page's DPI
        page: fitz.Page = self.pdf_document[self.current_page]
        pix: fitz.Pixmap = page.get_pixmap()
        dpi_x: float = pix.xres  # Horizontal DPI
        dpi_y: float = pix.yres  # Vertical DPI

        # Convert pixels to DPI
        distance_dpi: float = distance_pixels / (dpi_x / 72)

        # Convert pixels to millimeters
        distance_mm: float = distance_pixels * 0.352777  # 1 pixel = 0.352777 mm

        # Convert pixels to inches
        distance_inch: float = (
            distance_pixels / (dpi_x / 72) * 0.0393701
        )  # 1 inch = 25.4 mm

        # Print the distances in different units
        print("-" * 30)
        print(f"Distance: {distance_pixels:.2f} pixels")
        print(f"Distance: {distance_dpi:.2f} DPI")
        print(f"Distance: {distance_mm:.2f} mm")
        print(f"Distance: {distance_inch:.2f} inches")
        # Update the label with the measured distance
        # self.label.text = f"Distance: {distance_pixels:.2f} pixels"
        # Update the label with all distances
        self.label.text = (
            f"Distance: \n"
            f"{distance_mm:.2f} mm\n"
            f"{distance_inch:.2f} inches\n"
            f"{distance_pixels:.2f} pixels\n"
            f"{distance_dpi:.2f} DPI\n"
        )

    def get_pdf_dpi_and_mm(self, page: fitz.Page) -> tuple[float, float, float, float]:
        """
        Retrieves the DPI (dots per inch) and dimensions in millimeters of a PDF file.

        Args:
            page (fitz.Page): a page of an pdf loaded with fritz.

        Returns:
            tuple[float, float, float, float]: A tuple containing the horizontal DPI, vertical DPI,
                                                width in millimeters, and height in millimeters.

        Example usage:
            dpi_x, dpi_y, width_mm, height_mm = get_pdf_dpi_and_mm("example.pdf")
            print(f"DPI: {dpi_x} x {dpi_y}")
            print(f"Width: {width_mm} mm, Height: {height_mm} mm")

        """

        # Get the page's dimensions in points
        rect: fitz.Rect = page.rect
        width_points: float = rect.width  # Width in points
        height_points: float = rect.height  # Height in points

        # Convert points to inches (1 point = 1/72 inch)
        width_inches: float = width_points / 72
        height_inches: float = height_points / 72
        # Calculate DPI (assuming the page is in a standard 8.5x11 inch format)
        dpi_x: float = width_points / width_inches  # Horizontal DPI
        dpi_y: float = height_points / height_inches  # Vertical DPI

        # Convert points to millimeters (1 point = 0.352777 mm)
        width_mm: float = round(width_points * 0.352777, 1)
        height_mm: float = round(height_points * 0.352777, 1)

        return (dpi_x, dpi_y, width_mm, height_mm)


class PDFApp(App):
    def build(self):
        pdf_path: str = r"D:\11\02\14\kivy_measure_pdf\eosc300mk3-500mk2-im13-en.pdf"
        # pdf_path: str = r"D:\11\02\13\pdf_utils\outputs\Draw_Wallet_test.pdf"
        pdf_viewer: PDFViewer = PDFViewer(pdf_path=pdf_path)
        return pdf_viewer


if __name__ == "__main__":
    PDFApp().run()

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Rectangle


class MyWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points = []
        self.label = Label(
            text="hello", size_hint=(None, None), pos_hint={"x": 0, "y": 0}
        )
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        # Check if the touch event is from a mouse and if it's a scroll event
        if touch.is_mouse_scrolling:
            return False  # Ignore mouse scroll events

        if self.collide_point(touch.x, touch.y):
            self.points.append((touch.x, touch.y))
            if len(self.points) == 2:
                self.measure_distance()

                with self.canvas:
                    Color(0, 0, 1, 1)  # blue color for the line
                    Line(points=self.points, width=2)
                    self.points = []  # Reset points after measuring
                    return super().on_touch_down(touch)
            self.draw_red_point(
                canvas=self.canvas,
                position=(self.points[0]),
            )
        return super().on_touch_down(touch)

    def on_mouse_move(self, touch):
        if len(self.points) == 1:
            self.label.pos = (touch.x, touch.y)
            self.label.text = (
                f"Distance: {self.calculate_distance(touch.x, touch.y):.2f} pixels"
            )

    def measure_distance(self):
        """
        Measures the distance between two points in pixels, DPI, and millimeters.
        """
        p1: tuple[float, float] = self.points[0]  # First point (x, y) in pixels
        p2: tuple[float, float] = self.points[1]  # Second point (x, y) in pixels

        # Calculate the Euclidean distance in pixels
        distance_pixels: float = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

        # Get the page's DPI
        # ... (Your code to get DPI from the PDF)

        # Convert pixels to DPI
        # ... (Your code to convert pixels to DPI)

        # Convert pixels to millimeters
        # ... (Your code to convert pixels to millimeters)

        # Convert pixels to inches
        distance_inch: float = (
            distance_pixels / (dpi_x / 72) * 0.0393701
        )  # 1 inch = 25.4 mm

        # Print the distances in different units
        print(f"Distance: {distance_pixels:.2f} pixels")
        print(f"Distance: {distance_dpi:.2f} DPI")
        print(f"Distance: {distance_mm:.2f} mm")
        print(f"Distance: {distance_inch:.2f} inches")

        # Update the label with the measured distance
        self.label.text = f"Distance: {distance_pixels:.2f} pixels"

    def calculate_distance(self, x2, y2):
        """Calculates the distance between the first point and the current mouse position."""
        x1, y1 = self.points[0]
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def draw_red_point(self, canvas, position):
        with canvas:
            Color(1, 0, 0, 1)  # Red color for the point
            Rectangle(pos=position, size=(5, 5))


class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == "__main__":
    MyApp().run()

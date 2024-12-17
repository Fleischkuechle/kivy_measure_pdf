import os
import fitz  # PyMuPDF


class PDF_Helper:
    def __init__(
        self,
    ):
        self.pdf_document: fitz.Document = None
        self.current_page: int = 0
        self.pages_count: int = 0
        self.horizontal_DPI: float = 0
        self.vertical_DPI: float = 0
        self.width_in_millimeters: float = 0
        self.height_in_millimeters: float = 0
        self.page: fitz.Page = None
        if self.pdf_document != None:
            self.update_pdf()

    def update_pdf(
        self,
    ):
        if self.pdf_document != None:
            self.pages_count: int = len(self.pdf_document)

            self.page = self.get_current_page()
            (
                self.horizontal_DPI,
                self.vertical_DPI,
                self.width_in_millimeters,
                self.height_in_millimeters,
            ) = self.get_pdf_dpi_and_mm(page=self.page)

    def next_page(self) -> fitz.Page:
        # Logic to change the PDF page
        if self.current_page < self.pages_count - 1:
            self.current_page += 1
        elif self.current_page == self.pages_count - 1:
            self.current_page = 0
        # print(f"Changed to page: {self.current_page}")
        self.page: fitz.Page = self.get_current_page()
        return self.page

    def previous_page(self) -> fitz.Page:
        # Logic to change the PDF page
        if self.current_page <= self.pages_count and self.current_page != 0:
            self.current_page -= 1
        elif self.current_page == 0:
            self.current_page = self.pages_count - 1
        # print(f"Changed to page: {self.current_page}")
        self.page: fitz.Page = self.get_current_page()
        return self.page

    def get_current_page(self) -> fitz.Page:
        """
        Loads the current page from the PDF document and displays it in the image widget.

        This method retrieves the current page from the PDF document, converts it to a pixmap,
        and then sets the texture and size of the image widget to display the page content.
        """
        page: fitz.Page = self.pdf_document[self.current_page]

        return page

    def get_current_pixmap(self) -> fitz.Pixmap:
        # page: fitz.Page = self.get_current_page()
        pix_map: fitz.Pixmap = self.page.get_pixmap()  # Convert the page to a pixmap
        return pix_map

    def measure_distance(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
    ) -> tuple[float, float, float]:
        """
        Measures the distance between two points in pixels, DPI, millimeters, and inches.

        This method calculates the Euclidean distance between two points provided in the `self.points` attribute.
        It then converts the pixel distance to DPI, millimeters, and inches based on the page's DPI.
        """

        # Calculate the Euclidean distance in pixels
        distance_pixels: float = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

        # Convert pixels to millimeters
        distance_mm: float = distance_pixels * 0.352777  # 1 pixel = 0.352777 mm

        # Convert mm to inches
        distance_inch: float = distance_mm / 25.4  # 1 inch = 25.4 mm
        return distance_pixels, distance_mm, distance_inch

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

    def open_pdf(
        self,
        pdf_path: str,
    ) -> fitz.Document:
        self.pdf_document: fitz.Document = fitz.open(pdf_path)
        if self.pdf_document != None:
            self.update_pdf()
            # self.pages_count: int = len(self.pdf_document)
        return self.pdf_document


def test():
    pdf_helper: PDF_Helper = PDF_Helper()


if __name__ == "__main__":
    test()

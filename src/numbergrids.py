from docx import Document
from docx.shared import Inches
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from puzzle import PopulatedPuzzle, Puzzle


class Numbergrid(Puzzle):
    def __init__(self, grid_size_option: str, difficulty_option: str):
        super().__init__()
        self.subdomain = "numbergrids"
        self.grid_size_option = grid_size_option
        self.difficulty_option = difficulty_option

    def get_options_internal(self, driver: WebDriver, timeout: int):
        input_gs = driver.find_element_by_id("sg")  # Grid Sizes
        gs_options = {
            size: f"{size}x{size}"
            for size in input_gs.get_attribute("data-slider-values").split(",")
        }

        input_d = driver.find_element_by_id("sd")  # Difficulties
        d_options = {
            difficulty: [
                "Very Easy",
                "Moderate",
                "Challenging",
                "Difficult",
                "Fiendish",
            ][int(difficulty) - 1]
            for difficulty in input_d.get_attribute("data-slider-values").split(",")
        }

        return [("Grid Size", gs_options), ("Difficulty", d_options)]

    def select_options(self, driver: WebDriver, timeout: int):
        driver.execute_script(
            f"document.getElementById('sg').setAttribute('value', '{self.grid_size_option}')"
        )
        driver.execute_script(
            f"document.getElementById('sd').setAttribute('value', '{self.difficulty_option}')"
        )

    def get_populated_puzzle(self, driver: WebDriver, timeout: int):
        img_path = "tmp.png"

        board = (
            WebDriverWait(driver, timeout)
            .until(EC.presence_of_element_located((By.CLASS_NAME, "gridtable")))
            .find_element_by_tag_name("tbody")
        )
        board.screenshot(img_path)

        return PopulatedNumbergrid(img_path, self.grid_size_option)


class PopulatedNumbergrid(PopulatedPuzzle):
    def __init__(self, img: str, grid_size: str, heading_style: str = "Heading 2"):
        super().__init__(heading_style)
        self.img = img
        self.grid_size = grid_size

    def add_to_doc_internal(self, doc: Document):
        doc.add_picture(self.img, width=Inches(int(self.grid_size) / 5 + 2))

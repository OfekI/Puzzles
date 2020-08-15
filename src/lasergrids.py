from docx import Document
from docx.shared import Inches
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from puzzle import PopulatedPuzzle, Puzzle


class Lasergrid(Puzzle):
    def __init__(self, grid_size_option: str, difficulty_option: str):
        super().__init__()
        self.subdomain = "lasergrids"
        self.grid_size_option = grid_size_option
        self.difficulty_option = difficulty_option

    def get_options_internal(self, driver: WebDriver, timeout: int):
        select_gs = driver.find_element_by_name("sg")  # Grid Sizes
        gs_options = {
            option.get_attribute("value"): option.text
            for option in select_gs.find_elements_by_tag_name("option")
        }

        select_d = driver.find_element_by_name("sd")  # Difficulty
        d_options = {
            option.get_attribute("value"): option.text
            for option in select_d.find_elements_by_tag_name("option")
        }

        return [("Grid Size", gs_options), ("Difficulty", d_options)]

    def select_options(self, driver: WebDriver, timeout: int):
        select_gs = Select(driver.find_element_by_name("sg"))
        select_gs.select_by_value(self.grid_size_option)

        select_d = Select(driver.find_element_by_name("sd"))
        select_d.select_by_value(self.difficulty_option)

    def get_populated_puzzle(self, driver: WebDriver, timeout: int):
        img_path = "tmp.png"

        board = (
            WebDriverWait(driver, timeout)
            .until(EC.presence_of_element_located((By.ID, "lasergrid")))
            .find_element_by_tag_name("tbody")
        )
        board.screenshot(img_path)

        return PopulatedLasergrid(img_path, self.grid_size_option)


class PopulatedLasergrid(PopulatedPuzzle):
    def __init__(self, img: str, grid_size_option: str, heading_style="Heading 2"):
        super().__init__(heading_style)
        self.img = img
        self.grid_size = grid_size_option

    def add_to_doc_internal(self, doc: Document):
        doc.add_picture(self.img, width=Inches(3 if self.is_small() else 4))

    def is_small(self):
        return int(self.grid_size) < 3

from docx import Document
from docx.shared import Inches

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from puzzle import PopulatedPuzzle, Puzzle


class WordSearch(Puzzle):
    def __init__(self):
        super().__init__()
        self.subdomain = "wordsearch"
        self.has_options = False
        self.suffix = "?type=u"

    def get_populated_puzzle(self, driver: WebDriver, timeout: int):
        img_path = "tmp.png"

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "start"))
        ).click()
        board = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, "game"))
        )
        board.screenshot(img_path)
        return PopulatedWordSearch(img_path)


class PopulatedWordSearch(PopulatedPuzzle):
    def __init__(self, img: str, heading_style: str = "Heading 2"):
        super().__init__(heading_style)
        self.img = img

    def add_to_doc_internal(self, doc: Document):
        doc.add_picture(self.img, width=Inches(7))

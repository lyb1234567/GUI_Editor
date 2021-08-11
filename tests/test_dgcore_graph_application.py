import sys
import os
import time
import timeit
import itertools
import unittest
from pathlib import Path
from loguru import logger

CURRENT_FOLDER = Path(__file__).absolute().parent.parent
CURRENT_FOLDER_PATH = str(CURRENT_FOLDER)
sys.path.append(CURRENT_FOLDER_PATH)

# from directedgraph.dgcore import DirectedGraphApplication

logger.add(
    "logs/test_dgcore_graph_application.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


class TestDirectedGraphApplication(unittest.TestCase):
    """
    TestDirectedGraphApplication
    """

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @logger.catch
    def test_(self):
        pass


if __name__ == "__main__":
    unittest.main()

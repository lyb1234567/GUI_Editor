import sys
import unittest
from pathlib import Path
from loguru import logger

CURRENT_FOLDER = Path(__file__).absolute().parent.parent
CURRENT_FOLDER_PATH = str(CURRENT_FOLDER)
sys.path.append(CURRENT_FOLDER_PATH)

from directedgraph.dgcore import (
    GraphComponent,
    Node,
    SourceNode,
    GroundNode,
)

logger.add(
    "logs/test_dgcore_graphcomponent.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


class TestGraphComponent(unittest.TestCase):
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

    # @logger.catch
    def test_get(self):
        component1 = GraphComponent()
        self.assertEqual(vars(component1), component1.get())
        self.assertEqual(component1.get("name"), "Untitled")

    # @logger.catch
    def test_node_position(self):
        # node1 = Node(None, None, None, None, [1, 2])
        node1 = Node()
        node1.update_position([0, 9])
        self.assertEqual(node1.get("position"), [0, 9])

    # @logger.catch
    def test_groundnode_sourcenode(self):
        groundnode1 = GroundNode()
        self.assertEqual(groundnode1.get("user_defined_attribute"), "0")
        sourcenode1 = SourceNode(
            None, name="sourcenode1", position=[2, 3], user_defined_attribute="foo"
        )
        self.assertEqual(sourcenode1.get("user_defined_attribute"), "foo")

    # @logger.catch
    def test_node_arc(self):
        pass


if __name__ == "__main__":
    unittest.main()

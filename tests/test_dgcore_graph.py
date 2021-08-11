import sys
import os
import time
import itertools
import unittest
from pathlib import Path
from loguru import logger

CURRENT_FOLDER = Path(__file__).absolute().parent.parent
CURRENT_FOLDER_PATH = str(CURRENT_FOLDER)
sys.path.append(CURRENT_FOLDER_PATH)

from directedgraph.dgcore import (
    GraphComponent,
    Graph,
    Node,
    SourceNode,
    GroundNode,
    Arc,
)
from directedgraph.dgutils import FileManager

logger.add(
    "logs/test_dgcore_graph.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


class TestGraph(unittest.TestCase):
    """
    TestGraph
    """

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.file_name = "test_rc"
        self.file_extension = ".xml"
        self.path = Path(os.path.dirname(__file__)).joinpath(
            self.file_name + self.file_extension
        )

    def tearDown(self):
        pass

    # @logger.catch
    def test_get(self):
        """
        test_get
        """

        graph1 = Graph("graph1")
        graph1.create_component({"type": "Node", "name": "Node 1", "uid": "7778da"})
        graph1.create_component({"type": "Node", "name": "Node 2", "uid": "b911b2"})
        graph1.create_component(
            {
                "type": "Arc",
                "name": "Arc 1",
                "uid": "9a2812",
                "node1_uid": "7778da",
                "node2_uid": "b911b2",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            }
        )

        self.assertEqual(
            graph1.get(),
            (
                [{"name": "graph1"}],
                [
                    {
                        "type": "Node",
                        "uid": "7778da",
                        "name": "Node 1",
                        "colour": "#fd5455",
                        "position_x": "0",
                        "position_y": "0",
                    },
                    {
                        "type": "Node",
                        "uid": "b911b2",
                        "name": "Node 2",
                        "colour": "#fd5455",
                        "position_x": "0",
                        "position_y": "0",
                    },
                    {
                        "type": "Arc",
                        "uid": "9a2812",
                        "name": "Arc 1",
                        "colour": "#000000",
                        "node1_uid": "7778da",
                        "node2_uid": "b911b2",
                        "user_defined_attribute": "5",
                        "user_defined_arc_type": "Resistor",
                    },
                ],
            ),
        )

    # @logger.catch
    def test_create_component_without_uid(self):
        """
        test_id
        """

        graph1 = Graph("graph1")
        graph1.create_component({"type": "Node", "name": "Node without UID"})
        graph1.create_component({"type": "Node", "name": "Node 1", "uid": "7778da"})

        self.assertEqual(len(graph1.components), 2)

    # @logger.catch
    def test_insert_component(self):
        graph1 = Graph("graph1")

        node1 = Node(graph1, uid="b911b2", name="node1")
        graph1.insert_component(node1)
        node2 = Node(graph1, uid="9a2812", name="node2")
        graph1.insert_component(node2)

        self.assertEqual(len(graph1.components), 2)
        self.assertEqual(graph1.get_component("b911b2"), node1)
        self.assertEqual(graph1.get_component("b911b2").name, "node1")
        self.assertEqual(graph1.get_component("9a2812").connected_graph, graph1)

    # @logger.catch
    def test_create_component(self):
        graph1 = Graph("graph1")
        graph1.create_component(
            {
                "type": "Node",
                "uid": "7778da",
                "name": "node1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )

        self.assertEqual(graph1.get_component("7778da").name, "node1")
        self.assertIsInstance(graph1.get_component("7778da"), Node)

        graph1.create_component(
            {
                "type": "Node",
                "uid": "0a0a0b",
                "name": "node2",
                "colour": "#0000",
                "position_x": "400",
                "position_y": "500",
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "9a2812",
                "name": "Arc 1",
                "colour": "#0000",
                "node1_uid": "7778da",
                "node2_uid": "0a0a0b",
                "user_defined_attribute": None,
                "user_defined_arc_type": None,
            }
        )
        self.assertEqual(
            graph1.get_component("9a2812").get_position(), ([50, 50], [400, 500])
        )

    # @logger.catch
    def test_generate_component_uid(self):
        graph1 = Graph("graph1")
        graph1.create_component({"type": "Node", "name": "Node without UID 1"})
        graph1.create_component({"type": "Node", "name": "Node without UID 2"})
        graph1.create_component(
            {"type": "Node", "name": "Node with UID", "uid": "7778da"}
        )
        graph1.create_component(
            {"type": "Node", "name": "Node with duplicate UID", "uid": "7778da"}
        )

        self.assertEqual(len(graph1.components), 4)

    # @logger.catch
    def test_error(self):
        # graph1.create_component({"type": "Arc", "name": "Arc 1", "uid": "7778da"})
        # graph1.create_component({"name": "Fooo", "uid": "7778da"})
        pass

    # @logger.catch
    def test_query_and_delete(self):
        # print("---Init---")
        graph1 = Graph("graph1")
        graph1.create_component({"type": "Node", "name": "Node without UID 1"})
        graph1.create_component({"type": "Node", "name": "Node without UID 2"})
        graph1.create_component({"type": "Node", "name": "Foo", "uid": "7778da"})
        graph1.create_component({"type": "Node", "uid": "32a24b"})
        self.assertEqual(len(graph1.components), 4)

        # print("---Try Get Node---")
        self.assertEqual(graph1.get_component("7778da").name, "Foo")
        self.assertEqual(graph1.get_component("32a24b").name, "Untitled")

        # print("---Try Delete---")
        self.assertTrue(graph1.delete_component("32a24b"))
        self.assertFalse(graph1.delete_component("32a24b"))
        self.assertFalse(graph1.delete_component("31233"))
        self.assertEqual(len(graph1.components), 3)

    # @logger.catch
    def test_verify_graph_integrity(self):
        graph1 = Graph("graph1")
        graph1.create_component(
            {
                "type": "GroundNode",
                "uid": "7778da",
                "name": "GroundNode 1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )
        graph1.create_component(
            {
                "type": "GroundNode",
                "uid": "7778db",
                "name": "GroundNode 2",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )
        graph1.create_component(
            {
                "type": "SourceNode",
                "uid": "9a2812",
                "name": "SourceNode 1",
                "colour": "#0000",
                "position_x": "1000",
                "position_y": "500",
            }
        )
        graph1.create_component(
            {
                "type": "Node",
                "uid": "7778dc",
                "name": "Node 1",
                "colour": "#0000",
                "position_x": "50",
                "position_y": "50",
            }
        )
        graph1.create_component(
            {
                "type": "Node",
                "uid": "7778dd",
                "name": "Node 2",
                "colour": "#0000",
                "position_x": "400",
                "position_y": "500",
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "9a2813",
                "name": "Arc 1",
                "colour": "#0000",
                "node1_uid": "7778da",
                "node2_uid": "7778db",
                "user_defined_attribute": None,
                "user_defined_arc_type": None,
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "b7c567",
                "name": "Arc 2",
                "colour": "#0000",
                "node1_uid": "7778da",
                "node2_uid": "9a2812",
                "user_defined_attribute": None,
                "user_defined_arc_type": None,
            }
        )
        graph1.create_component(
            {
                "type": "Arc",
                "uid": "365bb9",
                "name": "Arc 3",
                "colour": "#0000",
                "node1_uid": "7778da",
                "node2_uid": "9a2812",
                "user_defined_attribute": None,
                "user_defined_arc_type": None,
            }
        )
        # graph1.print_graph_details()
        # print(graph1.get_component("9a2812943a39").get_position())
        self.assertEqual(
            graph1.verify_graph_integrity(),
            ["Only one Ground Node is allowed", "Source only allows single arcs"],
        )
        # print(graph1.verify_graph_integrity())
        # graph1.print_graph_details()
        # print(graph1.get_component("7778da0a0a0a").get())

    # @logger.catch
    def test_read_and_create_graph(self):
        fm = FileManager()
        path = Path(os.path.dirname(__file__)).joinpath("test_rc.xml")
        data1 = fm.create_graph_raw_data(str(path))
        graph1 = fm.create_graph(data1)

        # graph1.print_graph_details()
        graph1.verify_graph_integrity()
        # graph1.print_graph_details()

        self.assertEqual(len(graph1.get_component("1f9cb9").arcs), 2)  # N1 Arcs
        self.assertEqual(len(graph1.get_component("9cf405").arcs), 3)  # N2 Arcs
        self.assertEqual(len(graph1.get_component("59d632").arcs), 5)  # N4 Arcs
        self.assertEqual(len(graph1.get_component("567071").arcs), 3)  # N7 Arcs
        self.assertEqual(len(graph1.get_component("365bb9").arcs), 1)  # G1 Arcs
        # print("N1 Arcs:", len(graph1.get_component("1f9cb9").arcs))
        # print("N2 Arcs:", len(graph1.get_component("9cf405").arcs))
        # print("N4 Arcs:", len(graph1.get_component("59d632").arcs))
        # print("N7 Arcs:", len(graph1.get_component("567071").arcs))
        # print("G1 Arcs:", len(graph1.get_component("365bb9").arcs))

    # @logger.catch
    def test_read_and_create_graph_efficiency(self):
        start_time = time.time()
        for _ in itertools.repeat(None, 500):
            self.test_read_and_create_graph()
        end_time = time.time()
        print(
            "test_read_and_create_graph_efficiency() Elapsed time was %g seconds"
            % (end_time - start_time)
        )


if __name__ == "__main__":
    unittest.main()

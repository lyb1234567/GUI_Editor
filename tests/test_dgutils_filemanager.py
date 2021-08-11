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

from directedgraph.dgutils import FileManager

logger.add(
    "logs/test_dgutils_filemanager.py.log",
    level="DEBUG",
    format="{time:YYYY-MM-DD :mm:ss} - {level} - {file} - {line} - {message}",
    rotation="10 MB",
)
logger.info("Start Log")


class TestFileManager(unittest.TestCase):
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
    def test_open_graph(self):
        pass

    # @logger.catch
    def test_create_graph_raw_data(self):
        fm = FileManager()
        data1 = fm.create_graph_raw_data(str(self.path))
        list1 = [{"name": "My Graph"}]
        list2 = [
            {
                "type": "Node",
                "uid": "1f9cb9",
                "name": "N1",
                "colour": "#fd5455",
                "position_x": "300",
                "position_y": "100",
            },
            {
                "type": "Node",
                "uid": "9cf405",
                "name": "N2",
                "colour": "#fd5455",
                "position_x": "500",
                "position_y": "100",
            },
            {
                "type": "Node",
                "uid": "a129a9",
                "name": "N3",
                "colour": "#fd5455",
                "position_x": "1026.0",
                "position_y": "67.0",
            },
            {
                "type": "Node",
                "uid": "59d632",
                "name": "N4",
                "colour": "#fd5455",
                "position_x": "1011.0",
                "position_y": "387.0",
            },
            {
                "type": "Node",
                "uid": "8ad505",
                "name": "N5",
                "colour": "#fd5455",
                "position_x": "852.0",
                "position_y": "585.0",
            },
            {
                "type": "Node",
                "uid": "1d2386",
                "name": "N6",
                "colour": "#fd5455",
                "position_x": "175.0",
                "position_y": "342.0",
            },
            {
                "type": "Node",
                "uid": "567071",
                "name": "N7",
                "colour": "#fd5455",
                "position_x": "200.0",
                "position_y": "493.0",
            },
            {
                "type": "SourceNode",
                "uid": "14123f",
                "name": "S1",
                "colour": "#0f8080",
                "position_x": "100",
                "position_y": "100",
                "user_defined_attribute": "5",
            },
            {
                "type": "GroundNode",
                "uid": "365bb9",
                "name": "G1",
                "colour": "#d4aa01",
                "position_x": "179.0",
                "position_y": "632.0",
            },
            {
                "type": "Arc",
                "uid": "8665f0",
                "name": "A1",
                "colour": "#FFFFFF",
                "node1_uid": "14123f",
                "node2_uid": "1f9cb9",
                "user_defined_attribute": "None",
                "user_defined_arc_type": "None",
            },
            {
                "type": "Arc",
                "uid": "174404",
                "name": "C1",
                "colour": "#FFFFFF",
                "node1_uid": "59d632",
                "node2_uid": "1d2386",
                "user_defined_attribute": "10",
                "user_defined_arc_type": "Capacitor",
            },
            {
                "type": "Arc",
                "uid": "1c7ad3",
                "name": "C2",
                "colour": "#FFFFFF",
                "node1_uid": "1d2386",
                "node2_uid": "567071",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Capacitor",
            },
            {
                "type": "Arc",
                "uid": "2201bd",
                "name": "R1",
                "colour": "#FFFFFF",
                "node1_uid": "1f9cb9",
                "node2_uid": "9cf405",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "bd6295",
                "name": "R2",
                "colour": "#FFFFFF",
                "node1_uid": "9cf405",
                "node2_uid": "a129a9",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "a88df3",
                "name": "R3",
                "colour": "#FFFFFF",
                "node1_uid": "9cf405",
                "node2_uid": "a129a9",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "b081b6",
                "name": "R4",
                "colour": "#FFFFFF",
                "node1_uid": "a129a9",
                "node2_uid": "59d632",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "2f7002",
                "name": "R5",
                "colour": "#FFFFFF",
                "node1_uid": "a129a9",
                "node2_uid": "59d632",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "0dcb2f",
                "name": "R6",
                "colour": "#FFFFFF",
                "node1_uid": "a129a9",
                "node2_uid": "59d632",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "33ae52",
                "name": "R7",
                "colour": "#FFFFFF",
                "node1_uid": "59d632",
                "node2_uid": "8ad505",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "6bf56b",
                "name": "R8",
                "colour": "#FFFFFF",
                "node1_uid": "8ad505",
                "node2_uid": "567071",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
            {
                "type": "Arc",
                "uid": "ea40e5",
                "name": "R9",
                "colour": "#FFFFFF",
                "node1_uid": "567071",
                "node2_uid": "365bb9",
                "user_defined_attribute": "5",
                "user_defined_arc_type": "Resistor",
            },
        ]
        self.assertEqual(data1[0], list1)
        self.assertEqual(data1[1], list2)

        graph1 = fm.create_graph((list1, list2))
        self.assertEqual(data1[0], graph1.get()[0])

    # @logger.catch
    def test_create_graph(self):
        fm = FileManager()
        graph_attribute = [{"name": "graph1"}]
        graph_components = [
            {
                "type": "Node",
                "uid": "7778da",
                "name": "node1",
                "colour": "#FFFFFF",
                "position_x": "100",
                "position_y": "105",
            },
            {
                "type": "Node",
                "uid": "32a24b",
                "name": "node2",
                "colour": "#000000",
                "position_x": "30",
                "position_y": "30",
            },
            {
                "type": "Node",
                "uid": "9a2812943a39",
                "name": "node3",
            },
            {
                "type": "SourceNode",
                "uid": "b20350",
                "name": "sourcenode1",
                "colour": "#000000",
                "position_x": "40",
                "position_y": "40",
                "user_defined_attribute": "0",
            },
            {
                "type": "SourceNode",
                "uid": "e26c04",
                "name": "sourcenode2",
                "colour": "#000000",
                "position_x": "200",
                "position_y": "200",
                "user_defined_attribute": "Test",
            },
            {
                "type": "SourceNode",
                "uid": "3d8cc5",
                "name": "sourcenode3",
                "colour": "#000000",
                "position_x": "500",
                "position_y": "500",
                "user_defined_attribute": "Foo",
            },
            {
                "type": "GroundNode",
                "uid": "365bb9",
                "name": "groundnode",
            },
            {
                "type": "Arc",
                "uid": "b7c567",
                "name": "arc1",
                "node1": "365bb9",
                "node2": "3d8cc5",
            },
        ]
        graph_raw_data = (graph_attribute, graph_components)
        graph1 = fm.create_graph(graph_raw_data)
        self.assertEqual(graph1.name, "graph1")
        self.assertEqual(graph1.get_component("b7c567").name, "arc1")
        self.assertEqual(len(graph1.components), 8)

    # @logger.catch
    def test_export_graph_xml(self):
        pass
        # fm = FileManager()
        # graph1 = fm.open_graph(str(self.path))

        # path_output = Path(os.path.dirname(__file__)).joinpath(
        #     self.file_name + "_output" + self.file_extension
        # )
        # fm.export_graph_xml(str(path_output), graph1)


if __name__ == "__main__":
    unittest.main()

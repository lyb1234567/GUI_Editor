import sys
from pathlib import Path
from xml.dom import minidom

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))

from directedgraph.dgcore import Graph


class FileManager:
    def __init__(self):
        # self.link_filepath = None
        # self.link_graph = None
        pass

    # Internal

    def parse_attribute(self, component, temp, attributes):
        for attribute in attributes:
            try:
                temp[attribute] = (
                    component.getElementsByTagName(attribute)[0].childNodes[0].data
                )
            except IndexError:
                pass

    def create_graph_raw_data(self, filepath):
        dom1 = minidom.parse(filepath)
        graph_attribute = []
        graph_components = []
        type_list = ["Node", "SourceNode", "GroundNode", "Arc"]

        # Get Graph Name
        graph_name = (
            dom1.getElementsByTagName("Graph")[0]
            .getElementsByTagName("name")[0]
            .childNodes[0]
            .data
        )
        graph_attribute.append({"name": graph_name})

        # Get Graph components
        for component_type in type_list:
            components = dom1.getElementsByTagName(component_type)
            for component in components:
                temp = {"type": component_type, "uid": component.getAttribute("uid")}
                self.parse_attribute(component, temp, ["name", "colour"])

                if component_type == "Node":
                    self.parse_attribute(component, temp, ["position_x", "position_y"])

                elif component_type == "SourceNode":
                    self.parse_attribute(
                        component,
                        temp,
                        ["position_x", "position_y", "user_defined_attribute"],
                    )

                elif component_type == "GroundNode":
                    self.parse_attribute(component, temp, ["position_x", "position_y"])

                elif component_type == "Arc":
                    self.parse_attribute(
                        component,
                        temp,
                        [
                            "node1_uid",
                            "node2_uid",
                            "user_defined_attribute",
                            "user_defined_arc_type",
                        ],
                    )

                graph_components.append(temp)

        # Return Data as Tuple
        graph = (graph_attribute, graph_components)
        return graph

    def create_graph(self, graph_raw_data):
        # Creating Graph Instances
        new_graph = Graph(graph_raw_data[0][0].get("name"))

        # Inserting component instances into Graph
        for item in graph_raw_data[1]:
            if str(item.get("type")) is not "Arc":
                new_graph.create_component(item)
        for item in graph_raw_data[1]:
            if str(item.get("type")) is "Arc":
                new_graph.create_component(item)

        return new_graph

    # External

    def open_graph(self, filepath):
        new_graph = self.create_graph(self.create_graph_raw_data(filepath))
        return new_graph

    def export_graph_xml(self, filepath, import_graph):
        graph_raw_data = import_graph.get()
        graph_attribute = graph_raw_data[0]
        graph_components = graph_raw_data[1]

        doc = minidom.Document()
        directedgraph = doc.createElement("DirectedGraph")
        doc.appendChild(directedgraph)

        graph_node = doc.createElement("Graph")
        directedgraph.appendChild(graph_node)
        name = doc.createElement("name")
        graph_node.appendChild(name)
        graph_node_name = doc.createTextNode(graph_attribute[0]["name"])
        name.appendChild(graph_node_name)

        components_node = doc.createElement("Component")
        directedgraph.appendChild(components_node)

        for component in graph_components:
            component_node = doc.createElement(component["type"])
            component_node.setAttribute("uid", component["uid"])

            component_node_name = doc.createElement("name")
            component_node.appendChild(component_node_name)
            component_node_name_value = doc.createTextNode(component["name"])
            component_node_name.appendChild(component_node_name_value)

            component_node_colour = doc.createElement("colour")
            component_node.appendChild(component_node_colour)
            component_node_colour_value = doc.createTextNode(component["colour"])
            component_node_colour.appendChild(component_node_colour_value)

            if (
                component["type"] == "Node"
                or component["type"] == "GroundNode"
                or component["type"] == "SourceNode"
            ):
                component_node_position_x = doc.createElement("position_x")
                component_node.appendChild(component_node_position_x)
                component_node_position_x_value = doc.createTextNode(
                    component["position_x"]
                )
                component_node_position_x.appendChild(component_node_position_x_value)

                component_node_position_y = doc.createElement("position_y")
                component_node.appendChild(component_node_position_y)
                component_node_position_y_value = doc.createTextNode(
                    component["position_y"]
                )
                component_node_position_y.appendChild(component_node_position_y_value)

            if component["type"] == "SourceNode":
                component_node_user_defined_attribute = doc.createElement(
                    "user_defined_attribute"
                )
                component_node.appendChild(component_node_user_defined_attribute)
                component_node_user_defined_attribute_value = doc.createTextNode(
                    component["user_defined_attribute"]
                )
                component_node_user_defined_attribute.appendChild(
                    component_node_user_defined_attribute_value
                )

            if component["type"] == "Arc":
                component_node_node1_uid = doc.createElement("node1_uid")
                component_node.appendChild(component_node_node1_uid)
                component_node_node1_uid_value = doc.createTextNode(
                    component["node1_uid"]
                )
                component_node_node1_uid.appendChild(component_node_node1_uid_value)

                component_node_node2_uid = doc.createElement("node2_uid")
                component_node.appendChild(component_node_node2_uid)
                component_node_node2_uid_value = doc.createTextNode(
                    component["node2_uid"]
                )
                component_node_node2_uid.appendChild(component_node_node2_uid_value)

                component_node_user_defined_attribute = doc.createElement(
                    "user_defined_attribute"
                )
                component_node.appendChild(component_node_user_defined_attribute)
                component_node_user_defined_attribute_value = doc.createTextNode(
                    component["user_defined_attribute"]
                )
                component_node_user_defined_attribute.appendChild(
                    component_node_user_defined_attribute_value
                )

                component_node_user_defined_arc_type = doc.createElement(
                    "user_defined_arc_type"
                )
                component_node.appendChild(component_node_user_defined_arc_type)
                component_node_user_defined_arc_type_value = doc.createTextNode(
                    component["user_defined_arc_type"]
                )
                component_node_user_defined_arc_type.appendChild(
                    component_node_user_defined_arc_type_value
                )

            components_node.appendChild(component_node)

        f = open(filepath, "w")
        f.write(doc.toprettyxml(indent="    "))
        f.close()

    def export_graph_png(self, filepath, import_graph):
        pass

    def export_graph_pdf(self, filepath, import_graph):
        pass


if __name__ == "__main__":
    import unittest
    from tests import TestFileManager

    unittest.main()

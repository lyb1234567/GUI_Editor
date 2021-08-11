import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))

from directedgraph.dgcore import Node, SourceNode, GroundNode, Arc


class Graph:
    """
    init Graph()
    """

    def __init__(self, name=None):
        self.connected_window = None
        self.groundnode_counter = 0
        self.arc_counter = 0

        self.name = name if name else "Untitled"
        self.components = {}

    """
    Control Graph()
    """

    def get(self):
        """
        Pack all the data from Graph into Tuple.
        """

        graph_attribute = [{"name": self.name}]

        graph_components = []
        for component in self.components.values():
            if isinstance(component, Arc):
                component_dict = {
                    "type": "Arc",
                    "uid": str(component.uid),
                    "name": str(component.name),
                    "colour": str(component.colour),
                    "node1_uid": str(component.nodes[0].uid),
                    "node2_uid": str(component.nodes[1].uid),
                    "user_defined_attribute": str(component.user_defined_attribute),
                    "user_defined_arc_type": str(component.user_defined_arc_type),
                }
                graph_components.append(component_dict)
            elif isinstance(component, Node):
                component_dict = {
                    "type": "Node",
                    "uid": str(component.uid),
                    "name": str(component.name),
                    "colour": str(component.colour),
                    "position_x": str(component.position[0]),
                    "position_y": str(component.position[1]),
                }
                if isinstance(component, SourceNode):
                    component_dict["type"] = "SourceNode"
                    component_dict["user_defined_attribute"] = str(
                        component.user_defined_attribute
                    )
                if isinstance(component, GroundNode):
                    component_dict["type"] = "GroundNode"
                graph_components.append(component_dict)
            else:
                pass
        return graph_attribute, graph_components

    def get_name(self):
        """
        get_name
        """

        return self.name

    def update_name(self, name):
        """
        update_name
        """

        self.name = name

    def update_component_node_arcs(self):
        """
        update_component_node_arcs
        """

        self.arc_counter = 0
        components_values = self.components.values()

        for component_inst in components_values:
            if isinstance(component_inst, Node):
                component_inst.arcs.clear()

        for component_inst in components_values:
            if isinstance(component_inst, Arc):
                self.arc_counter += 1
                component_inst.nodes[0].arcs.append(component_inst)
                component_inst.nodes[1].arcs.append(component_inst)

    def verify_graph_integrity(self):
        """
        verify_graph_integrity
        """
        return_list = []
        return_list.clear()
        components_values = self.components.values()
        self.groundnode_counter = 0
        self.arc_counter = 0

        # Only one Ground Node is allowed
        for component_inst in components_values:
            if isinstance(component_inst, GroundNode):
                self.groundnode_counter += 1
        if self.groundnode_counter == 0:
            return_list.append("You need at least one GroundNode")
        elif self.groundnode_counter != 1:
            return_list.append("Only one Ground Node is allowed")
        else:
            pass

        # Source only allows single arcs
        self.update_component_node_arcs()

        for component_inst in components_values:
            if isinstance(component_inst, SourceNode):
                if len(component_inst.arcs) > 1:
                    return_list.append("Source only allows single arcs")

        if self.arc_counter > 50:
            return_list.append("Too many Arcs")

        return return_list

    """
    Control GraphComponent()
    """

    def get_component(self, uid):
        """
        get_component
        """

        # print(self.components[uid].get_name())
        # print("connected_graph:", self.components[uid].get_connected_graph())
        # print(vars(self.components[uid])) # 可以返回对象也可以返回字典
        return self.components[uid]

    def create_component(self, parameters):
        """
        create component according to the dictionary in the parameters
        """

        component_type = parameters.get("type", None)

        if component_type == "Node":
            component = Node(
                self,
                uid=parameters.get("uid", None),
                name=parameters.get("name", None),
                colour=parameters.get("colour", None),
                position=[
                    int(float(parameters.get("position_x", 0))),
                    int(float(parameters.get("position_y", 0))),
                ],
            )
            self.insert_component(component)
            return component
        elif component_type == "SourceNode":
            component = SourceNode(
                self,
                uid=parameters.get("uid", None),
                name=parameters.get("name", None),
                colour=parameters.get("colour", None),
                position=[
                    int(float(parameters.get("position_x", 0))),
                    int(float(parameters.get("position_y", 0))),
                ],
                user_defined_attribute=parameters.get("user_defined_attribute", None),
            )
            self.insert_component(component)
            return component
        elif component_type == "GroundNode":
            component = GroundNode(
                self,
                uid=parameters.get("uid", None),
                name=parameters.get("name", None),
                colour=parameters.get("colour", None),
                position=[
                    int(float(parameters.get("position_x", 0))),
                    int(float(parameters.get("position_y", 0))),
                ],
            )
            self.insert_component(component)
            return component
        elif component_type == "Arc":
            component = Arc(
                self,
                uid=parameters.get("uid", None),
                name=parameters.get("name", None),
                colour=parameters.get("colour", None),
                node1_uid=parameters.get("node1_uid", None),
                node2_uid=parameters.get("node2_uid", None),
                user_defined_attribute=parameters.get("user_defined_attribute", None),
                user_defined_arc_type=parameters.get("user_defined_arc_type", None),
            )
            self.insert_component(component)
            return component
        else:
            print("Error: Component Type")
            return False

    def insert_component(self, component):
        """
        insert_component
        """

        self.components[component.get_uid()] = component

    def update_component_name(self, uid, name):
        """
        update_component_name
        """

        self.components[uid].name = name

    def update_component_colour(self, uid, colour):
        """
        update_component_colour
        """

        self.components[uid].colour = colour

    # def update_arc_position(uid, uid, uid):
    # def update_arc_position(uid, node1, node2):
    # def update_arc_position(arc1, node1, node2):
    def update_arc_position(self, arc1, node1, node2):
        """
        update_arc_position
        """

        if isinstance(arc1, Arc):
            arc1.update_position(node1, node2)
        elif isinstance(arc1, str):
            if len(node2) == 12 and node2.connected_graph == self:
                self.get_component("arc1").update_position(node1, node2)

    def delete_component(self, uid):
        """
        Query and delete components using uid
        """

        if uid in self.components:
            self.components.pop(uid)
            return True
        else:
            return False

    """
    For debugging Graph
    """

    def print_graph_details(self):
        """
        Print UID|Name
        """

        print("------------------------------------")
        print("Graph vars(self):")
        print(vars(self))
        print("------------------------------------")
        print("Graph Components:")
        for component in self.components.values():
            print(
                "UID:",
                component.uid,
                "|",
                "Name:",
                component.name,
            )


if __name__ == "__main__":
    import unittest
    from tests import TestGraph  # Import test

    unittest.main()  # Run Unit tests

import uuid
import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))

UID_LENGTH = 6


class GraphComponent:
    """
    GraphComponent()
    """

    def __init__(self, connected_graph=None, **kwargs):
        self.connected_graph = connected_graph if connected_graph else None
        self.connected_window = None
        self.connected_gui = None

        self.uid = None
        self.generate_uid(kwargs.get("uid", None))
        self.name = kwargs["name"] if kwargs.get("name", None) else "Untitled"
        self.colour = kwargs["colour"] if kwargs.get("colour", None) else "#000000"

    def generate_uid(self, uid_old=None):
        """
        If the instance does not have a UID, a UID is generated.
        If there is a duplicate UID in the Graph to which the instance belongs, reassign a UID.
        """

        if self.connected_graph is None:
            self.uid = uuid.uuid4().hex[:UID_LENGTH]
        else:
            if uid_old is None:
                uid_new = uuid.uuid4().hex[:UID_LENGTH]
                while uid_new in self.connected_graph.components:
                    uid_new = uuid.uuid4().hex[:UID_LENGTH]
                    self.uid = uid_new
                self.uid = uid_new
            else:
                if uid_old not in self.connected_graph.components:
                    self.uid = uid_old
                else:
                    print("Error: Duplicate uid occurs", uid_old)
                    # Try to reassign UID...
                    uid_new = uuid.uuid4().hex[:UID_LENGTH]
                    while uid_new in self.connected_graph.components:
                        uid_new = uuid.uuid4().hex[:UID_LENGTH]
                        self.uid = uid_new
                    self.uid = uid_new
        return self.uid

    def get(self, element_attribute=None):
        """
        get(): return all
        get("name") return name
        """

        if element_attribute is None:
            return vars(self)
        else:
            return vars(self).get(element_attribute, None)

    def get_connected_graph(self):
        """
        get_connected_graph() return self.connected_graph
        """

        return self.connected_graph

    def get_uid(self):
        """
        get_uid()
        """

        return self.uid

    def get_name(self):
        """
        get_name()
        """

        return self.name

    def get_colour(self):
        """
        get_colour()
        """

        return self.colour

    def update(self, element_attribute, element_attribute_new_value):
        """
        update()
        """

        if element_attribute in self.vars(self):
            self.element_attribute = element_attribute_new_value
            return True
        else:
            return False

    def update_connected_gui(self, connected_gui_new):
        """
        update_connected_gui()
        """

        self.connected_gui = connected_gui_new

    def delete(self):
        """
        delete()
        """

        if self.connected_graph is not None:
            return self.connected_graph.delete_component(self.uid)
        else:
            return False


class Node(GraphComponent):
    """
    Node()
    """

    def __init__(
        self,
        connected_graph=None,
        **kwargs,
    ):
        self.colour = kwargs["colour"] if kwargs.get("colour", None) else "#fd5455"
        kwargs["colour"] = self.colour
        super().__init__(connected_graph, **kwargs)

        self.position = kwargs["position"] if kwargs.get("position", None) else [0, 0]
        self.arcs = []  # Objects of the arc connected to this node

    def get_position(self):
        """
        get_position()
        """

        return self.position

    def update(self, element_attribute, element_attribute_new_value):
        """
        update(position, [10, 10])
        """

        if element_attribute == "position":
            self.position[0] = element_attribute_new_value[0]
            self.position[1] = element_attribute_new_value[1]
            return True
        else:
            return super().update(element_attribute, element_attribute_new_value)

    def update_position(self, position):
        """
        update_position([10, 10])
        """

        self.position[0] = position[0]
        self.position[1] = position[1]


class SourceNode(Node):
    """
    SourceNode()
    """

    def __init__(
        self,
        connected_graph=None,
        **kwargs,
    ):
        self.colour = kwargs["colour"] if kwargs.get("colour", None) else "#0f8080"
        kwargs["colour"] = self.colour

        super().__init__(connected_graph, **kwargs)

        self.user_defined_attribute = (
            kwargs["user_defined_attribute"]
            if kwargs.get("user_defined_attribute", None)
            else "0"
        )

    def get_user_defined_attribute(self):
        """
        get_user_defined_attribute()
        """

        return self.user_defined_attribute

    def update_user_defined_attribute(self, user_defined_attribute_new):
        """
        update_user_defined_attribute()
        """

        self.user_defined_attribute = user_defined_attribute_new


class GroundNode(Node):
    """
    GroundNode()
    """

    def __init__(
        self,
        connected_graph=None,
        **kwargs,
    ):
        self.colour = kwargs["colour"] if kwargs.get("colour", None) else "#d4aa01"
        kwargs["colour"] = self.colour

        super().__init__(connected_graph, **kwargs)

        self.user_defined_attribute = "0"

        if connected_graph is not None:
            self.connected_graph.groundnode_counter += 1

    def get_user_defined_attribute(self):
        """
        get_user_defined_attribute()
        """

        return self.user_defined_attribute

    def update_user_defined_attribute(self):
        """
        update_user_defined_attribute()
        """

        return False  # groundnode user_defined_attribute cannot be modified


if __name__ == "__main__":
    import unittest
    from tests import TestGraphComponent

    unittest.main()

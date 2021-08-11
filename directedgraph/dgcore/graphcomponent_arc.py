import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))

from directedgraph.dgcore import GraphComponent, Node


class Arc(GraphComponent):
    def __init__(self, connected_graph=None, **kwargs):
        super().__init__(connected_graph, **kwargs)

        self.nodes = [None, None]
        self.update_position(kwargs["node1_uid"], kwargs["node2_uid"])

        self.user_defined_attribute = (
            kwargs["user_defined_attribute"]
            if kwargs.get("user_defined_attribute", None)
            else "0"
        )

        self.user_defined_arc_type = (
            kwargs["user_defined_arc_type"]
            if kwargs.get("user_defined_arc_type", None)
            else None
        )

        # self.function = {}

    # get_position() get positions of two objects connected by the arc
    # #TODO 需要设计 Trace Back 捕捉
    def get_position(self):
        return self.nodes[0].get_position(), self.nodes[1].get_position()

    # update_position() get positions of two objects connected by the arc
    # update_position() can accept both UIDs and objects as parameters
    # #TODO 需要设计 Trace Back 捕捉
    def update_position(self, node1=None, node2=None):
        if node1 is not None:
            if isinstance(node1, str):
                if len(node1) == 6 and self.connected_graph is not None:
                    self.nodes[0] = self.connected_graph.get_component(node1)
            elif isinstance(node1, Node):
                self.nodes[0] = node1

        if node2 is not None:
            if isinstance(node2, str) and self.connected_graph is not None:
                if len(node2) == 6 and self.connected_graph is not None:
                    self.nodes[1] = self.connected_graph.get_component(node2)
            elif isinstance(node2, Node):
                self.nodes[1] = node2

    def update_user_defined_arc_type(self, new_user_defined_arc_type):
        self.user_defined_arc_type = new_user_defined_arc_type

    def update_user_defined_attribute(self, new_user_defined_attribute):
        str_can_be_used = ["p", "u", "k", "n", "m"]
        if new_user_defined_attribute.isdigit() is True:
            if self.user_defined_arc_type.lower() == "resistor":
                if (
                    len(new_user_defined_attribute) > 1
                    and new_user_defined_attribute[0] == "0"
                    or new_user_defined_attribute == "-"
                ):
                    raise ValueError("wrong input!!!")
        elif new_user_defined_attribute.isdigit() is False:
            if new_user_defined_attribute[0] == "0":
                raise ValueError("wrong input!!!")
            for j in new_user_defined_attribute:
                if j.isdigit() is False:
                    if j.lower() not in str_can_be_used:
                        raise ValueError("wrong input!!!")
                    else:
                        index = new_user_defined_attribute.index(j)
                        if len(new_user_defined_attribute[index:]) > 1:
                            raise ValueError("wrong input!!!")
        else:
            self.user_defined_attribute = new_user_defined_attribute

        self.user_defined_attribute = new_user_defined_attribute

    # get editable function,eg: if Take a resistance.
    # The current through the resistance from node i to node j is given by (V_i - V)j) / R.
    # But if the arc represented a diode, the current would be I_0 [exp((V_i - V_j)/kT) - 1].
    # def get_function(self):
    #     if self.user_defined_attribute == None:
    #         return
    #     elif self.user_defined_attribute.lower() == "resistance":
    #         if (
    #             isinstance(self.node1, Node)
    #             and isinstance(self.node2, SourceNode)
    #             or isinstance(self.node2, GroundNode)
    #         ):
    #             return (
    #                 abs(self.node1.value - float(self.node2.user_defined_attribute))
    #                 / self.impedance
    #             )
    #
    #         elif (
    #             isinstance(self.node1, SourceNode)
    #             or isinstance(self.node1, GroundNode)
    #             and isinstance(self.node2, Node)
    #         ):
    #             return (
    #                 abs(
    #                     float(self.node1.user_defined_attribute)
    #                     - float(self.node2.value)
    #                 )
    #                 / self.impedance
    #             )
    #
    #         elif (
    #             isinstance(self.node1, SourceNode)
    #             or isinstance(self.node1, GroundNode)
    #             and isinstance(self.node2, GroundNode)
    #             or isinstance(self.node2, SourceNode)
    #         ):
    #             return (
    #                 abs(
    #                     float(self.node1.user_defined_attribute)
    #                     - float(self.node2.user_defined_attribute)
    #                 )
    #                 / self.impedance
    #             )
    #     elif self.user_defined_attribute.lower() == "capacitor":
    #         if (
    #             isinstance(self.node1, Node)
    #             and isinstance(self.node2, SourceNode)
    #             or isinstance(self.node2, GroundNode)
    #         ):
    #             return (
    #                 abs(self.node1.value - float(self.node2.user_defined_attribute))
    #                 / self.impedance
    #             )
    #
    #         elif (
    #             isinstance(self.node1, SourceNode)
    #             or isinstance(self.node1, GroundNode)
    #             and isinstance(self.node2, Node)
    #         ):
    #             return (
    #                 abs(
    #                     float(self.node1.user_defined_attribute)
    #                     - float(self.node2.value)
    #                 )
    #                 / self.impedance
    #             )
    #
    #         elif (
    #             isinstance(self.node1, SourceNode)
    #             or isinstance(self.node1, GroundNode)
    #             and isinstance(self.node2, GroundNode)
    #             or isinstance(self.node2, SourceNode)
    #         ):
    #             return (
    #                 abs(
    #                     float(self.node1.user_defined_attribute)
    #                     - float(self.node2.user_defined_attribute)
    #                 )
    #                 / self.impedance
    #             )
    #     elif self.user_defined_attribute.lower() == "diode":
    #         pass
    #
    # # function['resistance']=(V_i - V)j) / R.
    # def update_function(self):
    #     function_update = self.get_function()
    #     self.function[self.user_defined_attribute] = function_update
    #
    # def update_node(self):
    #     if isinstance(self.node1, SourceNode) and isinstance(self.node2, Node):
    #         node2.value = float(
    #             self.node1.user_defined_attribute
    #         ) - node1.current * float(self.impedance)
    #     elif isinstance(self.node1, Node) and isinstance(self.node2, Node):
    #         node2.value = (
    #             float(self.node1.value)
    #             - self.impedance * self.function[self.user_defined_attribute]
    #         )

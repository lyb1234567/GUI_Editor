import sys
from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent.parent
CURRENT_FOLDER_PATH = str(CURRENT_FOLDER)
sys.path.append(CURRENT_FOLDER_PATH)

from directedgraph.dgcore import (
    Node,
    SourceNode,
    GroundNode,
    Arc,
)

# pass  node as uid
# def test_arc_init_case_1():
#     from directedgraph.dgcore.graph import Graph

#     graph1 = Graph("graph1")
#     graph1.create_component({"type": "Node", "name": "Node 1", "uid": "859e4b"})
#     graph1.create_component({"type": "Node", "name": "Node 2", "uid": "7778da"})
#     # graph1.print_graph_details()
#     arc1 = Arc(
#         graph1,
#         "123",
#         None,
#         "arc1",
#         "859e4b",
#         "7778da",
#     )
#     print(arc1.get())
#     # print(arc1.nodes)
#     print(arc1.get_position())


# # pass node as objects
# def test_arc_init_case_2():
#     node1 = Node(None, None, "node1", None, None)
#     node2 = GroundNode(None, None, "node2", None, [10, 10])
#     arc1 = Arc(
#         None,
#         "123",
#         None,
#         "arc1",
#         node1,
#         node2,
#     )
#     print(arc1.get())
#     # print(arc1.nodes)
#     print(arc1.get_position())


# def test_arc_function():
#     node1 = GroundNode(None, None, "node1", None, None)
#     # set SourceNode user_defined_attribute to 5(5v)
#     node2 = SourceNode(None, None, "ndoe2", None, None, 10)
#     arc1 = Arc(None, "sdasd", "arc1", None, node1, node2, "resistance", 5)
#     arc1.get_function()
#     print(arc1.get())
#     arc1.update_function("resistance")
#     print(arc1.get())

#     from directedgraph.dgcore.graph import Graph

#     graph1 = Graph("graph1")
#     graph1.create_component({"type": "Node", "name": "Node 1", "uid": "859e4b"})
#     graph1.create_component({"type": "Node", "name": "Node 2", "uid": "7778da"})
#     # graph1.print_graph_details()
#     arc2 = Arc(graph1, "123", None, "arc2", "859e4b", "7778da0", "resistance", 5)
#     arc2.get_function()
#     print(arc2.get())
#     arc2.update_function("resistance")
#     print(arc2.get())


if __name__ == "__main__":
    # test_arc_init_case_1()
    # test_arc_init_case_2()
    # test_arc_function()
    pass

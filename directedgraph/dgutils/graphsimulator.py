import sys
import os
from pathlib import Path
import csv

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))

from directedgraph.dgcore import Graph, Node, SourceNode, GroundNode, Arc
from directedgraph.dgutils import FileManager


class GraphSimulator:
    def __init__(self):
        pass

    def export(self, filepath, import_graph):
        arc_list = []
        node_uid_list = []
        sourcenode_list = []
        groundnode_list = []

        resistor_count = 1
        capacitor_count = 1
        inductor_count = 1

        uid_map = {}

        for component in import_graph.components.values():
            if type(component) == Arc:
                arc_list.append(component)
            if type(component) == SourceNode:
                sourcenode_list.append(component)
            if type(component) == GroundNode:
                groundnode_list.append(component)
            if type(component) == Node:
                node_uid_list.append(component)

        print(arc_list)
        print(node_uid_list)
        print(sourcenode_list)
        print(groundnode_list)
        ####################
        i = 0
        for n in groundnode_list:
            if n.uid not in uid_map:
                uid_map[n.uid] = i
                i += 1
        for n in sourcenode_list:
            if n.uid not in uid_map:
                uid_map[n.uid] = i
                i += 1
        for n in node_uid_list:
            if n.uid not in uid_map:
                uid_map[n.uid] = i
                i += 1

        print(uid_map)

        ####################

        # Output txt
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            graph_name = import_graph.name
            headers = ["Arc", "Node1", "Node2", "Value", "#", str(graph_name)]
            f_csv = csv.writer(f, delimiter=" ")
            f_csv.writerow(headers)

            f_csv.writerow(
                [
                    f"VS",  # VS
                    uid_map[sourcenode_list[0].uid],
                    uid_map[groundnode_list[0].uid],
                    sourcenode_list[0].user_defined_attribute,
                    ";",
                    sourcenode_list[0].uid,
                    groundnode_list[0].uid,
                ]
            )

            for arc in arc_list:
                if arc.user_defined_arc_type == "Resistor":
                    print(
                        "R"
                        + str(resistor_count)
                        + f" {uid_map[arc.nodes[0].uid]}"
                        + f" {uid_map[arc.nodes[1].uid]}"
                        + f" {arc.user_defined_attribute}"
                    )
                    f_csv.writerow(
                        [
                            f"R{resistor_count}",
                            uid_map[arc.nodes[0].uid],
                            uid_map[arc.nodes[1].uid],
                            arc.user_defined_attribute,
                            ";",
                            arc.nodes[0].uid,
                            arc.nodes[1].uid,
                        ]
                    )
                    resistor_count = resistor_count + 1
                    pass
                if arc.user_defined_arc_type == "Capacitor":
                    print(
                        "C"
                        + str(capacitor_count)
                        + f" {uid_map[arc.nodes[0].uid]}"
                        + f" {uid_map[arc.nodes[1].uid]}"
                        + f" {arc.user_defined_attribute}"
                    )
                    f_csv.writerow(
                        [
                            f"C{capacitor_count}",
                            uid_map[arc.nodes[0].uid],
                            uid_map[arc.nodes[1].uid],
                            arc.user_defined_attribute,
                            ";",
                            arc.nodes[0].uid,
                            arc.nodes[1].uid,
                        ]
                    )
                    capacitor_count = capacitor_count + 1
                    pass
                if arc.user_defined_arc_type == "Inductor":
                    print(
                        "L"
                        + str(inductor_count)
                        + f" {uid_map[arc.nodes[0].uid]}"
                        + f" {uid_map[arc.nodes[1].uid]}"
                        + f" {arc.user_defined_attribute}"
                    )
                    f_csv.writerow(
                        [
                            f"L{inductor_count}",
                            uid_map[arc.nodes[0].uid],
                            uid_map[arc.nodes[1].uid],
                            arc.user_defined_attribute,
                            ";",
                            arc.nodes[0].uid,
                            arc.nodes[1].uid,
                        ]
                    )
                    inductor_count = inductor_count + 1
                    pass
                if arc.user_defined_arc_type == "None":
                    pass
            f_csv.writerow([".TRAN", "0.1M", "30M", "UIC"])
            f_csv.writerow([".end"])

            # 批量替换 UID
            # 先把所有的UID按照顺序（先R 再C）输出一下，再把每个UID替换成0 1 2 ……
            # Eg. (a-f 代指每个Arc的两个不同的uid) (这只是一个例子，最后程序应该能根据输入的Arc来输出相对应的电路规格文本.cir)
            #   R1 a b
            #   R2 b c
            #   R3 b c
            #   R4,R5,R6 c d
            #   R7 d e
            #   R8 e g
            #   R9 g h
            #   C1 d f
            #   C2 f g
            # 如果全部列出来即 ab bc bc cd cd cd de df fg eg gh
            # 在Spice输出规范里面不直接考虑单独的groundnode和sourcenode
            # 那么在这个输出规范里面我们应该认为在groundnode和sourcenode有一个Vdd等效为一个电源的输入
            # 在这个例子里，R1的node1没有重合的UID,R9的node2没有重合的UID，所以这两个node可以被认为和单独的
            # groundnode和sourcenode相连结，并通过算法将node1等效于sourcenode，node2等效于groundnode
            # 然后依次替换,uid=> 01 12 12 23 23 23 34 35 56 46 67
            # 这个可能储存在[0,1,1,2,1,2,2,3,2,3,2,3,3,4,3,5,5,6,4,7,6,7]
            # 最后读取输出 Vdd 1 22 value （1 22 指的是位置）
            #             R1 1 2 value
            #             R2 3 4 value
            #             ……
            #             R9 21 22 valu
            #
            # 最后输出到文本里应该是
            #   Vdd 0 7 x（代指value）
            #   C1 3 5 x
            #   C2 5 6 x
            #   R1 0 1 x
            #   R2 1 2 x
            #   R3 1 2 x
            #   R4 2 3 x
            #   R5 2 3 x
            #   R6 2 3 x
            #   R7 3 4 x
            #   R8 4 6 x
            #   R9 6 7 x


if __name__ == "__main__":
    path = (
        Path(os.path.dirname(__file__))
        .parent.parent.joinpath("tests")
        .joinpath("test_rlc.xml")
    )

    path_out = (
        Path(os.path.dirname(__file__))
        .parent.parent.joinpath("tests")
        .joinpath("test_rlc.cir")
    )

    fm = FileManager()
    import_graph = fm.open_graph(str(path))
    gs = GraphSimulator()
    gs.export(path_out, import_graph)

    # graph_attribute = [{"name": "import_graph"}]
    # graph_components = [
    #     {
    #         "type": "Node",
    #         "uid": "7778da",
    #         "name": "Node 2",
    #         "colour": "#fd5455",
    #         "position_x": "100",
    #         "position_y": "105",
    #     },
    #     {
    #         "type": "Node",
    #         "uid": "32a24b",
    #         "name": "Node 3",
    #         "colour": "#fd5455",
    #         "position_x": "30",
    #         "position_y": "30",
    #     },
    #     {
    #         "type": "SourceNode",
    #         "uid": "b20350",
    #         "name": "SourceNode 1",
    #         "colour": "#0f8080",
    #         "position_x": "40",
    #         "position_y": "40",
    #         "user_defined_attribute": "10",
    #     },
    #     {
    #         "type": "GroundNode",
    #         "uid": "365bb9",
    #         "name": "GroundNode 0",
    #         "colour": "#d4aa01",
    #         "position_x": "40",
    #         "position_y": "40",
    #     },
    #     {
    #         "type": "Arc",
    #         "uid": "2f7002",
    #         "name": "Resistor 1",
    #         "colour": "#0000",
    #         "node1_uid": "b20350",
    #         "node2_uid": "7778da",
    #         "user_defined_attribute": "20",
    #         "user_defined_arc_type": "Resistor",
    #     },
    #     {
    #         "type": "Arc",
    #         "uid": "0dcb2f",
    #         "name": "Resistor 2",
    #         "colour": "#0000",
    #         "node1_uid": "365bb9",
    #         "node2_uid": "7778da",
    #         "user_defined_attribute": "20",
    #         "user_defined_arc_type": "Resistor",
    #     },
    #     {
    #         "type": "Arc",
    #         "uid": "33ae52",
    #         "name": "Resistor 3",
    #         "colour": "#0000",
    #         "node1_uid": "365bb9",
    #         "node2_uid": "32a24b",
    #         "user_defined_attribute": "4000",
    #         "user_defined_arc_type": "Resistor",
    #     },
    #     {
    #         "type": "Arc",
    #         "uid": "6bf56b",
    #         "name": "Capacitor 1",
    #         "colour": "#0000",
    #         "node1_uid": "365bb9",
    #         "node2_uid": "32a24b",
    #         "user_defined_attribute": "0.0000005",
    #         "user_defined_arc_type": "Capacitor",
    #     },
    #     {
    #         "type": "Arc",
    #         "uid": "2201bd",
    #         "name": "Inductor 1",
    #         "colour": "#0000",
    #         "node1_uid": "7778da",
    #         "node2_uid": "32a24b",
    #         "user_defined_attribute": "0.2",
    #         "user_defined_arc_type": "Inductor",
    #     },
    # ]
    # graph_raw_data = (graph_attribute, graph_components)
    # import_graph = fm.create_graph(graph_raw_data)

    # import_graph.print_graph_details()

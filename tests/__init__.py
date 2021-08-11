from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())

from tests.test_dgcore_graph import TestGraph
from tests.test_dgcore_graphcomponent import TestGraphComponent
from tests.test_dgcore_graph_application import TestDirectedGraphApplication
from tests.test_dgutils_filemanager import TestFileManager

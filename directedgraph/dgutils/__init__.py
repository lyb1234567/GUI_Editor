from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())

from directedgraph.dgutils.filemanager import FileManager
from directedgraph.dgutils.graphsimulator import GraphSimulator

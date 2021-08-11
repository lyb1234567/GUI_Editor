import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))


if __name__ == "__main__":
    import unittest
    from tests import TestDirectedGraphApplication

    unittest.main()

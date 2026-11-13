import os
import sys

# Make the app package importable when tests run from the repo root or from cypher/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

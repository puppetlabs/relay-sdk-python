import sys
import os

# RTD changes directory into docs/ to run the build,
# so the module code cannot be found for autodoc
if os.environ.get('READTHEDOCS') == 'True':
  sys.path.append("../src")
else:
  sys.path.append("./src")

project = "Relay.sh SDK"
author = "Puppet Inc"
copyright = f"2020, {author}"
extensions = [
  "sphinx.ext.autodoc",
  "sphinx.ext.napoleon",
  "sphinx_autodoc_typehints"
]

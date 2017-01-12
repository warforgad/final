import importlib, os
from .. import plugin

for dyn_plugin in os.listdir(os.path.dirname(__file__)):
    if dyn_plugin != '__init__.py':
        importlib.import_module('.' + os.path.splitext(dyn_plugin)[0], __name__)

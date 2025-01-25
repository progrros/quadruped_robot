# my_package/__init__.py
print("Initializing my_package!")  # Just a demo message

# Package-wide constant
VERSION = "2.0.0"

# Import submodules so that users can access them directly via my_package
# from outside code
#__all__ = ["calculations", "servo", "utils"]

# Import the submodules
#from . import calculations
from . import utils
from . import servo

# (Optional) You could also do wildcard imports, but it’s typically not recommended:
# from .calculations import *
# from .utils import *

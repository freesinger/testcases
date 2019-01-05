import PySide2.QtCore

# Prints PySide2 version
# e.g. 5.11.1a1
print('PySide2 version:', PySide2.__version__)

# Gets a tuple with each version component
# e.g. (5, 11, 1, 'a', 1)
# print(PySide2.__version_info__)

# Prints the Qt version used to compile PySide2
# e.g. "5.11.2"
print('Qt version:', PySide2.QtCore.__version__)

# Gets a tuple with each version components of Qt used to compile PySide2
# e.g. (5, 11, 2)
# print(PySide2.QtCore.__version_info__)

# Print the current running Qt version number
print(PySide2.QtCore.qVersion())
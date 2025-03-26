# Here you define the commands that will be added to your add-in.

# Import each command's entry module
from .unlinkedCopy import entry as unlinkedCopy
from .flipComponent import entry as flipComponent
from .componentMirror import entry as componentMirror

# Add the command modules to this list
commands = [
    unlinkedCopy,
    flipComponent,
    componentMirror
]

def start():
    for command in commands:
        command.start()

def stop():
    for command in commands:
        command.stop()

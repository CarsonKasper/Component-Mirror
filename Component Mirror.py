# Assuming you have not changed the general structure of the template,
# no modification is needed in this file.

from . import commands
from .lib import fusionAddInUtils as futil


def run(context):
    try:
        # This will run the start() function in each of your commands
        commands.start()
    except:
        futil.handle_error('run')


def stop(context):
    try:
        # Remove all global event handlers
        futil.clear_handlers()

        # This will run the stop() function in each of your commands
        commands.stop()
    except:
        futil.handle_error('stop')

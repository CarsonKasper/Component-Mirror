import adsk.core

class Command:
    def __init__(self):
        self.id = 'flipComponent'
        self.name = 'Flip Component'
        self.tooltip = 'Flips the selected component and sketches'
        self.resources = 'resources'
        self.workspace = 'FusionSolidEnvironment'
        self.panel = 'SolidScriptsAddinsPanel'
        self.command_control_id = None
        self.command_definition = None

    def on_execute(self, args: adsk.core.CommandEventArgs):
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox(f'{self.name} clicked!')

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        pass

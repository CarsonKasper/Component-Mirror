import adsk.core
import adsk.fusion
import traceback
import os

from ...lib import fusionAddInUtils as futil

app = adsk.core.Application.get()
ui = app.userInterface

class Command:
    def __init__(self):
        self.id = 'unlinkedCopy'
        self.name = 'Unlinked Copy'
        self.tooltip = 'Creates an unlinked copy of the selected component'

        self.resources = os.path.join(os.path.dirname(__file__), 'resources')
        if not os.path.isdir(self.resources):
            self.resources = ''

        self.workspace = 'FusionSolidEnvironment'
        self.panel = 'ComponentMirrorPanel'
        self.tab = 'ToolsTab'
        self.command_control_id = None
        self.command_definition = None

    def on_execute(self, args: adsk.core.CommandEventArgs):
        ui.messageBox(f'{self.name} clicked!')

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        pass

class ExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, command_obj):
        super().__init__()
        self.command_obj = command_obj

    def notify(self, args):
        self.command_obj.on_execute(args)

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, command_obj):
        super().__init__()
        self.command_obj = command_obj

    def notify(self, args):
        command = args.command
        inputs = command.commandInputs

        execute_handler = ExecuteHandler(self.command_obj)
        futil.add_handler(execute_handler)
        command.execute.add(execute_handler)

        self.command_obj.on_create(command, inputs)

def start():
    try:
        cmd = Command()

        cmd_def = ui.commandDefinitions.itemById(cmd.id)
        if cmd_def:
            cmd_def.deleteMe()

        cmd_def = ui.commandDefinitions.addButtonDefinition(
            cmd.id, cmd.name, cmd.tooltip, cmd.resources
        )

        on_command_created = CommandCreatedHandler(cmd)
        futil.add_handler(on_command_created)
        cmd_def.commandCreated.add(on_command_created)

        workspace = ui.workspaces.itemById(cmd.workspace)
        toolbar_panels = workspace.toolbarPanels
        panel = toolbar_panels.itemById(cmd.panel)
        if not panel:
            panel = toolbar_panels.add(cmd.panel, 'Component Mirror', cmd.tab, False)

        if not panel.controls.itemById(cmd.id):
            panel.controls.addCommand(cmd_def, '', False)

    except:
        futil.handle_error('start')

def stop():
    try:
        cmd_id = 'unlinkedCopy'
        panel_id = 'ComponentMirrorPanel'

        workspace = ui.workspaces.itemById('FusionSolidEnvironment')
        toolbar_panels = workspace.toolbarPanels
        panel = toolbar_panels.itemById(panel_id)

        if panel:
            ctrl = panel.controls.itemById(cmd_id)
            if ctrl:
                ctrl.deleteMe()
            dropdown = panel.controls.itemById(f'{cmd_id}_dropdown')
            if dropdown:
                dropdown.deleteMe()

        cmd_def = ui.commandDefinitions.itemById(cmd_id)
        if cmd_def:
            cmd_def.deleteMe()

    except:
        futil.handle_error('stop')

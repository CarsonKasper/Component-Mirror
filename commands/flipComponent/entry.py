import adsk.core
import adsk.fusion
import traceback
import os

app = adsk.core.Application.get()
ui = app.userInterface

class Command:
    def __init__(self):
        self.id = 'flipComponent'
        self.name = 'Flip Component'
        self.tooltip = 'Flips the selected component over the selected plane'

        # ✅ Absolute path to resources folder
        self.resources = os.path.join(os.path.dirname(__file__), 'resources')
        if not os.path.isdir(self.resources):
            self.resources = ''  # fallback if missing

        self.workspace = 'FusionSolidEnvironment'
        self.panel = 'ComponentMirrorPanel'
        self.tab = 'ToolsTab'  # Utilities tab
        self.command_control_id = None
        self.command_definition = None

    def on_execute(self, args: adsk.core.CommandEventArgs):
        ui.messageBox(f'{self.name} clicked!')

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        pass

# Event handler for command execution
class ExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, command_obj):
        super().__init__()
        self.command_obj = command_obj

    def notify(self, args):
        self.command_obj.on_execute(args)

# Event handler for command creation
class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, command_obj):
        super().__init__()
        self.command_obj = command_obj

    def notify(self, args):
        command = args.command
        inputs = command.commandInputs
        command.execute.add(ExecuteHandler(self.command_obj))
        self.command_obj.on_create(command, inputs)

def start():
    try:
        cmd = Command()

        # Delete old definition if exists
        cmd_def = ui.commandDefinitions.itemById(cmd.id)
        if cmd_def:
            cmd_def.deleteMe()

        # Create new command definition with icon
        cmd_def = ui.commandDefinitions.addButtonDefinition(
            cmd.id, cmd.name, cmd.tooltip, cmd.resources
        )

        # Hook up event
        on_command_created = CommandCreatedHandler(cmd)
        cmd_def.commandCreated.add(on_command_created)

        # ✅ Get the workspace and its toolbarPanels list
        workspace = ui.workspaces.itemById(cmd.workspace)
        toolbar_panels = workspace.toolbarPanels

        # ✅ Create or get custom panel in Utilities tab
        panel = toolbar_panels.itemById(cmd.panel)
        if not panel:
            panel = toolbar_panels.add(cmd.panel, 'Component Mirror', cmd.tab, False)

        # Add to panel as main button
        if not panel.controls.itemById(cmd.id):
            panel.controls.addCommand(cmd_def, '', False)
        else:
            # Fusion may auto-add to dropdown when adding to panel — avoid duplication
            return


    except:
        ui.messageBox('Failed to start command:\n{}'.format(traceback.format_exc()))

def stop():
    try:
        cmd_id = 'flipComponent'
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
        pass

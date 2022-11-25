import pprint
import inspect
import html
import copy

import pyblish.api
from Qt import QtWidgets, QtCore, QtGui


TAB = 4* "&nbsp;"
HEADER_SIZE = "15px"
KEY_COLOR = "#ffffff"
NEW_KEY_COLOR = "#00ff00"
VALUE_TYPE_COLOR = "#ffbbbb"
VALUE_COLOR = "#777799"
NEW_VALUE_COLOR = "#DDDDCC"

COLORED = "<font style='color:{color}'>{txt}</font>"

MAX_VALUE_STR_LEN = 100

def format_data(data, previous_data):
    previous_data = previous_data or {}
    msg = ""
    for key, value in sorted(data.items()):
        type_str = type(value).__name__
        
        key_color = NEW_KEY_COLOR if key not in previous_data else KEY_COLOR
        value_color = VALUE_COLOR
        if key not in previous_data or previous_data[key] != value:
            value_color = NEW_VALUE_COLOR
        
        value_str = str(value)
        if len(value_str) > MAX_VALUE_STR_LEN:
            value_str = value_str[:MAX_VALUE_STR_LEN] + "..."
            
        key_str = COLORED.format(txt=key, color=key_color)
        type_str = COLORED.format(txt=type_str, color=VALUE_TYPE_COLOR)
        value_str = COLORED.format(txt=html.escape(value_str), color=value_color)
        
        data_str = TAB + f"{key_str} ({type_str}): {value_str} <br>"
        
        msg += data_str
    return msg
    

class DebugUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(DebugUI, self).__init__(parent=parent)
        
        self.setWindowTitle("Pyblish Debug Stepper")
        self.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowMinimizeButtonHint
            | QtCore.Qt.WindowCloseButtonHint
            | QtCore.Qt.WindowStaysOnTopHint
        )
        
        layout = QtWidgets.QVBoxLayout(self)
        text_edit = QtWidgets.QTextEdit()
        font = QtGui.QFont("NONEXISTENTFONT")
        font.setStyleHint(font.TypeWriter)
        text_edit.setFont(font)
        text_edit.setLineWrapMode(text_edit.NoWrap)

        step = QtWidgets.QPushButton("Step")
        step.setEnabled(False)

        layout.addWidget(text_edit)
        layout.addWidget(step)

        step.clicked.connect(self.on_step)

        self._pause = False
        self.text = text_edit
        self.step = step
        self.resize(700, 500)
        
        self._previous_data = {}

    def pause(self, state):
        self._pause = state
        self.step.setEnabled(state)

    def on_step(self):
        self.pause(False)

    def showEvent(self, event):
        print("Registering callback..")
        pyblish.api.register_callback("pluginProcessed",
                                      self.on_plugin_processed)

    def hideEvent(self, event):
        self.pause(False)
        print("Deregistering callback..")
        pyblish.api.deregister_callback("pluginProcessed",
                                        self.on_plugin_processed)

    def on_plugin_processed(self, result):
        self.pause(True)
        
        # Don't tell me why - but the pyblish event does not
        # pass along the context with the result. And thus
        # it's non trivial to debug step by step. So, we
        # get the context like the evil bastards we are.
        i = 0
        found_context = None
        current_frame = inspect.currentframe()
        for frame_info in inspect.getouterframes(current_frame):
            frame_locals = frame_info.frame.f_locals
            if "context" in frame_locals:
                found_context = frame_locals["context"]
                break
            i += 1
            if i > 5:
                print("Warning: Pyblish context not found..")
                # We should be getting to the context within 
                # a few frames
                break
        
        plugin_name = result["plugin"].__name__
        duration = result['duration']
        plugin_instance = result["instance"]
        
        msg = ""
        msg += f"Plugin: {plugin_name}"
        if plugin_instance is not None:
            msg += f" -> instance: {plugin_instance}"
        msg += "<br>"
        msg += f"Duration: {duration}ms<br>"
        msg += "====<br>"
        
        context = found_context
        if context is not None:
            id = "context"
            
            msg += f"""<font style='font-size: {HEADER_SIZE};'><b>Context:</b></font><br>"""
            msg += format_data(context.data, previous_data=self._previous_data.get(id))
            msg += "====<br>"
            self._previous_data[id] = copy.deepcopy(context.data)
            
            for instance in context:
                id = instance.name
                
                msg += f"""<font style='font-size: {HEADER_SIZE};'><b>Instance:</b> {instance}</font><br>"""
                msg += format_data(instance.data, previous_data=self._previous_data.get(id))
                msg += "----<br>"
                self._previous_data[id] = copy.deepcopy(instance.data)
        
        self.text.setHtml(msg)

        app = QtWidgets.QApplication.instance()
        while self._pause:
            # Allow user interaction with the UI
            app.processEvents()


window = DebugUI()
window.show()

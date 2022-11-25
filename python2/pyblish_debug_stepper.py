import pprint
import inspect
#### PYTHON2 - HTML - BEGIN
#import html
#### PYTHON2 - HTML - MID
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
        #### PYTHON2 - HTML - BEGIN
        #value_str = COLORED.format(txt=html.escape(value_str), color=value_color)
        #### PYTHON2 - HTML - MID
        value_str = COLORED.format(txt=value_str, color=value_color)
        #### PYTHON2 - HTML - END
        
        #### PYTHON2 - FORMAT - BEGIN
        #data_str = TAB + f"{key_str} ({type_str}): {value_str} <br>"
        #### PYTHON2 - FORMAT - MID
        data_str = TAB + "{} ({}): {} <br>".format(key_str, type_str, value_str)
        #### PYTHON2 - FORMAT - END
        
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
            #### PYTHON2 - FRAME - BEGIN
            #frame_locals = frame_info.frame.f_locals
            #### PYTHON2 - FRAME - MID
            frame_locals = frame_info[0].f_locals
            #### PYTHON2 - FRAME - END
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
        
        #### PYTHON2 - FORMAT - BEGIN
        """
        msg = ""
        msg += f"Plugin: {plugin_name}"
        if plugin_instance is not None:
            msg += f" -> instance: {plugin_instance}"
        msg += "<br>"
        msg += f"Duration: {duration}ms<br>"
        msg += "====<br>"
        """
        #### PYTHON2 - FORMAT - MID
        msg = ""
        msg += "Plugin: {}".format(plugin_name)
        if plugin_instance is not None:
            msg += " -> instance: {}".format(plugin_instance)
        msg += "<br>"
        msg += "Duration: {}ms<br>".format(duration)
        msg += "====<br>"
        #### PYTHON2 - FORMAT - END
        
        context = found_context
        if context is not None:
            id = "context"
            
            #### PYTHON2 - FORMAT - BEGIN
            #msg += f"""<font style='font-size: {HEADER_SIZE};'><b>Context:</b></font><br>"""
            #### PYTHON2 - FORMAT - MID
            msg += """<font style='font-size: {};'><b>Context:</b></font><br>""".format(HEADER_SIZE)
            #### PYTHON2 - FORMAT - END
            msg += format_data(context.data, previous_data=self._previous_data.get(id))
            msg += "====<br>"
            #### PYTHON2 - DEEPCOPY - BEGIN
            #self._previous_data[id] = copy.deepcopy(context.data)
            #### PYTHON2 - DEEPCOPY - MID
            self._previous_data[id] = self.deep_c(context.data)
            #### PYTHON2 - DEEPCOPY - END
            
            for instance in context:
                id = instance.name
                
                #### PYTHON2 - FORMAT - BEGIN
                #msg += f"""<font style='font-size: {HEADER_SIZE};'><b>Instance:</b> {instance}</font><br>"""
                #### PYTHON2 - FORMAT - MID
                msg += """<font style='font-size: {};'><b>Instance:</b> {}</font><br>""".format(HEADER_SIZE, instance)
                #### PYTHON2 - FORMAT - END
                msg += format_data(instance.data, previous_data=self._previous_data.get(id))
                msg += "----<br>"
                #### PYTHON2 - DEEPCOPY - BEGIN
                #self._previous_data[id] = copy.deepcopy(instance.data)
                #### PYTHON2 - DEEPCOPY - MID
                self._previous_data[id] = self.deep_c(instance.data)
                #### PYTHON2 - DEEPCOPY - END
        
        self.text.setHtml(msg)

        app = QtWidgets.QApplication.instance()
        while self._pause:
            # Allow user interaction with the UI
            app.processEvents()


    #### PYTHON2 - DEEPCOPY - MID
    @classmethod
    def deep_c(cls, data):
        try:
            temp = copy.deepcopy(data)

        except TypeError as te:
            #print("data: {} ({})".format(data, type(data)))

            #TODO: Find better way
            # ~hack to avoid going deep in Ftrack objects
            # (=> max recursion level issue)
            if "ftrack" in str(type(data)).lower():
                return str(data)

            try:
                temp = {}
                for item in data:
                    #print("item '{}' ({}): {}".format(item, type(data[item]), data[item]))
                    temp[item] = cls.deep_c(data[item])

            except TypeError as te:
                if "__getitem__" in str(te):
                    temp = data
                #TODO: add case "iterable"?
        except Exception as e:
            #print("Exception: {}".format(str(e)))
            #TODO: str OK? => Find better way
            temp = str(data)

        return temp
    #### PYTHON2 - DEEPCOPY - END


# Auto execution removed
"""
window = DebugUI()
window.show()
"""

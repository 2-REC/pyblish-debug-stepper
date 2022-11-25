# Pyblish Debug Stepper

## Description

"Pauses between each plug-in process and shows the Context + Instances with their data at that point in time" (BigRoy)


Snippet/script from [BigRoy](https://gist.github.com/BigRoy)'s GitHub Gist "[pyblish_debug_stepper.py](https://gist.github.com/BigRoy/1972822065e38f8fae7521078e44eca2)".

Modified version for use with Python 2.


## Files

* "original/pyblish_debug_stepper.py"
    => Original script from BigRoy.

* "python2/pyblish_debug_stepper.py"
    => Modified script for Python 2 (tested in Maya 2020).


## Usage

The location of the script must be in Python's ```sys.path```.

Execute the script:
```
import pyblish_debug_stepper

window = pyblish_debug_stepper.DebugUI()
window.show()
```

! - The auto execution has been removed, to make it easier/cleaner to repeat the execution of the script.

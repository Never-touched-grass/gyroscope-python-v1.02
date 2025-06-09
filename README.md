# gyroscope-python-v1.05
Custom scripting interpreter written in Python
Note that this project was made with Visual Studio using external C++ libraries. Without the proper configuration properties, it will not work.
# Instructions:
1. Install Python from python.org, and make sure to add it to your systems PATH
2. Follow all the defualt file locations, as they will be needed for this instruction set.
3. Go to Windows Command Prompt and type "pip install pybind11" (without quotes)
4. Open a new Visual Studio Python Console App and name it GyroScopePy
5. Paste all the code from GyroScopePy.py and filemanager.py into accordingly named files
6. Right click on the solution. Click: add -> New Project -> Dynamic Link Library (DLL) (C++) and name it math_util
7. In the new project delete "framework.h"
8. Go to "pch.h" and remove the #include "framework.h"
9. Right click on math_util then click Properties -> Configuration Properties -> C/C++ -> General -> Additional Include Directories
10. Copy this path: C:/Users/name/AppData/Local/Programs/Python/Python313/include (replace name with your name) then go back to properties. Click the dropdown on the right side of the Additional Include Directories, click edit, and paste it there
11. Now, in your Python project, put import pybind11, then on the next line, print(pybind11.get_include())
12. That prints the path to pybind11's include directory
13. Copy that path, and do the same thing with it as you did with Python's include.
14. Now go to Linker -> General -> Additional Library Directories. Now copy this path: C:/Users/name/AppData/Local/ProgramsPython/Python313/libs, and paste it there.
15. Now go to Linker -> General -> Output File. Replace $(OutDir)$(TargetName).dll to $(OutDir)math_util.pyd
16. Create a new C++ file. Name it anything you want (e.g. math)
17. Paste the code from math.cpp into it
18. Press Ctrl + Shift + B to build it. If you followed the directions properly, the build should run successfully.
19. Search for the GyroScopePy folder. Open it, go to x64 -> Debug, and copy the math_util.pyd file.
20. Paste it into this folder: GyroScopePy -> GyroScopePy (project folder).
21. Enjoy!
# PLEASE READ
Please DO NOT put another repository with this code, without my permission and credit from me. You may make edits, as long as they are functional, and necessary.

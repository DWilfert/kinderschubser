[app]

# (str) Title of your application
title = Kinderschubser

# (str) Package name
package.name = kinderschubser

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source directory where the main.py file resides
source.dir = .

# (list) Source files to include (let it empty to include all files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let it empty to exclude all files)
source.exclude_exts = spec

# (list) List of directory to exclude (let it empty to exclude all files)
source.exclude_dirs = bin, venv, .git, .github

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) Use --private data storage (True) or --public storage (False)
android.private_storage = True

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
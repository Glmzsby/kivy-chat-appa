[app]
title = Mobile Chat
package.name = mobilechat
package.domain = org.mobileapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Application requirements and dependencies
requirements = python3,\
    kivy==2.3.1,\
    certifi,\
    chardet,\
    docutils,\
    idna,\
    Kivy-Garden,\
    kivymd,\
    Pillow,\
    requests,\
    urllib3,\
    cython

# Android specific settings
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a

# (str) Presplash of the application
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# (list) List of service to declare
services = 

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# Build options
android.release_artifact = apk
p4a.branch = master
p4a.bootstrap = sdl2
android.allow_backup = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
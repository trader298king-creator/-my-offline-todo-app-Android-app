
[app]

title = My To-Do App
package.name = mytodoapp
package.domain = org.myoffline

source.dir = .
source.include_exts = py,json

version = 1.0.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions =

android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

log_level = 2
warn_on_root = 1

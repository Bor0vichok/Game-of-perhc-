[app]
title = Underwater World
package.name = underwaterworld
package.domain = org.borovichok
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,ogg,mp3
version = 0.1
requirements = python3,pygame,sdl2,pyjnius
orientation = landscape
fullscreen = 1
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

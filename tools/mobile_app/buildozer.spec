[app]
title = AutoAccountor
package.name = autoaccountor
package.domain = com.autoaccountor
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# Android specific
android.api = 33
android.minapi = 21
# 修改 android.arch 为 android.archs
android.archs = arm64-v8a
# 移除 android.sdk，因为它已被弃用
# android.sdk = 33

# 添加其他架构，如果需要
# android.archs = arm64-v8a,x86,x86_64
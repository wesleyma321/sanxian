[app]

# 应用标题
title = 三仙归洞

# 应用名称（包名的一部分）
package.name = sanxian_guidou

# 包名
package.domain = com.traditional

# 源代码目录
source.dir = .

# 应用版本
version = 1.0.0

# 描述
description = 中国传统技艺三仙归洞游戏

# 需求列表
requirements = kivy

# 屏幕方向
orientation = portrait

# 全屏
fullscreen = 0

# 图标（可选）
# icon.filename = icon.png

# 启动画面（可选）
# splash.filename = splash.png

# Android特定配置
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION
android.archs = arm64-v8a, armeabi-v7a

# iOS特定配置（如果有）
# ios.kivy_ios_url = https://github.com/kivy/kivy-ios
# ios.kivy_ios_branch = master
# ios.ios_deploy_url = https://github.com/phonegap/ios-deploy

[buildozer]
android.sdk_path = /usr/local/lib/android/sdk

# 日志级别
log_level = 2

# 显示构建进度
show_build_output = True

# 用于创建keystore的密码
# android.release_keystore_password = your_password

# 构建模式
build_mode = debug

# Android SDK路径（如果不在默认位置）
# android.sdk_path = /path/to/android/sdk

# Android NDK路径（如果需要）
# android.ndk_path = /path/to/android/ndk

# Android NDK版本
android.ndk_version = 21

# Android API级别
android.api_level = 27

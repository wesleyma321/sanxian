# 三仙归洞 - Shell Game

中国传统民间技艺"三仙归洞"游戏，安卓版本。

## 功能特性

- **单人模式**：茶碗快速洗牌，找出隐藏的红色球
- **双人蓝牙联机**：
  - 表演者模式：可以看到球的位置
  - 观众模式：盲猜找出球
- **3D视觉效果**：
  - 青花瓷茶碗纹理
  - 红色球高光反射
  - 实时阴影效果
- **精美中国风UI**：传统配色，古朴风格

## 项目结构

```
sanxian/
├── main.py              # 主程序入口
├── buildozer.spec       # 打包配置文件
├── bluetooth_service.py  # 蓝牙联机服务
├── screens/
│   ├── menu_screen.py       # 主菜单
│   ├── game_screen.py       # 游戏界面
│   ├── bluetooth_screen.py  # 蓝牙设置
│   └── result_screen.py     # 结果界面
├── widgets/
│   ├── cup_widget.py        # 茶碗组件
│   └── ball_widget.py       # 红色球组件
└── utils/
    ├── animator.py          # 动画效果
    └── __init__.py
```

## 环境要求

- Python 3.10+
- Java JDK 17 或 21
- Android SDK（可选，用于本地调试）

## 安装步骤

### 1. 安装Python依赖

```bash
pip install kivy kivymd buildozer
```

### 2. 安装Java JDK

下载并安装 Adoptium JDK 21:
https://adoptium.net/

### 3. 构建APK

#### 方法一：使用构建脚本（推荐）
双击运行 `C:\Users\34613\Desktop\构建APK.bat`

#### 方法二：手动构建

```bash
cd C:\Users\34613\sanxian
buildozer android debug
```

APK文件将生成在 `bin/` 目录。

## 游戏玩法

1. **开始游戏**：点击"开始游戏"按钮
2. **洗牌阶段**：观察三个快速移动的茶碗
3. **选择阶段**：洗牌结束后，点击茶碗找出红色球
4. **得分规则**：
   - 找到球：+10分
   - 连续两次找不到：-5分

## 双人模式

1. 两部手机通过蓝牙连接
2. 一方选择"表演者"，另一方选择"观众"
3. 表演者可以看到球的位置，但碗是半透明的
4. 观众需要凭记忆找出球的位置

## 开发说明

- 使用 Kivy 2.3.1 + KivyMD 1.2.0 开发
- 使用 Buildozer 打包APK
- 动画使用 Kivy Animation API
- 蓝牙使用 Android Bluetooth API（需在Android设备上运行）

## 版本信息

- 版本：1.0.0
- 作者：传统技艺数字化
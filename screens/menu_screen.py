#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主菜单界面 - 改进版
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.core.text import LabelBase


class MenuScreen(Screen):
    """主菜单界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_ui()

    def _create_ui(self):
        """创建UI元素"""
        with self.canvas:
            # 中国风深色背景
            Color(0.12, 0.07, 0.04, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_bg, pos=self._update_bg)

        # 主布局
        main_layout = BoxLayout(
            orientation='vertical',
            padding=30,
            spacing=15
        )

        # 顶部装饰
        top_decoration = BoxLayout(size_hint_y=0.08)
        for i in range(9):
            dot = Label(
                text='●',
                font_size='12sp',
                color=(0.6 + i * 0.04, 0.4 + i * 0.03, 0.2, 1)  # 渐变金色
            )
            top_decoration.add_widget(dot)
        main_layout.add_widget(top_decoration)

        # 标题
        title_layout = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=5)

        title = Label(
            text='[color=ffd700]三仙归洞[/color]',
            font_size='52sp',
            bold=True,
            markup=True,
        )
        title_layout.add_widget(title)

        # 副标题
        subtitle = Label(
            text='[color=daa520]—— 传统民间技艺 ——[/color]',
            font_size='18sp',
            markup=True,
        )
        title_layout.add_widget(subtitle)
        main_layout.add_widget(title_layout)

        # 说明文字
        intro = Label(
            text='[color=888888]三人抬轿，瞬息万变\n眼观六路，心领神会[/color]',
            font_size='14sp',
            markup=True,
            size_hint_y=0.12
        )
        main_layout.add_widget(intro)

        # 按钮区域
        btn_layout = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=12)

        # 单人游戏按钮
        single_btn = self._create_menu_button('单人游戏', (0.75, 0.35, 0.1, 1))
        single_btn.bind(on_press=lambda x: self.start_single_mode())
        btn_layout.add_widget(single_btn)

        # 双人蓝牙按钮
        bluetooth_btn = self._create_menu_button('双人联机', (0.2, 0.5, 0.75, 1))
        bluetooth_btn.bind(on_press=lambda x: self.go_bluetooth())
        btn_layout.add_widget(bluetooth_btn)

        # 游戏说明按钮
        help_btn = self._create_menu_button('游戏说明', (0.4, 0.35, 0.3, 1))
        help_btn.bind(on_press=lambda x: self.show_help())
        btn_layout.add_widget(help_btn)

        main_layout.add_widget(btn_layout)

        # 底部装饰
        bottom_layout = BoxLayout(size_hint_y=0.1, padding=10)
        version = Label(
            text='[color=666666]三仙归洞 v1.0[/color]',
            font_size='12sp',
            markup=True
        )
        bottom_layout.add_widget(version)
        main_layout.add_widget(bottom_layout)

        self.add_widget(main_layout)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def _create_menu_button(self, text, color):
        """创建菜单按钮"""
        btn = Button(
            text=text,
            font_size='22sp',
            bold=True,
            background_color=color,
            color=(1, 0.95, 0.6, 1),
            border=(16, 16, 16, 16)
        )

        # 按钮边框效果
        with btn.canvas.before:
            Color(color[0] * 0.8, color[1] * 0.8, color[2] * 0.8, 1)
            Line(width=2, rectangle=(0, 0, btn.width, btn.height))

        return btn

    def start_single_mode(self):
        """开始单人模式"""
        app = self.manager.app
        app.start_game('single')
        self.manager.current = 'game'

    def go_bluetooth(self):
        """进入蓝牙设置"""
        self.manager.current = 'bluetooth'

    def show_help(self):
        """显示游戏说明"""
        # 创建一个简单的弹出说明
        from kivy.uix.popup import Popup
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.boxlayout import BoxLayout

        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        content.add_widget(Label(
            text='[color=ffd700]游戏说明[/color]',
            font_size='24sp',
            markup=True,
            size_hint_y=0.1
        ))
        content.add_widget(Label(
            text='[color=cccccc]1. 点击"开始游戏"后，球会随机藏在某个茶碗下\n'
                 '2. 茶碗会快速洗牌移动\n'
                 '3. 洗牌结束后，点击茶碗找出红色球\n'
                 '4. 找到+10分，连续两次找不到-5分\n\n'
                 '双人模式：\n'
                 '5. 表演者可看到球的位置\n'
                 '6. 观众需凭记忆找出球\n'
                 '7. 通过蓝牙联机实现[/color]',
            font_size='16sp',
            markup=True,
            size_hint_y=0.7
        ))

        close_btn = Button(text='知道了', size_hint_y=0.15)
        content.add_widget(close_btn)

        popup = Popup(title='', content=content, size_hint=(0.8, 0.6),
                    background_color=(0.15, 0.1, 0.08, 0.95),
                    auto_dismiss=True)
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def on_enter(self):
        """进入界面时"""
        pass
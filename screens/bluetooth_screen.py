#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝牙设置界面
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle


class BluetoothScreen(Screen):
    """蓝牙设置界面"""

    is_connected = False
    connection_role = None  # 'performer' or 'audience'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.12, 0.08, 0.05, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_bg, pos=self._update_bg)
        self._create_ui()

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def _create_ui(self):
        """创建UI"""
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        # 标题
        title = Label(
            text='[color=ffd700]蓝牙联机[/color]',
            font_size='32sp',
            bold=True,
            markup=True,
            size_hint_y=0.15
        )
        layout.add_widget(title)

        # 状态显示
        self.status_label = Label(
            text='[color=888888]未连接[/color]',
            font_size='18sp',
            markup=True,
            size_hint_y=0.1
        )
        layout.add_widget(self.status_label)

        # 连接按钮区域
        btn_layout = GridLayout(cols=2, spacing=15, size_hint_y=0.3)

        # 作为表演者
        performer_btn = Button(
            text='我是表演者',
            font_size='18sp',
            bold=True,
            background_color=(0.7, 0.2, 0.1, 1),
            color=(1, 0.9, 0.5, 1)
        )
        performer_btn.bind(on_press=lambda x: self.start_as_performer())
        btn_layout.add_widget(performer_btn)

        # 作为观众
        audience_btn = Button(
            text='我是观众',
            font_size='18sp',
            bold=True,
            background_color=(0.2, 0.4, 0.7, 1),
            color=(1, 0.9, 0.5, 1)
        )
        audience_btn.bind(on_press=lambda x: self.start_as_audience())
        btn_layout.add_widget(audience_btn)

        layout.add_widget(btn_layout)

        # 搜索设备按钮
        self.search_btn = Button(
            text='搜索设备',
            font_size='18sp',
            background_color=(0.4, 0.3, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        self.search_btn.bind(on_press=lambda x: self.search_devices())
        layout.add_widget(self.search_btn)

        # 设备列表
        self.device_list_label = Label(
            text='[color=666666]暂未搜索到设备[/color]',
            font_size='14sp',
            markup=True,
            size_hint_y=0.2
        )
        layout.add_widget(self.device_list_label)

        # 开始游戏按钮
        self.start_game_btn = Button(
            text='开始联机游戏',
            font_size='22sp',
            bold=True,
            background_color=(0.6, 0.5, 0.1, 1),
            color=(1, 0.9, 0.5, 1),
            size_hint_y=0.15
        )
        self.start_game_btn.bind(on_press=lambda x: self.start_multiplayer_game())
        self.start_game_btn.disabled = True
        layout.add_widget(self.start_game_btn)

        # 返回按钮
        back_btn = Button(
            text='返回菜单',
            font_size='16sp',
            size_hint_y=0.1
        )
        back_btn.bind(on_press=lambda x: self.go_menu())
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def start_as_performer(self):
        """作为表演者开始"""
        self.connection_role = 'performer'
        self.status_label.text = '[color=00ff00]已选择: 表演者模式[/color]'
        self.start_game_btn.disabled = False

    def start_as_audience(self):
        """作为观众开始"""
        self.connection_role = 'audience'
        self.status_label.text = '[color=00ff00]已选择: 观众模式[/color]'
        self.start_game_btn.disabled = False

    def search_devices(self):
        """搜索蓝牙设备"""
        self.status_label.text = '[color=ffff00]搜索中...[/color]'
        self.search_btn.disabled = True

        # 模拟搜索（实际需要蓝牙API）
        from kivy.clock import Clock
        Clock.schedule_once(self._search_complete, 2.0)

    def _search_complete(self, *args):
        """搜索完成"""
        self.search_btn.disabled = False
        self.status_label.text = '[color=00ff00]搜索完成 - 模拟设备已发现[/color]'
        self.device_list_label.text = '[color=aaaaaa]示例设备:[/color]\n[color=888888]- 三仙归洞手机A[/color]\n[color=888888]- 三仙归洞手机B[/color]'

        # 在实际实现中，这里会列出发现的所有设备
        # 用户可以点击设备进行连接

    def start_multiplayer_game(self):
        """开始联机游戏"""
        if not self.connection_role:
            self.status_label.text = '[color=ff6666]请先选择角色[/color]'
            return

        # 导航到游戏界面
        game_screen = self.manager.get_screen('game')
        if self.connection_role == 'performer':
            game_screen.set_performer_mode()
        else:
            game_screen.set_audience_mode()

        game_screen.start_game('multiplayer')
        self.manager.current = 'game'

    def go_menu(self):
        """返回菜单"""
        self.manager.current = 'menu'

    def on_enter(self):
        """进入界面时重置状态"""
        self.is_connected = False
        self.connection_role = None
        self.status_label.text = '[color=888888]未连接[/color]'
        self.start_game_btn.disabled = True
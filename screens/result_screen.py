#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结果界面
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock


class ResultScreen(Screen):
    """结果界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.1, 0.08, 0.05, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_bg, pos=self._update_bg)
        self._create_ui()

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def _create_ui(self):
        """创建UI"""
        layout = BoxLayout(orientation='vertical', padding=40, spacing=30)

        # 结果标题
        self.result_title = Label(
            text='[color=ffd700]结果[/color]',
            font_size='48sp',
            bold=True,
            markup=True,
            size_hint_y=0.3
        )
        layout.add_widget(self.result_title)

        # 详细结果
        self.result_detail = Label(
            text='',
            font_size='24sp',
            markup=True,
            size_hint_y=0.2
        )
        layout.add_widget(self.result_detail)

        # 分数
        self.score_label = Label(
            text='',
            font_size='32sp',
            markup=True,
            size_hint_y=0.2
        )
        layout.add_widget(self.score_label)

        # 按钮区域
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=20)

        replay_btn = Button(
            text='再来一局',
            font_size='20sp',
            bold=True,
            background_color=(0.7, 0.3, 0.1, 1),
            color=(1, 0.9, 0.5, 1)
        )
        replay_btn.bind(on_press=lambda x: self.replay())
        btn_layout.add_widget(replay_btn)

        menu_btn = Button(
            text='返回菜单',
            font_size='20sp',
            background_color=(0.4, 0.4, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        menu_btn.bind(on_press=lambda x: self.go_menu())
        btn_layout.add_widget(menu_btn)

        layout.add_widget(btn_layout)

        self.add_widget(layout)

    def show_result(self, found, score):
        """显示结果"""
        if found:
            self.result_title.text = '[color=00ff00]找到了！[/color]'
            self.result_detail.text = '[color=aaffaa]恭喜您找到了隐藏的红色球！[/color]'
        else:
            self.result_title.text = '[color=ff6666]没找到...[/color]'
            self.result_detail.text = '[color=ffaaaa]球在另一个茶碗下面[/color]'

        self.score_label.text = f'[color=ffd700]当前分数: {score}[/color]'

        # 动画效果
        self._animate_result()

    def _animate_result(self):
        """结果动画"""
        # 简单的缩放动画
        from kivy.animation import Animation

        anim = Animation(size=(self.width * 1.1, self.height * 1.1), duration=0.2)
        anim &= Animation(size=(self.width, self.height), duration=0.2)
        anim.start(self.result_title)

    def replay(self):
        """再来一局"""
        game_screen = self.manager.get_screen('game')
        game_screen.reset_game()
        game_screen.start_shuffle()
        self.manager.current = 'game'

    def go_menu(self):
        """返回菜单"""
        self.manager.current = 'menu'
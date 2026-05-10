#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三仙归洞 - 中国传统技艺 shell game
单人模式 + 蓝牙双人联机模式
"""

__version__ = "1.0.0"

import os
import sys

# 设置工作目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'resizable', False)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.resources import resource_add_path

# 添加当前目录到资源路径
resource_add_path(os.path.dirname(__file__))

from screens.menu_screen import MenuScreen
from screens.game_screen import GameScreen
from screens.bluetooth_screen import BluetoothScreen
from screens.result_screen import ResultScreen
from bluetooth_service import BluetoothService

class SanxianApp(App):
    """三仙归洞游戏主类"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bluetooth_service = BluetoothService()
        self.game_state = {
            'mode': 'single',  # 'single' or 'performer' or 'audience'
            'ball_position': 0,  # 0, 1, 2
            'cup_positions': [0, 1, 2],
            'is_shuffling': False,
            'is_covered': False,
            'revealed_cups': [],
            'score': 0,
            'round': 0
        }

    def build(self):
        """构建应用"""
        Window.clearcolor = (0.09, 0.07, 0.05, 1)  # 深棕色背景

        sm = ScreenManager(transition=FadeTransition(duration=0.3))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(BluetoothScreen(name='bluetooth'))
        sm.add_widget(ResultScreen(name='result'))

        return sm

    def start_game(self, mode='single'):
        """开始游戏"""
        self.game_state['mode'] = mode
        self.game_state['score'] = 0
        self.game_state['round'] = 1
        self.reset_game()

    def reset_game(self):
        """重置游戏"""
        self.game_state['cup_positions'] = [0, 1, 2]
        self.game_state['is_shuffling'] = False
        self.game_state['is_covered'] = False
        self.game_state['revealed_cups'] = []

    def set_ball_position(self, pos):
        """设置球位置"""
        self.game_state['ball_position'] = pos

    def shuffle_cups(self):
        """洗牌动画"""
        self.game_state['is_shuffling'] = True

    def cover_ball(self):
        """盖住球"""
        self.game_state['is_covered'] = True
        self.game_state['is_shuffling'] = False

    def reveal_cup(self, cup_index):
        """揭示茶碗"""
        if cup_index not in self.game_state['revealed_cups']:
            self.game_state['revealed_cups'].append(cup_index)
            return cup_index == self.game_state['ball_position']
        return None

    def check_win(self):
        """检查是否全部揭示"""
        return len(self.game_state['revealed_cups']) == 3

    def get_bluetooth_service(self):
        """获取蓝牙服务"""
        return self.bluetooth_service


if __name__ == '__main__':
    SanxianApp().run()
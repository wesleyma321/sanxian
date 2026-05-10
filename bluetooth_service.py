#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝牙服务 - 处理双人联机
"""

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, StringProperty, ListProperty


class BluetoothService(EventDispatcher):
    """蓝牙服务类"""

    is_available = BooleanProperty(False)
    is_connected = BooleanProperty(False)
    device_name = StringProperty('')
    connection_role = StringProperty('')  # 'performer' or 'audience'

    # 发现的设备列表
    discovered_devices = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 检查蓝牙可用性
        self._check_bluetooth()

    def _check_bluetooth(self):
        """检查蓝牙是否可用"""
        # 在实际设备上需要使用bluetooth API
        # 这里简化为模拟检测
        try:
            # 尝试导入android bluetooth API
            import android
            self.is_available = True
        except:
            # 非Android环境，模拟为可用
            self.is_available = True

    def search_devices(self, callback=None):
        """搜索附近设备"""
        if not self.is_available:
            if callback:
                callback([])
            return []

        # 模拟搜索结果
        # 实际实现需要使用Android BluetoothAdapter
        devices = [
            {'name': '三仙归洞-手机A', 'address': '00:11:22:33:44:55'},
            {'name': '三仙归洞-手机B', 'address': '00:11:22:33:44:66'}
        ]

        self.discovered_devices = devices
        if callback:
            callback(devices)

        return devices

    def connect(self, device_address, role='performer'):
        """连接到设备"""
        if not self.is_available:
            return False

        self.connection_role = role

        # 模拟连接
        # 实际需要使用BluetoothSocket
        self.is_connected = True
        self.device_name = device_address

        return True

    def disconnect(self):
        """断开连接"""
        self.is_connected = False
        self.device_name = ''
        self.connection_role = ''

    def send_message(self, message):
        """发送消息"""
        if not self.is_connected:
            return False

        # 模拟发送
        # 实际需要通过BluetoothSocket发送
        return True

    def on_message_received(self, message):
        """收到消息时的回调"""
        # 处理接收到的消息
        pass


class GameMessage:
    """游戏消息类型"""

    # 游戏状态
    MSG_GAME_START = 'game_start'
    MSG_GAME_END = 'game_end'
    MSG_BALL_POSITION = 'ball_position'
    MSG_CUP_SHUFFLE = 'cup_shuffle'
    MSG_CUP_REVEAL = 'cup_reveal'
    MSG_ROUND_RESULT = 'round_result'

    @staticmethod
    def create_message(msg_type, data=None):
        """创建消息"""
        import json
        return json.dumps({
            'type': msg_type,
            'data': data or {}
        })

    @staticmethod
    def parse_message(json_str):
        """解析消息"""
        import json
        try:
            return json.loads(json_str)
        except:
            return None
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
茶碗组件 - 带3D阴影效果
"""

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Bezier
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale
from kivy.properties import NumericProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
import math


class CupWidget(Widget):
    """茶碗组件 - 3D效果"""

    # 位置索引
    position = NumericProperty(0)

    # 是否被揭开
    revealed = BooleanProperty(False)

    # 是否有球
    has_ball = BooleanProperty(False)

    # 动画状态
    is_shuffling = BooleanProperty(False)

    # 颜色配置
    cup_color = ListProperty([0.9, 0.85, 0.8, 1])  # 淡青色
    cup_pattern_color = ListProperty([0.3, 0.5, 0.7, 1])  # 青花瓷蓝

    # 内部状态
    _animation_progress = 0
    _shadow_offset = 15
    _3d_depth = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_graphics, pos=self._update_graphics)

    def _update_graphics(self, *args):
        """更新图形"""
        self.canvas.clear()
        with self.canvas:
            self._draw_cup()

    def _draw_cup(self):
        """绘制茶碗"""
        cx, cy = self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2
        width, height = self.size[0], self.size[1]

        # 如果是掀开状态，绘制掀开的碗
        if self.revealed:
            self._draw_lifted_cup(cx, cy, width, height)
            return

        # 3D效果 - 先绘制阴影
        self._draw_shadow(cx, cy, width, height)

        # 碗的主体（圆顶）
        self._draw_cup_body(cx, cy, width, height)

        # 青花瓷纹理
        self._draw_pattern(cx, cy, width, height)

    def _draw_shadow(self, cx, cy, width, height):
        """绘制3D阴影"""
        # 椭圆形阴影
        shadow_width = width * 0.7
        shadow_height = shadow_width * 0.3

        Color(0.1, 0.08, 0.06, 0.5)
        Ellipse(size=(shadow_width, shadow_height),
                pos=(cx - shadow_width/2, cy - height/2 - 5))

        # 渐变阴影效果
        Color(0.15, 0.12, 0.1, 0.3)
        Ellipse(size=(shadow_width * 0.8, shadow_height * 0.8),
                pos=(cx - shadow_width*0.4, cy - height/2 - 3))

    def _draw_cup_body(self, cx, cy, width, height):
        """绘制碗体 - 3D效果"""
        cup_width = width * 0.65
        cup_height = height * 0.6

        # 碗底（深色）
        Color(0.6, 0.55, 0.5, 1)
        Ellipse(size=(cup_width * 0.3, cup_width * 0.15),
                pos=(cx - cup_width*0.15, cy - height*0.15))

        # 碗体（渐变效果）
        # 底部深色
        Color(0.85, 0.8, 0.75, 1)
        Ellipse(size=(cup_width, cup_height * 0.4),
                pos=(cx - cup_width/2, cy - height*0.2))

        # 中间主色
        Color(0.92, 0.88, 0.85, 1)
        Ellipse(size=(cup_width * 0.95, cup_height * 0.35),
                pos=(cx - cup_width*0.475, cy - height*0.1))

        # 顶部高光
        Color(0.95, 0.92, 0.9, 1)
        Ellipse(size=(cup_width * 0.8, cup_height * 0.2),
                pos=(cx - cup_width*0.4, cy + height*0.05))

        # 碗口边缘
        Color(0.88, 0.84, 0.8, 1)
        Ellipse(size=(cup_width * 0.7, cup_height * 0.15),
                pos=(cx - cup_width*0.35, cy + height*0.15))

    def _draw_pattern(self, cx, cy, width, height):
        """绘制青花瓷图案"""
        cup_width = width * 0.65
        cup_height = height * 0.6

        # 装饰纹
        Color(0.3, 0.5, 0.7, 0.8)

        # 碗身花纹
        for i in range(3):
            offset_y = -height * 0.1 + i * height * 0.08
            Ellipse(size=(cup_width * 0.4, cup_height * 0.08),
                    pos=(cx - cup_width*0.2, cy + offset_y),
                    segments=20)

        # 碗口花纹
        Color(0.25, 0.45, 0.65, 0.6)
        Ellipse(size=(cup_width * 0.5, cup_height * 0.1),
                pos=(cx - cup_width*0.25, cy + height*0.12),
                segments=30)

    def _draw_lifted_cup(self, cx, cy, width, height):
        """绘制掀开的碗"""
        cup_width = width * 0.65
        cup_height = height * 0.6

        # 如果有球，绘制球
        if self.has_ball:
            self._draw_ball(cx, cy - height*0.1, width * 0.25)

        # 碗被掀开倾斜的效果
        Color(0.88, 0.84, 0.8, 0.7)

        # 碗的边缘（倾斜）
        from kivy.graphics import Rotate
        PushMatrix()
        Translate(cx, cy + height*0.3, 0)
        Rotate(angle=45, axis=(0, 0, 1))
        Color(0.85, 0.8, 0.75, 0.5)
        Ellipse(size=(cup_width * 0.8, cup_height * 0.3))
        PopMatrix()

    def _draw_ball(self, cx, cy, radius):
        """绘制红色球 - 3D效果"""
        # 球体阴影
        Color(0.2, 0.1, 0.1, 0.4)
        Ellipse(size=(radius * 1.5, radius * 0.4),
                pos=(cx - radius*0.75, cy - radius*1.2))

        # 球体渐变 - 深色
        Color(0.7, 0.1, 0.1, 1)
        Ellipse(size=(radius*2, radius*2),
                pos=(cx - radius, cy - radius))

        # 球体渐变 - 主色
        Color(0.9, 0.15, 0.15, 1)
        Ellipse(size=(radius*1.7, radius*1.7),
                pos=(cx - radius*0.85, cy - radius*0.85))

        # 高光
        Color(1, 0.5, 0.5, 0.8)
        Ellipse(size=(radius*0.6, radius*0.6),
                pos=(cx - radius*0.3, cy - radius*0.3))

        # 反光
        Color(1, 0.8, 0.8, 0.4)
        Ellipse(size=(radius*0.3, radius*0.3),
                pos=(cx - radius*0.15, cy - radius*0.15))

    def animate_shuffle(self, target_pos, duration=0.3):
        """洗牌动画"""
        anim = Animation(pos=target_pos, duration=duration, t='out_quad')
        anim.start(self)

    def animate_lift(self):
        """掀开动画"""
        anim = Animation(revealed=True, duration=0.5, t='bounce_out')
        anim.start(self)

    def reset(self):
        """重置状态"""
        self.revealed = False
        self.has_ball = False
        self._animation_progress = 0
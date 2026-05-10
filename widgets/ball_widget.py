#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红色球组件 - 带光泽效果
"""

from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.properties import NumericProperty, ListProperty


class BallWidget(Widget):
    """红色球组件"""

    # 球大小
    ball_size = NumericProperty(50)

    # 颜色配置
    ball_color = ListProperty([0.9, 0.1, 0.1, 1])  # 红色
    highlight_color = ListProperty([1, 0.5, 0.5, 0.8])  # 高光

    _glow_effect = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_graphics, pos=self._update_graphics)

    def _update_graphics(self, *args):
        """更新图形"""
        self.canvas.clear()
        with self.canvas:
            self._draw_ball()

    def _draw_ball(self):
        """绘制3D红色球"""
        cx, cy = self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2
        radius = min(self.size[0], self.size[1]) / 2

        # 外发光效果
        if self._glow_effect > 0:
            glow_alpha = self._glow_effect * 0.3
            Color(1, 0.2, 0.2, glow_alpha)
            Ellipse(size=(radius * 2.5, radius * 2.5),
                    pos=(cx - radius * 1.25, cy - radius * 1.25))

        # 球体阴影
        Color(0.15, 0.05, 0.05, 0.5)
        Ellipse(size=(radius * 1.8, radius * 0.5),
                pos=(cx - radius * 0.9, cy - radius * 1.5))

        # 球体 - 底层深色
        Color(0.6, 0.05, 0.05, 1)
        Ellipse(size=(radius * 2, radius * 2),
                pos=(cx - radius, cy - radius))

        # 球体 - 中层
        Color(0.8, 0.1, 0.1, 1)
        Ellipse(size=(radius * 1.8, radius * 1.8),
                pos=(cx - radius * 0.9, cy - radius * 0.9))

        # 球体 - 主色
        Color(0.9, 0.15, 0.15, 1)
        Ellipse(size=(radius * 1.5, radius * 1.5),
                pos=(cx - radius * 0.75, cy - radius * 0.75))

        # 球体 - 亮色
        Color(0.95, 0.2, 0.2, 1)
        Ellipse(size=(radius * 1.2, radius * 1.2),
                pos=(cx - radius * 0.6, cy - radius * 0.6))

        # 高光点
        Color(1, 0.6, 0.6, 0.9)
        Ellipse(size=(radius * 0.5, radius * 0.5),
                pos=(cx - radius * 0.25, cy - radius * 0.25))

        # 次高光
        Color(1, 0.8, 0.8, 0.5)
        Ellipse(size=(radius * 0.25, radius * 0.25),
                pos=(cx - radius * 0.125, cy - radius * 0.125))

    def animate_glow(self):
        """发光动画"""
        from kivy.animation import Animation
        anim = Animation(_glow_effect=1, duration=0.5)
        anim &= Animation(_glow_effect=0, duration=0.5)
        anim.repeat = True
        anim.start(self)

    def stop_glow(self):
        """停止发光"""
        self._glow_effect = 0
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏动画控制器 - 改进版
"""

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, PushMatrix, PopMatrix, Translate, Rotate
from kivy.uix.widget import Widget
import random
import math


class ShuffleAnimator:
    """洗牌动画控制器"""

    def __init__(self, cups, ball, on_complete=None):
        self.cups = cups
        self.ball = ball
        self.on_complete = on_complete
        self.positions = [0.15, 0.5, 0.85]  # 初始位置
        self.is_animating = False

    def start_shuffle(self, count=10, speed=0.25):
        """开始洗牌动画"""
        if self.is_animating:
            return

        self.is_animating = True
        self.shuffle_count = count
        self.speed = speed
        self._do_shuffle()

    def _do_shuffle(self):
        """执行洗牌"""
        if self.shuffle_count <= 0:
            self._finish_shuffle()
            return

        self.shuffle_count -= 1

        # 随机选择两个茶碗交换
        idx1, idx2 = random.sample([0, 1, 2], 2)

        # 计算新位置
        pos1 = {'center_x': self.positions[idx2], 'center_y': 0.55}
        pos2 = {'center_x': self.positions[idx1], 'center_y': 0.55}

        # 创建动画
        cup1_anim = Animation(pos_hint=pos1, duration=self.speed, t='out_quad')
        cup2_anim = Animation(pos_hint=pos2, duration=self.speed, t='out_quad')

        # 交换位置记录
        self.positions[idx1], self.positions[idx2] = self.positions[idx2], self.positions[idx1]

        # 启动动画
        cup1_anim.start(self.cups[idx1])
        cup2_anim.start(self.cups[idx2])

        # 继续洗牌
        Clock.schedule_once(lambda dt: self._do_shuffle(), self.speed + 0.05)

    def _finish_shuffle(self):
        """洗牌完成"""
        self.is_animating = False
        if self.on_complete:
            self.on_complete()


class CupLiftAnimator:
    """茶碗掀开动画"""

    def __init__(self, cup_widget):
        self.cup = cup_widget

    def animate(self, duration=0.5):
        """执行掀开动画"""
        # 掀开动画：缩放 + 旋转效果
        anim = Animation(
            scale_x=1.1,
            scale_y=0.8,
            opacity=0.9,
            duration=duration/2,
            t='bounce_out'
        )
        anim &= Animation(
            scale_x=1.0,
            scale_y=1.0,
            duration=duration/2,
            t='bounce_in'
        )
        anim.start(self.cup)


class BallRevealAnimator:
    """球揭示动画"""

    def __init__(self, ball_widget):
        self.ball = ball_widget

    def animate_found(self):
        """找到球的发光动画"""
        from kivy.graphics import Color

        # 发光效果
        original_color = self.ball.color[:] if hasattr(self.ball, 'color') else [1, 0.2, 0.2, 1]

        # 创建一系列动画
        anim = Animation(opacity=1, duration=0.3)

        def pulse_glow(dt):
            # 脉冲发光
            glow = 1.0
            direction = -0.05

            def update(dt):
                nonlocal glow, direction
                glow += direction
                if glow <= 0.5 or glow >= 1.5:
                    direction *= -1
                self.ball._glow_effect = (glow - 0.5) / 0.5  # 归一化

            return update

        glow_clock = Clock.schedule_interval(pulse_glow(), 0.05)

        def stop_pulse(dt):
            glow_clock.cancel()
            self.ball._glow_effect = 0

        Clock.schedule_once(stop_pulse, 2.0)


class ParticleEffect:
    """粒子效果（用于揭示时的光效）"""

    def __init__(self, widget, pos):
        self.widget = widget
        self.pos = pos
        self.particles = []
        self.container = Widget(pos=pos, size=widget.size)

    def start(self, count=20):
        """启动粒子效果"""
        from kivy.graphics import Color, Ellipse

        for i in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            size = random.uniform(5, 15)

            particle = {
                'x': self.pos[0] + self.widget.size[0] / 2,
                'y': self.pos[1] + self.widget.size[1] / 2,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': size,
                'life': 1.0,
                'color': self._get_random_gold_color()
            }
            self.particles.append(particle)

        # 更新粒子
        def update_particles(dt):
            # 更新每个粒子
            for p in self.particles[:]:
                p['x'] += p['vx'] * dt
                p['y'] += p['vy'] * dt
                p['life'] -= dt * 0.5
                p['vy'] -= 100 * dt  # 重力效果

                if p['life'] <= 0:
                    self.particles.remove(p)

            # 绘制粒子
            with self.container.canvas:
                for p in self.particles:
                    Color(p['color'][0], p['color'][1], p['color'][2], p['life'])
                    Ellipse(size=(p['size'], p['size']), pos=(p['x'] - p['size']/2, p['y'] - p['size']/2))

            if not self.particles:
                return False

            return True

        Clock.schedule_interval(update_particles, 1/60)
        return self.container

    def _get_random_gold_color(self):
        """获取随机金色"""
        return [
            random.uniform(0.9, 1.0),  # R
            random.uniform(0.7, 0.9),  # G
            random.uniform(0.2, 0.4),  # B
            1.0
        ]


class Cup3DRenderer:
    """3D茶碗渲染器"""

    @staticmethod
    def draw_3d_cup(canvas, cx, cy, width, height, revealed=False, has_ball=False):
        """绘制3D效果茶碗"""
        cup_width = width * 0.7
        cup_height = height * 0.5

        with canvas:
            # 3D阴影效果 - 底部阴影
            Color(0.08, 0.06, 0.04, 0.6)
            Ellipse(
                size=(cup_width * 1.2, cup_width * 0.4),
                pos=(cx - cup_width * 0.6, cy - height * 0.6)
            )

            # 碗体 - 底部深色
            Color(0.5, 0.45, 0.4, 1)
            Ellipse(
                size=(cup_width * 0.8, cup_height * 0.3),
                pos=(cx - cup_width * 0.4, cy - height * 0.3)
            )

            # 碗体 - 主色（渐变）
            Color(0.75, 0.7, 0.65, 1)
            Ellipse(
                size=(cup_width * 0.9, cup_height * 0.35),
                pos=(cx - cup_width * 0.45, cy - height * 0.15)
            )

            # 碗体 - 亮色
            Color(0.88, 0.84, 0.8, 1)
            Ellipse(
                size=(cup_width * 0.7, cup_height * 0.25),
                pos=(cx - cup_width * 0.35, cy - height * 0.05)
            )

            # 碗口 - 高光
            Color(0.92, 0.88, 0.85, 1)
            Ellipse(
                size=(cup_width * 0.6, cup_height * 0.2),
                pos=(cx - cup_width * 0.3, cy + height * 0.05)
            )

            # 青花瓷装饰
            Cup3DRenderer._draw_pattern(canvas, cx, cy, cup_width, cup_height)

            # 如果有球且已揭示，绘制球
            if has_ball and revealed:
                Cup3DRenderer._draw_3d_ball(canvas, cx, cy - height * 0.1, width * 0.2)

    @staticmethod
    def _draw_pattern(canvas, cx, cy, cup_width, cup_height):
        """绘制青花瓷图案"""
        # 碗身花纹
        Color(0.25, 0.45, 0.65, 0.7)
        for i in range(-1, 2):
            Ellipse(
                size=(cup_width * 0.3, cup_height * 0.12),
                pos=(cx - cup_width * 0.15 + i * cup_width * 0.25, cy - height * 0.12),
                segments=20
            )

        # 碗口装饰线
        Color(0.2, 0.4, 0.6, 0.5)
        Ellipse(
            size=(cup_width * 0.55, cup_height * 0.1),
            pos=(cx - cup_width * 0.275, cy + height * 0.08),
            segments=30
        )

    @staticmethod
    def _draw_3d_ball(canvas, cx, cy, radius):
        """绘制3D红色球"""
        # 球体阴影
        Color(0.15, 0.05, 0.05, 0.5)
        Ellipse(
            size=(radius * 2, radius * 0.5),
            pos=(cx - radius, cy - radius * 1.5)
        )

        # 球体层
        Color(0.6, 0.05, 0.05, 1)
        Ellipse(size=(radius * 2, radius * 2), pos=(cx - radius, cy - radius))

        Color(0.75, 0.1, 0.1, 1)
        Ellipse(size=(radius * 1.7, radius * 1.7), pos=(cx - radius * 0.85, cy - radius * 0.85))

        Color(0.85, 0.15, 0.15, 1)
        Ellipse(size=(radius * 1.4, radius * 1.4), pos=(cx - radius * 0.7, cy - radius * 0.7))

        # 高光
        Color(1, 0.5, 0.5, 0.9)
        Ellipse(size=(radius * 0.5, radius * 0.5), pos=(cx - radius * 0.25, cy - radius * 0.25))

        Color(1, 0.7, 0.7, 0.5)
        Ellipse(size=(radius * 0.25, radius * 0.25), pos=(cx - radius * 0.125, cy - radius * 0.125))
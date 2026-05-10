#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动画效果模块
"""

from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.clock import Clock
import math


def animate_shuffle(widget, target_pos, duration=0.3, callback=None):
    """茶碗洗牌动画"""
    anim = Animation(pos_hint=target_pos, duration=duration, t='in_out_quad')
    if callback:
        anim.bind(on_complete=lambda *args: callback())
    anim.start(widget)
    return anim


def animate_lift(widget, duration=0.5, callback=None):
    """掀开茶碗动画"""
    anim = Animation(
        revealed=True,
        height=widget.height * 1.1,
        duration=duration,
        t='bounce_out'
    )
    if callback:
        anim.bind(on_complete=lambda *args: callback())
    anim.start(widget)
    return anim


def animate_ball_glow(ball_widget):
    """球发光动画"""
    glow = 0
    direction = 1

    def update_glow(dt):
        nonlocal glow, direction
        glow += direction * 0.05
        if glow >= 1:
            glow = 1
            direction = -1
        elif glow <= 0:
            glow = 0
            direction = 1
        ball_widget._glow_effect = glow

    return Clock.schedule_interval(update_glow, 0.05)


def animate_reveal_effect(widget, duration=1.0):
    """揭示时的光效动画"""
    from kivy.graphics import Color, Rectangle
    from kivy.uix.widget import Widget

    effect = Widget(size=widget.size, pos=widget.pos)
    widget.add_widget(effect)

    alpha = 0.8

    def fade_out(dt):
        nonlocal alpha
        alpha -= 0.02
        if alpha <= 0:
            widget.remove_widget(effect)
            return False
        return True

    with effect.canvas:
        from kivy.graphics import Color
        Color(1, 0.9, 0.5, alpha)

    Clock.schedule_interval(fade_out, 0.02)
    return effect


def animate_score_change(label_widget, new_score):
    """分数变化动画"""
    # 数字跳动效果
    from kivy.animation import Animation

    anim = Animation(font_size='36sp', duration=0.1)
    anim &= Animation(font_size='28sp', duration=0.1)
    anim.start(label_widget)


def create_shuffle_sequence(cups, ball_position, shuffle_count=10, speed=0.3):
    """创建洗牌序列动画"""
    animations = []
    positions = [0.15, 0.5, 0.85]  # 三个茶碗的位置

    for i in range(shuffle_count):
        # 随机选择两个茶碗交换
        idx1, idx2 = __import__('random').sample([0, 1, 2], 2)

        # 创建交换动画
        cup1_anim = animate_shuffle(cups[idx1], {'center_x': positions[idx2], 'center_y': 0.55}, speed)
        cup2_anim = animate_shuffle(cups[idx2], {'center_x': positions[idx1], 'center_y': 0.55}, speed)

        animations.append((cup1_anim, cup2_anim))

    return animations


def interpolate_position(start, end, t):
    """位置插值"""
    return {
        'center_x': start.get('center_x', 0.5) + (end.get('center_x', 0.5) - start.get('center_x', 0.5)) * t,
        'center_y': start.get('center_y', 0.5) + (end.get('center_y', 0.5) - start.get('center_y', 0.5)) * t
    }
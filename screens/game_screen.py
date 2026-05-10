#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏界面 - 核心游戏逻辑（修复版）
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.text import LabelBase
import random
import math

from utils.animator import ShuffleAnimator, Cup3DRenderer


class GameScreen(Screen):
    """游戏界面"""

    # 游戏状态
    game_mode = 'single'
    ball_position = 0
    cup_positions = [0, 1, 2]
    is_shuffling = False
    is_covered = False
    revealed_cups = []
    score = 0
    round_num = 1

    # 动画
    shuffle_animator = None

    # 组件引用
    cup_widgets = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 背景
        with self.canvas.before:
            Color(0.12, 0.08, 0.05, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_bg, pos=self._update_bg)
        self._create_ui()

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def _create_ui(self):
        """创建游戏UI"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=8)

        # 顶部状态栏
        top_bar = BoxLayout(size_hint_y=0.08, padding=10)
        self.round_label = Label(text='回合: 1', font_size='16sp', color=(1, 0.9, 0.5, 1))
        self.title_label = Label(text='[color=ffd700]三仙归洞[/color]', font_size='22sp',
                                markup=True, bold=True)
        self.score_label = Label(text='分数: 0', font_size='16sp', color=(1, 0.9, 0.5, 1))
        top_bar.add_widget(self.round_label)
        top_bar.add_widget(self.title_label)
        top_bar.add_widget(self.score_label)
        main_layout.add_widget(top_bar)

        # 提示标签
        self.hint_label = Label(
            text='[color=888888]点击"开始游戏"按钮[/color]',
            font_size='14sp',
            markup=True,
            size_hint_y=0.05
        )
        main_layout.add_widget(self.hint_label)

        # 游戏区域
        game_area = GameAreaWidget(size_hint_y=0.65)
        main_layout.add_widget(game_area)
        self.game_area = game_area

        # 控制按钮区域
        control_area = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.12,
            padding=15,
            spacing=20
        )

        self.start_btn = Button(
            text='开始游戏',
            font_size='18sp',
            bold=True,
            background_color=(0.7, 0.35, 0.1, 1),
            color=(1, 0.9, 0.5, 1)
        )
        self.start_btn.bind(on_press=lambda x: self.start_shuffle())
        control_area.add_widget(self.start_btn)

        self.reset_btn = Button(
            text='重新开始',
            font_size='16sp',
            background_color=(0.4, 0.4, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        self.reset_btn.bind(on_press=lambda x: self.reset_game())
        control_area.add_widget(self.reset_btn)

        main_layout.add_widget(control_area)

        # 底部返回按钮
        bottom_bar = BoxLayout(size_hint_y=0.05, padding=5)
        back_btn = Button(text='返回菜单', font_size='14sp', size_hint_x=0.4)
        back_btn.bind(on_press=lambda x: self.go_menu())
        bottom_bar.add_widget(back_btn)
        main_layout.add_widget(bottom_bar)

        self.add_widget(main_layout)

    def start_game(self, mode='single'):
        """开始游戏"""
        self.game_mode = mode
        self.reset_game()

    def start_shuffle(self):
        """开始洗牌动画"""
        if self.is_shuffling or self.is_covered:
            return

        self.is_shuffling = True
        self.start_btn.text = '洗牌中...'
        self.start_btn.disabled = True
        self.hint_label.text = '[color=ffff00]洗牌进行中...[/color]'

        # 重置揭示状态
        self.revealed_cups = []
        self.game_area.reset_cups()

        # 隐藏球
        self.game_area.hide_ball()

        # 随机选择球的位置
        self.ball_position = random.randint(0, 2)

        # 创建洗牌动画
        self.shuffle_animator = ShuffleAnimator(
            cups=self.game_area.cup_widgets,
            ball=self.game_area.ball_widget,
            on_complete=self._on_shuffle_complete
        )
        self.shuffle_animator.start_shuffle(count=random.randint(8, 12), speed=0.25)

    def _on_shuffle_complete(self):
        """洗牌完成回调"""
        self.is_shuffling = False
        self.hint_label.text = '[color=00ff00]洗牌完成，请等待...[/color]'

        # 延迟盖球
        Clock.schedule_once(lambda dt: self._cover_ball(), 0.8)

    def _cover_ball(self):
        """盖住球"""
        self.is_covered = True
        self.start_btn.text = '请选择茶碗'
        self.start_btn.disabled = False

        # 显示球（在表演者模式下可见）
        self.game_area.show_ball()

        # 在表演者模式下高亮显示球的位置
        if self.game_mode == 'performer':
            self.game_area.highlight_ball_position(self.ball_position)

        # 观众模式下隐藏球
        if self.game_mode == 'audience':
            self.game_area.hide_ball()

        self.hint_label.text = '[color=aaffaa]请点击茶碗找出红色球！[/color]'

    def on_cup_tap(self, cup_index):
        """点击茶碗"""
        if not self.is_covered or cup_index in self.revealed_cups:
            return

        self.hint_label.text = '[color=ffff00]揭晓中...[/color]'

        # 揭示茶碗
        found = self.game_area.reveal_cup(cup_index, self.ball_position)
        self.revealed_cups.append(cup_index)

        if found:
            # 找到了！
            self.score += 10
            self.update_score()
            self.hint_label.text = '[color=00ff00]太棒了！找到了！+10分[/color]'
            Clock.schedule_once(lambda dt: self.show_result(True), 1.0)
        else:
            # 没找到
            if len(self.revealed_cups) >= 2:
                self.score = max(0, self.score - 5)
                self.update_score()
                self.hint_label.text = '[color=ff6666]没找到...-5分[/color]'
                Clock.schedule_once(lambda dt: self.show_result(False), 1.0)

    def update_score(self):
        """更新分数显示"""
        self.score_label.text = f'分数: {self.score}'

    def show_result(self, found):
        """显示结果"""
        result_screen = self.manager.get_screen('result')
        result_screen.show_result(found, self.score)
        self.manager.current = 'result'

    def reset_game(self):
        """重置游戏"""
        self.is_shuffling = False
        self.is_covered = False
        self.revealed_cups = []
        self.ball_position = 0

        self.game_area.reset()

        self.start_btn.text = '开始游戏'
        self.start_btn.disabled = False
        self.hint_label.text = '[color=888888]点击"开始游戏"按钮[/color]'
        self.update_score()

    def go_menu(self):
        """返回菜单"""
        self.reset_game()
        self.manager.current = 'menu'

    def set_performer_mode(self):
        """设置为表演者模式"""
        self.game_mode = 'performer'
        self.hint_label.text = '[color=ffaaaa]表演者模式：球位置已标注[/color]'

    def set_audience_mode(self):
        """设置为观众模式"""
        self.game_mode = 'audience'
        self.hint_label.text = '[color=aaffaa]观众模式：找出球的位置！[/color]'


class GameAreaWidget(Widget):
    """游戏区域组件"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cup_widgets = []
        self.ball_widget = None
        self._create_game_elements()

        with self.canvas:
            # 木质桌面背景
            Color(0.2, 0.12, 0.08, 1)
            Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, *args):
        """更新画布"""
        self.canvas.clear()
        with self.canvas:
            Color(0.18, 0.1, 0.06, 1)
            Rectangle(size=self.size, pos=self.pos)
        self._draw_game()

    def _create_game_elements(self):
        """创建游戏元素"""
        # 创建三个茶碗
        positions = [0.18, 0.5, 0.82]
        for i, x_pos in enumerate(positions):
            cup = CupGameWidget(
                size_hint=(0.28, 0.35),
                pos_hint={'center_x': x_pos, 'center_y': 0.55},
                index=i
            )
            cup.bind(on_tap=self._on_cup_tap)
            self.cup_widgets.append(cup)
            self.add_widget(cup)

        # 创建球
        self.ball_widget = BallGameWidget(
            size_hint=(0.12, 0.12),
            pos_hint={'center_x': 0.18, 'center_y': 0.42}
        )
        self.add_widget(self.ball_widget)

    def _draw_game(self):
        """绘制游戏场景"""
        pass  # 画布已在__init__中绘制

    def _on_cup_tap(self, cup_widget):
        """茶碗点击回调"""
        # 获取屏幕管理器并调用on_cup_tap
        screen = self.parent.parent.parent  # 嵌套层级
        if hasattr(screen, 'on_cup_tap'):
            screen.on_cup_tap(cup_widget.index)

    def reset_cups(self):
        """重置茶碗状态"""
        for cup in self.cup_widgets:
            cup.reset()

    def hide_ball(self):
        """隐藏球"""
        self.ball_widget.opacity = 0

    def show_ball(self):
        """显示球"""
        self.ball_widget.opacity = 1

    def highlight_ball_position(self, ball_pos):
        """高亮显示球位置（表演者模式）"""
        # 在表演者模式下，让对应茶碗显示特殊标记
        for i, cup in enumerate(self.cup_widgets):
            if cup.index == ball_pos:
                cup.show_ball_marker()

    def reveal_cup(self, cup_index, ball_position):
        """揭示茶碗"""
        cup = self.cup_widgets[cup_index]
        found = cup.reveal(has_ball=(cup.index == ball_position))
        return found

    def reset(self):
        """重置游戏区域"""
        positions = [0.18, 0.5, 0.82]
        for i, cup in enumerate(self.cup_widgets):
            cup.pos_hint = {'center_x': positions[i], 'center_y': 0.55}
            cup.index = i
            cup.reset()

        self.ball_widget.pos_hint = {'center_x': 0.18, 'center_y': 0.42}
        self.ball_widget.opacity = 1


class CupGameWidget(Widget):
    """茶碗游戏组件"""

    index = NumericProperty(0)
    _revealed = BooleanProperty(False)
    _has_ball = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_graphics, pos=self._update_graphics)
        self._draw_cup()

    def _update_graphics(self, *args):
        self.canvas.clear()
        self._draw_cup()

    def _draw_cup(self):
        """绘制3D茶碗"""
        cx, cy = self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2
        width, height = self.size[0], self.size[1]
        cup_width = width * 0.75
        cup_height = height * 0.5

        with self.canvas:
            # 3D阴影
            Color(0.05, 0.03, 0.02, 0.7)
            Ellipse(size=(cup_width * 1.1, cup_width * 0.35),
                    pos=(cx - cup_width * 0.55, cy - height * 0.55))

            # 碗体 - 底部
            Color(0.55, 0.48, 0.42, 1)
            Ellipse(size=(cup_width * 0.7, cup_height * 0.25),
                    pos=(cx - cup_width * 0.35, cy - height * 0.25))

            # 碗体 - 中层
            Color(0.75, 0.68, 0.62, 1)
            Ellipse(size=(cup_width * 0.85, cup_height * 0.3),
                    pos=(cx - cup_width * 0.425, cy - height * 0.1))

            # 碗体 - 上层
            Color(0.88, 0.82, 0.76, 1)
            Ellipse(size=(cup_width * 0.75, cup_height * 0.25),
                    pos=(cx - cup_width * 0.375, cy + height * 0.02))

            # 碗口 - 边缘
            Color(0.92, 0.88, 0.82, 1)
            Ellipse(size=(cup_width * 0.6, cup_height * 0.18),
                    pos=(cx - cup_width * 0.3, cy + height * 0.12))

            # 青花瓷装饰纹
            Color(0.3, 0.5, 0.65, 0.6)
            Ellipse(size=(cup_width * 0.5, cup_height * 0.1),
                    pos=(cx - cup_width * 0.25, cy - height * 0.05),
                    segments=25)
            Ellipse(size=(cup_width * 0.4, cup_height * 0.08),
                    pos=(cx - cup_width * 0.2, cy + height * 0.1),
                    segments=25)

        # 如果已揭示，显示球
        if self._revealed:
            self._draw_revealed_content(cx, cy, width, height)

    def _draw_revealed_content(self, cx, cy, width, height):
        """绘制揭示后的内容"""
        with self.canvas:
            if self._has_ball:
                # 绘制红色球
                radius = width * 0.2
                # 球阴影
                Color(0.1, 0.02, 0.02, 0.5)
                Ellipse(size=(radius * 1.8, radius * 0.5),
                        pos=(cx - radius * 0.9, cy - radius * 1.2))
                # 球体
                Color(0.7, 0.08, 0.08, 1)
                Ellipse(size=(radius * 2, radius * 2), pos=(cx - radius, cy - radius))
                Color(0.85, 0.12, 0.12, 1)
                Ellipse(size=(radius * 1.6, radius * 1.6),
                        pos=(cx - radius * 0.8, cy - radius * 0.8))
                # 高光
                Color(1, 0.5, 0.5, 0.9)
                Ellipse(size=(radius * 0.5, radius * 0.5),
                        pos=(cx - radius * 0.25, cy - radius * 0.25))

    def reveal(self, has_ball=False):
        """揭示茶碗"""
        self._revealed = True
        self._has_ball = has_ball
        self._update_graphics()
        return has_ball

    def show_ball_marker(self):
        """显示球标记（表演者模式）"""
        # 在茶碗上显示一个小红点标记
        pass

    def reset(self):
        """重置茶碗"""
        self._revealed = False
        self._has_ball = False
        self._update_graphics()

    def on_tap(self):
        """点击事件"""
        self.callback()


class BallGameWidget(Widget):
    """红色球游戏组件"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_graphics, pos=self._update_graphics)

    def _update_graphics(self, *args):
        self.canvas.clear()
        self._draw_ball()

    def _draw_ball(self):
        """绘制3D红色球"""
        cx, cy = self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1]/2
        radius = min(self.size[0], self.size[1]) / 2

        with self.canvas:
            # 阴影
            Color(0.1, 0.02, 0.02, 0.5)
            Ellipse(size=(radius * 2, radius * 0.5),
                    pos=(cx - radius, cy - radius * 1.3))

            # 球体层
            Color(0.65, 0.05, 0.05, 1)
            Ellipse(size=(radius * 2, radius * 2), pos=(cx - radius, cy - radius))
            Color(0.8, 0.1, 0.1, 1)
            Ellipse(size=(radius * 1.7, radius * 1.7),
                    pos=(cx - radius * 0.85, cy - radius * 0.85))
            Color(0.9, 0.15, 0.15, 1)
            Ellipse(size=(radius * 1.4, radius * 1.4),
                    pos=(cx - radius * 0.7, cy - radius * 0.7))

            # 高光
            Color(1, 0.55, 0.55, 0.9)
            Ellipse(size=(radius * 0.5, radius * 0.5),
                    pos=(cx - radius * 0.25, cy - radius * 0.25))
            Color(1, 0.75, 0.75, 0.6)
            Ellipse(size=(radius * 0.25, radius * 0.25),
                    pos=(cx - radius * 0.125, cy - radius * 0.125))
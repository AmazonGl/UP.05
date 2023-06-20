import arcade
import arcade.gui
from arcade import load_texture
from arcade.experimental.uislider import UISlider
from arcade.gui import UIManager, UIAnchorWidget, UILabel
from arcade.gui.events import UIOnChangeEvent
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
import random

WIDTH = 800
HEIGHT = 600
CUBE_SIZE = 50
ENEMY_MOVEMENT_SPEED = 2
ENEMY_MOVEMENT_BOUNDS_LEFT = 100
ENEMY_MOVEMENT_BOUNDS_RIGHT = 700
CUBE_WIDTH = 80
CUBE_HEIGHT = 40
CUBE_DEPTH = 40

wasd = False

volume = 10

background = arcade.load_texture("images/backgrounds/background.png")

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        width, height = self.window.get_size()

        if width == 800:
            width_button_scale = 300
            height_button_scale = 50
        else:
            width_button_scale = 500
            height_button_scale = 70

        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Играть", width=width_button_scale, height=height_button_scale)
        self.v_box.add(start_button.with_space_around(bottom=20))

        rules_button = arcade.gui.UIFlatButton(text="Правила", width=width_button_scale, height=height_button_scale)
        self.v_box.add(rules_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Настройки", width=width_button_scale, height=height_button_scale)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        exit_button = arcade.gui.UIFlatButton(text="Выход", width=width_button_scale, height=height_button_scale)
        self.v_box.add(exit_button.with_space_around(bottom=20))

        start_button.on_click = self.on_click_start

        rules_button.on_click = self.on_click_rules

        settings_button.on_click = self.on_click_settings

        exit_button.on_click = self.on_click_exit

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        self.click = arcade.Sound("sounds/effects/songfon.mp3")

    def on_click_start(self, event):
        global volume
        self.click.play(volume=volume)
        qbert_game_view = LevelView()
        # qbert_game_view.setup()
        self.window.show_view(qbert_game_view)

    def on_click_settings(self, event):
        global volume
        settings_view = SettingsView()
        self.window.show_view(settings_view)
        self.click.play(volume=volume)

    def on_click_exit(self, event):
        arcade.exit()

    def on_click_rules(self, event):
        rules_view = RulesVIew()
        self.window.show_view(rules_view)

    def on_draw(self):
        width, height = self.window.get_size()
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, width, height, background)
        if width == 800:
            arcade.draw_text("Q*bert", 400, 500,
                            arcade.color.WHITE, font_size=50, anchor_x="center", font_name="Arial")
        elif width == 1920:
            arcade.draw_text("Q*bert", width/2, 900,
                             arcade.color.WHITE, font_size=110, anchor_x="center", font_name="Arial")
        elif width == 2560:
            arcade.draw_text("Q*bert", width/2, 1100,
                             arcade.color.WHITE, font_size=150, anchor_x="center", font_name="Arial")
        self.manager.draw()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

class LevelView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        width, height = self.window.get_size()

        if width == 800:
            width_button_scale = 300
            height_button_scale = 50
        else:
            width_button_scale = 500
            height_button_scale = 70

        self.v_box = arcade.gui.UIBoxLayout()

        level1_button = arcade.gui.UIFlatButton(text="Уровень 1", width=width_button_scale, height=height_button_scale)
        self.v_box.add(level1_button.with_space_around(bottom=20))

        level2_button = arcade.gui.UIFlatButton(text="Уровень 2", width=width_button_scale, height=height_button_scale)
        self.v_box.add(level2_button.with_space_around(bottom=20))
        level1_button.on_click = self.on_click_level1

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        self.click = arcade.Sound("sounds/effects/songfon.mp3")
    def on_click_level1(self, event):
        global volume
        self.click.play(volume=volume)
        qbert_game_view = QbertGameView()
        qbert_game_view.setup()
        self.window.show_view(qbert_game_view)

    def on_draw(self):
        width, height = self.window.get_size()
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, width, height, background)
        if width == 800:
            arcade.draw_text("Выбор уровня", 400, 500,
                             arcade.color.WHITE, font_size=50, anchor_x="center", font_name="Arial")
        elif width == 1920:
            arcade.draw_text("Выбор уровня", width / 2, 900,
                             arcade.color.WHITE, font_size=110, anchor_x="center", font_name="Arial")
        elif width == 2560:
            arcade.draw_text("Выбор уровня", width / 2, 1100,
                             arcade.color.WHITE, font_size=150, anchor_x="center", font_name="Arial")
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)
class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        global volume

        width, height = self.window.get_size()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        if width == 800:
            width_button_scale = 300
            height_button_scale = 50
            size_slider = 24
        else:
            width_button_scale = 500
            height_button_scale = 70
            size_slider = 40
            button_y = 12

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        ui_slider = UISlider(value=volume, width=300, height=50, max_value=20, min_value=0)
        label = UILabel(text=f"Уровень громкости: {ui_slider.value:01.0f}", font_size=size_slider)

        wasd_button = arcade.gui.UIFlatButton(text="WASD", width=width_button_scale)
        self.manager.add(UIAnchorWidget(child=wasd_button, anchor_x="center", align_y=-50))

        arrows_button = arcade.gui.UIFlatButton(text="Стрелочки", width=width_button_scale)
        self.manager.add(UIAnchorWidget(child=arrows_button, anchor_x="center", align_y=-120))

        @ui_slider.event()
        def on_change(event: UIOnChangeEvent):
            global volume
            label.text = f"Уровень громкости: {ui_slider.value:01.0f}"
            label.fit_content()
            volume = round(ui_slider.value)
            print(volume)

        self.manager.add(UIAnchorWidget(child=ui_slider, align_y=70))
        self.manager.add(UIAnchorWidget(child=label, align_y=130))

        wasd_button.on_click = self.on_click_wasd

        arrows_button.on_click = self.on_click_arrows

    def on_click_wasd(self, event):
        global wasd
        wasd = True

    def on_click_arrows(self, event):
        global wasd
        wasd = False

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        width, height = self.window.get_size()
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, width, height, background)
        if width == 800:
            arcade.draw_text("Настройки", 400, 500,
                             arcade.color.WHITE, font_size=50, anchor_x="center", font_name="Arial")
            arcade.draw_text("Выбор управления", 400, 300,
                             arcade.color.WHITE, font_size=24, anchor_x="center", font_name="Arial")
            arcade.draw_text("Если хотите сделать игру в полноэкранный режим, нажмите F", 400, 100,
                             arcade.color.WHITE, font_size=20, anchor_x="center", font_name="Arial")
        elif width == 1920:
            arcade.draw_text("Настройки", width / 2, 900,
                             arcade.color.WHITE, font_size=110, anchor_x="center", font_name="Arial")
            arcade.draw_text("Выбор управления", width / 2, 550,
                             arcade.color.WHITE, font_size=24, anchor_x="center", font_name="Arial")
            arcade.draw_text("Если хотите сделать игру в оконный режим, нажмите F", width / 2, 300,
                             arcade.color.WHITE, font_size=20, anchor_x="center", font_name="Arial")

        elif width == 2560:
            arcade.draw_text("Настройки", width / 2, 1100,
                             arcade.color.WHITE, font_size=150, anchor_x="center", font_name="Arial")
            arcade.draw_text("Выбор управления", width / 2, 720,
                             arcade.color.WHITE, font_size=34, anchor_x="center", font_name="Arial")
            arcade.draw_text("Если хотите сделать игру в оконный режим, нажмите F", width / 2, 500,
                             arcade.color.WHITE, font_size=30, anchor_x="center", font_name="Arial")
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)
        if key == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)
            width, height = self.window.get_size()
            self.window.set_viewport(0, width, 0, height)


class RulesVIew(arcade.View):
    def __init__(self):
        super().__init__()

        width, height = self.window.get_size()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        if width == 800:
            width_button_scale = 300
            button_x = WIDTH - 465
            button_y = HEIGHT - 600
        elif width == 1920:
            width_button_scale = 500
            button_x = width / 2
            button_y = HEIGHT - 600
        elif width == 2560:
            width_button_scale = 500
            button_x = width / 2 + 150
            button_y = HEIGHT - 600

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        back_button = arcade.gui.UIFlatButton(text="Назад", width=width_button_scale, x=button_x, y=button_y)
        self.manager.add(back_button)

        text = "Правила игры:\n\nВам необходимо изменить цвет всех блоков на игровом поле. " \
                 "Когда Q*bert перепрыгивает на блок, его цвет меняется. " \
                 "Однако будьте осторожны, поскольку некоторые блоки могут содержать врагов! " \
                 "Если Q*bert касается врага, он теряет жизнь. " \
                 "Цель состоит в том, чтобы изменить цвет всех блоков, прежде чем жизни Q*bert закончатся.\n\n" \
                 "Управление:\n" \
                 " - Для передвижения Q*bert используйте клавиши W, A, S, D или стрелки.\n"
        text_area = UITextArea(x=width / 4,
                               y=height / 3.6,
                               width=width / 2,
                               height=height / 2.4,
                               text=text,
                               text_color=(0, 0, 0, 255))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        self.manager.add(
            UITexturePane(
                text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(20, 20, 20, 20)
            )
        )

        back_button.on_click = self.on_click_back

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)

    def on_draw(self):
        width, height = self.window.get_size()
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, width, height, background)
        if width == 800:
            arcade.draw_text("Правила", 400, 500,
                             arcade.color.WHITE, font_size=50, anchor_x="center", font_name="Arial")
        elif width == 1920:
            arcade.draw_text("Правила", width / 2, 900,
                             arcade.color.WHITE, font_size=110, anchor_x="center", font_name="Arial")
        elif width == 2560:
            arcade.draw_text("Правила", width / 2, 1100,
                             arcade.color.WHITE, font_size=150, anchor_x="center", font_name="Arial")
        self.manager.draw()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_click_back(self, event):
        menu_view = MenuView()
        self.window.show_view(menu_view)


class QbertGameView(arcade.View):
    cubes = []
    def __init__(self):
        super().__init__()
        self.cubes = []
        self.enemies = []
        self.player = None
        self.score = 0
        self.lives = 3
        self.game_over = False
        width, height = self.window.get_size()
        self.window.set_viewport(0, width, 0, height)
        arcade.set_background_color(arcade.color.AMAZON)
        # self.cubes_enemy = []  # 28
        # x = 400
        # y = 520
        # while x != 160:
        #     while y != 160:
        #         self.cubes_enemy.append([x - 40, y - 60])

    def setup(self):
        i = random.randint(0, 27)
        self.player = Player("D:/Proect college/qbert.png", 1.0)  # Создать куберта
        self.enemies = [Enemy(200,400), Enemy(300,700)]  # Создать врагов
        self.create_cube_grid()
        self.player.set_initial_position(self.cubes[0])

        # Создание врагов
        for i in range(2):
            x = 200 + (i * CUBE_SIZE * 6)
            y = 200
            enemy = Enemy(x, y)
            self.enemies.append(enemy)

    def create_cube_grid(self):
        for y in range(7):
            for x in range(y + 1):
                cube_x = (x - y / 2) * CUBE_WIDTH + WIDTH // 2
                cube_y = (13 - y) * CUBE_HEIGHT + y * -20
                self.cubes.append(Cube(cube_x, cube_y))

    def on_draw(self):
        width, height = self.window.get_size()
        arcade.start_render()
        for cube in self.cubes:
            cube.draw()
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        if width == 800:
            arcade.draw_rectangle_filled(width / 2 - 1250, height / 2 + 650, 900, 220, arcade.color.BLACK + (100,))
            arcade.draw_text(f"Очки: {self.score}", width/2, height/2, arcade.color.WHITE, 20)
            arcade.draw_text(f"Жизни: {self.lives}", width/2, height/2, arcade.color.WHITE, 20)
            if self.game_over:
                arcade.draw_text("Вы проиграли!", WIDTH // 2, HEIGHT // 2, arcade.color.WHITE, 40,
                             anchor_x="center")
        elif width == 1920:
            arcade.draw_rectangle_filled(width / 2 - 1250, height / 2 + 650, 900, 220, arcade.color.BLACK + (100,))
            arcade.draw_text(f"Очки: {self.score}", width/2 - 600, height/2 + 650, arcade.color.WHITE, 14)
            arcade.draw_text(f"Жизни: {self.lives}", width/2 - 550, height/2 + 280, arcade.color.WHITE, 14)
            if self.game_over:
                arcade.draw_text("Вы проиграли!", WIDTH // 2, HEIGHT // 2, arcade.color.WHITE, 40,
                             anchor_x="center")
        elif width == 2560:
            arcade.draw_rectangle_filled(width/2 - 1250, height/2 + 650, 900, 220, arcade.color.BLACK + (100,))
            arcade.draw_text(f"Очки: {self.score}", width/2 - 1250, height/2 + 650, arcade.color.WHITE, 50)
            arcade.draw_text(f"Жизни: {self.lives}", width/2 - 1250, height/2 + 580, arcade.color.WHITE, 50)
            if self.game_over:
                arcade.draw_text("Вы проиграли!", WIDTH // 2, HEIGHT // 2, arcade.color.WHITE, 40,
                             anchor_x="center")

    def update(self, delta_time):

        if self.game_over:
            return

        # Обновление игрока и врагов
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        # Проверка столкновения между игроком и кубами
        on_cube = False
        for cube in self.cubes:
            if arcade.check_for_collision(self.player, cube):
                on_cube = True
                if cube.color != arcade.color.BLUE:
                    self.score += 1
                    cube.change_color()
                    print(f"Координаты куба: ({cube.center_x}, {cube.center_y})")
                break
        # Проверка столкновений между игроком и врагами
        for enemy in self.enemies:
            if arcade.check_for_collision(self.player, enemy):
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    # Сброс позиции игрока
                    initial_cube = self.cubes[0]
                    self.player.set_initial_position(initial_cube)
            if not on_cube:
                self.lives -= 1
                initial_cube = self.cubes[0]
                self.player.set_initial_position(initial_cube)
                break

    def on_key_press(self, key, modifiers):
        global wasd
        global volume
        self.jump = arcade.Sound("sounds/effects/jump.mp3")
        if not wasd:
            if key == arcade.key.LEFT:
                self.player.move_left()
                self.player.move_to_next_cell()
                self.jump.play(volume=volume)
            elif key == arcade.key.RIGHT:
                self.player.move_right()
                self.player.move_to_next_cell()
                self.jump.play(volume=volume)
            elif key == arcade.key.UP:
                self.player.move_up()
                self.player.move_to_next_cell()
                self.jump.play(volume=volume)
            elif key == arcade.key.DOWN:
                self.player.move_down()
                self.player.move_to_next_cell()
                self.jump.play(volume=volume)
            if key == arcade.key.F:
                self.window.set_fullscreen(not self.window.fullscreen)
                width, height = self.window.get_size()
                self.window.set_viewport(0, width, 0, height)
        else:
            if key == arcade.key.A:
                self.player.move_left()
                self.player.move_to_next_cell()
                self.jump.play(volume=volume)
            elif key == arcade.key.D:
                self.player.move_right()
                self.player.move_to_next_cell()
                self.jump.play(volume=volume)
            elif key == arcade.key.W:
                self.player.move_up()
                self.player.move_to_next_cell()
                self.jump.play(volume=volume)
            elif key == arcade.key.S:
                self.player.move_down()
                self.player.move_to_next_cell()
                self.jump.play(volume=volume)
            if key == arcade.key.F:
                self.window.set_fullscreen(not self.window.fullscreen)
                width, height = self.window.get_size()
                self.window.set_viewport(0, width, 0, height)

    def on_close(self):
        # Закрытие окна
        arcade.close_window()

class Player(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.player_position = (0, 0)
        self.change_x = 0
        self.change_y = 0
        self.current_cube = None
        self.move_count = 0
        self.is_jumping = False

    def update(self):
        for cube in QbertGameView.cubes:
            if arcade.check_for_collision(self, cube):
                self.current_cube = cube
                self.move_count += 1  # Increment move count
                if self.move_count >= 2:
                    cube.change_color()  # Change color after two moves
                    self.move_count = 0  # Reset move count
                break
    def move_left(self):
        self.change_x = -40
        self.change_y = 60
        arcade.Sound("sounds/effects/songfon.mp3")

    def move_right(self):
        self.change_x = 40
        self.change_y = -60

    def move_up(self):
        self.change_x = 40
        self.change_y = 60

    def move_down(self):
        self.change_x = -40
        self.change_y = -60

    def move_to_next_cell(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def set_initial_position(self, cube):
        # Установите начальную позицию игрока на указанном кубе
        self.current_cube = cube
        self.center_x = cube.center_x
        self.center_y = cube.center_y
class Enemy(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("D:/Proect college/qbert.png")
        self.center_x = x
        self.center_y = y
        self.change_x = ENEMY_MOVEMENT_SPEED
        self.bounds_left = ENEMY_MOVEMENT_BOUNDS_LEFT
        self.bounds_right = ENEMY_MOVEMENT_BOUNDS_RIGHT

    def update(self):
        self.center_x += self.change_x
        if self.center_x <= self.bounds_left or self.center_x >= self.bounds_right:
            self.change_x *= -1


class Cube(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("D:/Proect college/qbert.png", scale=0.5)
        self.center_x = x
        self.center_y = y
        self.x = x
        self.y = y
        self.color = arcade.color.YELLOW
        self.height = CUBE_HEIGHT

    def draw(self):
        top_left_x = self.center_x - CUBE_WIDTH // 2
        top_left_y = self.center_y - CUBE_HEIGHT // 2

        arcade.draw_polygon_filled(
            [
                (top_left_x, top_left_y),
                (top_left_x + CUBE_WIDTH // 2, top_left_y - CUBE_HEIGHT // 2),
                (top_left_x + CUBE_WIDTH, top_left_y),
                (top_left_x + CUBE_WIDTH // 2, top_left_y + CUBE_HEIGHT // 2)
            ],
            self.color
        )

        arcade.draw_polygon_filled(
            [
                (top_left_x, top_left_y),
                (top_left_x, top_left_y - self.height),
                (top_left_x + CUBE_WIDTH // 2, top_left_y - CUBE_HEIGHT // 2 - self.height),
                (top_left_x + CUBE_WIDTH // 2, top_left_y - CUBE_HEIGHT // 2)
            ],
            arcade.color.DARK_GRAY
        )

        arcade.draw_polygon_filled(
            [
                (top_left_x + CUBE_WIDTH, top_left_y),
                (top_left_x + CUBE_WIDTH // 2, top_left_y - CUBE_HEIGHT // 2),
                (top_left_x + CUBE_WIDTH // 2, top_left_y - CUBE_HEIGHT // 2 - self.height),
                (top_left_x + CUBE_WIDTH, top_left_y - self.height)
            ],
            arcade.color.DARK_GRAY
        )

    def change_color(self):
        if self.color == arcade.color.YELLOW:
            self.color = arcade.color.BLUE

def main():
    window = arcade.Window(WIDTH, HEIGHT, "Q*bert")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

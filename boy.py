from pico2d import *
from state_machine import *


class Idle:
    @staticmethod
    def enter(boy, e):
        print("Boy Idle Enter")

        if start_event(e):
            boy.action = 3
            boy.face_dir = 1

        elif left_up(e):
            boy.action = 2
            boy.face_dir = -1

        elif right_up(e):
            boy.action = 3
            boy.face_dir = 1

        elif time_out(e):
            boy.action = 3
            boy.face_dir = 1

        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        print("Boy Idle Exit")

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class Sleep:
    @staticmethod
    def enter(boy, e):
        if start_event(e):
            boy.action = 3
            boy.face_dir = -1

        elif space_down(e):
            boy.action = 3
            boy.face_dir = -1

        boy.frame = 0
        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

        if get_time() - boy.start_time > 2:
            boy.state_machine.add_event(("TIME_OUT", 0))

    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(
                boy.frame * 100,
                boy.action * 100,
                100,
                100,
                3.141592 / 2,
                "",
                boy.x - 25,
                boy.y - 25,
                100,
                100,
            )

        else:
            boy.image.clip_composite_draw(
                boy.frame * 100,
                boy.action * 100,
                100,
                100,
                -3.141592 / 2,
                "",
                boy.x - 25,
                boy.y - 25,
                100,
                100,
            )


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e):
            boy.dir, boy.action = 1, 1

        elif left_down(e):
            boy.dir, boy.action = -1, 0
        boy.frame = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 3

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class AutoRun:
    @staticmethod
    def enter(boy, e):
        if a_down(e):
            boy.dir, boy.action = 1, 1
            boy.frame = 0
            boy.dx = 0
            boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        print(f"Speed: ", boy.dir)
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 3

        if boy.dir >= 1:
            boy.dir += 0.01

        elif boy.dir <= -1:
            boy.dir -= 0.01

        if boy.x >= 780:
            boy.dir = -boy.dir
            boy.dx = -boy.dx
            boy.action = 0

        elif boy.x <= 20:
            boy.dir = -boy.dir
            boy.dx = -boy.dx
            boy.action = 1

        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(("TIME_OUT", 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image("animation_sheet.png")
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {
                    time_out: Sleep,
                    right_down: Run,
                    left_down: Run,
                    right_up: Idle,
                    left_up: Idle,
                    space_down: Sleep,
                    a_down: AutoRun,
                },
                Sleep: {
                    right_down: Idle,
                    left_down: Idle,
                    right_up: Idle,
                    left_up: Idle,
                    time_out: Idle,
                },
                Run: {
                    right_down: Run,
                    left_down: Run,
                    right_up: Idle,
                    left_up: Idle,
                    space_down: Sleep,
                },
                AutoRun: {
                    time_out: Idle,
                    right_down: Run,
                    left_down: Run,
                },
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        #   event : 입력 이벤트
        #   우리가 state machine 전달해즐 간 튜플( , )
        self.state_machine.add_event(("INPUT", event))

    def draw(self):
        self.state_machine.draw()

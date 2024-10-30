#   이벤트 체크 함수 정의
#   상태 이벤트 e = (종류, 실제 값) 튜플로 정의
from sdl2 import *


def start_event(e):
    return e[0] == "START"


def space_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == "TIME_OUT"


def right_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def a_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []  #   상태 이벤트를 보관할 큐

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.o, ("START", 0))
        print(f"Enter into {self.cur_state}")

    def add_event(self, e):
        print(f"        DEBUG: New event {e} added to event que")
        self.event_que.append(e)

    def handle_event(self, e):
        for event, next_state in self.transitions[self.cur_state].items():
            if event(e):
                print(f"Exit from {self.cur_state}")
                self.cur_state.exit(self.o, e)
                self.cur_state = next_state
                print(f"Enter into {self.cur_state}")
                self.cur_state.enter(self.o, e)
                return

        print(f"        WARN: Event [{e}] at State [{self.cur_state}] not handled")

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.o)

        if self.event_que:  #   큐에 하나라도 있으면 True
            event = self.event_que.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.o)

import argparse
import pathlib
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()
instructions = input_raw.splitlines()


class DisplayCPU:
    reg_X = 1
    cycle = 1
    signal_strength = 0

    framebuffer = np.zeros((40, 6), dtype=bool)

    def print_framebuffer(self):
        w, h = self.framebuffer.shape
        for y in range(h):
            for x in range(w):
                print("▓" if self.framebuffer[x, y] else "░", end="")
            print()

    def record_signal_strength(self):
        if self.cycle == 20 or (self.cycle - 20) % 40 == 0:
            print(f"\t{self.cycle=}, {self.reg_X=}")
            self.signal_strength += self.cycle * self.reg_X

    def draw(self):
        draw_x = self.cycle % 40
        draw_y = self.cycle // 40

        sprite_x = self.reg_X
        will_draw = draw_x >= sprite_x - 1 and draw_x <= sprite_x + 1

        print(f"\t{self.cycle=}, {draw_x=}, {draw_y=}, {sprite_x=}, {will_draw=}")

        self.framebuffer[draw_x, draw_y] = will_draw

    def execute(self, instruction: str):
        if self.cycle >= 240:
            return

        if " " in instruction:
            op, arg = instruction.split()
        else:
            op, arg = instruction, None

        match op:
            case "addx":
                self.draw()
                self.cycle += 1
                self.record_signal_strength()

                self.reg_X += int(arg)
                self.draw()
                self.cycle += 1
                self.record_signal_strength()
            case "noop":
                self.draw()
                self.cycle += 1
                self.record_signal_strength()


cpu = DisplayCPU()
for instruction in instructions:
    cpu.execute(instruction)
print(f"Part 1: {cpu.signal_strength}")
print("Part 2:")
cpu.print_framebuffer()

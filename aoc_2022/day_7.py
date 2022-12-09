import argparse
import pathlib
from collections import deque

parser = argparse.ArgumentParser()
parser.add_argument("input", type=pathlib.Path)
args = parser.parse_args()

input_raw = args.input.read_text()

# Filesystem definitions
class FilesystemNode:
    def __init__(self, name: str, parent):
        self.name = name
        self.parent = parent


class File(FilesystemNode):
    def __init__(self, name: str, _size: int, parent=None):
        super().__init__(name, parent)
        self._size = _size

    def size(self) -> int:
        return self._size


class Directory(FilesystemNode):
    def __init__(self, name: str, parent=None):
        super().__init__(name, parent)
        self.children = []

    def size(self) -> int:
        return sum(child.size() for child in self.children)

    def get_child_by_name(self, name: str) -> FilesystemNode:
        for child in self.children:
            if child.name == name:
                return child

        raise ValueError(f"File with {name} not found")

    def print(self, indent: int = 0):
        print(f"{' ' * indent}{self.name}")
        for child in self.children:
            if isinstance(child, Directory):
                child.print(indent + 2)
            else:
                print(f"{' ' * (indent + 2)}{child.name} ({child.size()} bytes)")


root = Directory(name="/")


# Part 1
cwd = root
commands = input_raw.split("$")

for command in commands:
    command = command.strip()
    if len(command) == 0:
        continue

    lines = command.split("\n")
    if lines[0][:2] == "cd":
        target = lines[0][3:]
        if target == "..":
            cwd = cwd.parent
        elif target == "/":
            cwd = root
        else:
            cwd = cwd.get_child_by_name(target)
        continue

    if lines[0][:3] == "ls":
        listing = lines[1:]

        for item in listing:
            spec, name = item.split(" ", 1)
            if spec == "dir":
                cwd.children.append(Directory(parent=cwd, name=name))
            else:
                size = int(spec)
                cwd.children.append(File(name=name, parent=cwd, _size=size))

root.print()

## Part 1
sizes = []
queue = deque([root])

while queue:
    node = queue.pop()
    if isinstance(node, Directory):
        sizes.append(node.size())
        queue.extend(node.children)

print(sizes)
less_than_100k = [v for v in sizes if v <= 100000]
print(f"Part 1: {sum(less_than_100k)}")


## Part 2
free_space = 70000000 - root.size()
target_space = 30000000
diff = target_space - free_space

smallest_directory = (root, root.size())
queue = deque([root])

while queue:
    node = queue.pop()
    if isinstance(node, Directory):
        size = node.size()
        if size < smallest_directory[1] and size > diff:
            smallest_directory = (node, size)
        queue.extend(node.children)

print(f"Part 2: {smallest_directory[1]}")

import re
from collections import namedtuple

BlockInfo = namedtuple("BlockInfo", ["block_type", "position", "indent_level"])

def is_block_start(line):
    return re.match(r"^\w+\s*:", line)

def should_tag_line(line):
    return re.match(r"^\s*\w*['\"]", line)

def count_indent(line):
    return len(line) - len(line.lstrip())

def remove_previous_wait_tags(line):
    return re.sub(r"{w=\d+(\.\d+)?}", "", line)

def add_wait_tags(line):
    wait_tags = {
        r"[.,]": "{w=[COMMA_WAIT]}",
        r"[:;]": "{w=[COLON_WAIT]}",
        r"[-–—]": "{w=[HYPHEN_WAIT]}",
        r"[!]": "{w=[EXCLAMATION_WAIT]}",
        r"[?]": "{w=[QUESTION_WAIT]}",
        r"[.]": "{w=[PERIOD_WAIT]}",
    }

    for punctuation, wait_tag in wait_tags.items():
        line = re.sub(punctuation, lambda match: f"{match.group()}{wait_tag}", line)

    return line

with open("example_renpy_file.py", "r") as file:
    block_stack = []
    for i, line in enumerate(file.readlines()):
        original_line = line.strip()
        if not original_line:
            continue

        indent_level = count_indent(original_line)
        if is_block_start(original_line):
            block_type = original_line.split()[0]
            block_stack.append(BlockInfo(block_type=block_type, position=i, indent_level=indent_level))
        else:
            while block_stack and indent_level <= block_stack[-1].indent_level:
                block_stack.pop()

            if should_tag_line(original_line):
                # This line should be tagged
                modified_line = remove_previous_wait_tags(original_line)
                modified_line = add_wait_tags(modified_line)
            else:
                # This line should not be tagged
                modified_line = original_line

            # Do something with modified_line (e.g., write it to an output file)

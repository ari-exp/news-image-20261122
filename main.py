"""Copy the pre-rendered newspaper image into the grader's output folder."""

import os
import shutil


def main():
    output_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    os.makedirs(output_dir, exist_ok=True)
    source = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    shutil.copyfile(source, os.path.join(output_dir, "entry.png"))


if __name__ == "__main__":
    main()

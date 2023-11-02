from prepare_toolbox.core import get_input, set_output
from prepare_toolbox.file import get_matching_files

from svg_darkmode.svg import add_style


def main() -> None:
    inputs = get_input("inputs", required=True)
    files = get_matching_files(inputs)
    for file in files:
        add_style(file)
    set_output("files", files)


if __name__ == "__main__":
    main()

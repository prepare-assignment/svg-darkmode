from prepare_toolbox.core import get_input, set_failed, set_output
from prepare_toolbox.file import get_matching_files

from prepare_svg_darkmode.svg import add_style


def main() -> None:
    try:
        inputs = get_input("inputs", required=True)
        files = get_matching_files(inputs)
        for file in files:
            add_style(file)
        set_output("files", files)
    except Exception as e:
        set_failed(e)


if __name__ == "__main__":
    main()

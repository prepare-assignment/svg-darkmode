from prepare_toolbox.core import get_input, set_failed, set_output, warning
from prepare_toolbox.file import get_matching_files

from prepare_svg_darkmode.svg import add_style


def main() -> None:
    try:
        inputs = get_input("inputs", required=True)
        excluded = get_input("excluded")
        include_hidden = get_input("include-hidden")
        files = get_matching_files(inputs, excluded, include_hidden=bool(include_hidden))
        if len(files) == 0:
            # Nothing to convert is usually a mistake in the glob, but not a reason to fail the run
            warning(f"No files matched {inputs}")
        for file in files:
            add_style(file)
        set_output("files", files)
    except Exception as e:
        set_failed(e)


if __name__ == "__main__":
    main()

import os
import tempfile
from pathlib import Path
from typing import Final

import pytest
from _pytest.monkeypatch import MonkeyPatch

from svg_darkmode.svg import add_style

SVG_DIR: Final[str] = os.path.join(Path(__file__).parent.absolute(), "svgs")


@pytest.mark.parametrize(
    "file", [
        "test.svg",
        "test_empty.svg",
        "test_no_media.svg",
        "test_no_svg_selector.svg",
        "test_no_filter.svg"
    ]
)
def test_svg(file: str, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.chdir(SVG_DIR)
    with open(file) as handle:
        contents = handle.read()
    with tempfile.NamedTemporaryFile("w+") as handle:
        handle.write(contents)
        handle.flush()
        add_style(handle.name)
        handle.seek(0)
        result = handle.read()
    with open("result_" + file, mode="r") as handle:
        expected = handle.read()
    assert result == expected


def test_invalid_svg(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.chdir(SVG_DIR)
    with pytest.raises(ValueError) as e:
        add_style("invalid.svg")
    assert "svg tag" in str(e)

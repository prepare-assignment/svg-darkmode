import json
import shutil
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml
from pytest_mock import MockerFixture

from prepare_svg_darkmode.main import main

TASK = Path(__file__).parent.parent / "task.yml"
SVGS = Path(__file__).parent / "svgs"
MEDIA_QUERY = "@media (prefers-color-scheme: dark)"


def set_inputs(monkeypatch: pytest.MonkeyPatch, **inputs: Any) -> None:
    """
    Pass the inputs like prepare-assignment core does: as JSON in PREPARE_<NAME> environment variables,
    including the defaults from task.yml. Use the names from task.yml, with '_' for '-'.
    """
    definition: Dict[str, Any] = yaml.safe_load(TASK.read_text(encoding="utf-8"))["inputs"]
    values = {name: spec["default"] for name, spec in definition.items() if "default" in spec}
    values.update({key.replace("_", "-"): value for key, value in inputs.items()})
    for key, value in values.items():
        if value is not None:
            monkeypatch.setenv(f"PREPARE_{key.upper()}", json.dumps(value))


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """
    project
    |- test.svg
    |- images
    |  |- empty.svg
    |- notes.txt
    """
    shutil.copy(SVGS / "test.svg", tmp_path / "test.svg")
    (tmp_path / "images").mkdir()
    shutil.copy(SVGS / "test_empty.svg", tmp_path / "images" / "empty.svg")
    (tmp_path / "notes.txt").write_text("not an svg\n")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def converted(set_output: Any) -> List[str]:
    """The files output, as is: paths use '/' on every platform (they are used in other steps)"""
    set_output.assert_called_once()
    return list(set_output.call_args.args[1])


def test_convert(project: Path, monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> None:
    set_inputs(monkeypatch, inputs=["**/*.svg"])
    set_output = mocker.patch("prepare_svg_darkmode.main.set_output")
    main()
    assert converted(set_output) == ["images/empty.svg", "test.svg"]
    for file in ["test.svg", "images/empty.svg"]:
        contents = (project / file).read_text()
        assert MEDIA_QUERY in contents
        assert "filter: invert(100%)" in contents


def test_only_matched_files(project: Path, monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> None:
    set_inputs(monkeypatch, inputs=["images/*.svg"])
    set_output = mocker.patch("prepare_svg_darkmode.main.set_output")
    main()
    assert converted(set_output) == ["images/empty.svg"]
    assert MEDIA_QUERY not in (project / "test.svg").read_text()


def test_twice_keeps_one_rule(project: Path, monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> None:
    """Running the task again on a converted file doesn't add the style a second time"""
    set_inputs(monkeypatch, inputs=["test.svg"])
    mocker.patch("prepare_svg_darkmode.main.set_output")
    main()
    once = (project / "test.svg").read_text()
    main()
    assert (project / "test.svg").read_text() == once
    assert once.count(MEDIA_QUERY) == 1


def test_no_matches(project: Path, monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> None:
    set_inputs(monkeypatch, inputs=["**/*.svgz"])
    set_output = mocker.patch("prepare_svg_darkmode.main.set_output")
    main()
    assert converted(set_output) == []


def test_not_an_svg(project: Path, monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> None:
    """The error used to come out of main() as a traceback, so core never got the message"""
    shutil.copy(SVGS / "invalid.svg", project / "invalid.svg")
    set_inputs(monkeypatch, inputs=["invalid.svg"])
    failed = mocker.patch("prepare_svg_darkmode.main.set_failed")
    set_output = mocker.patch("prepare_svg_darkmode.main.set_output")
    main()
    assert "Missing svg tag" in str(failed.call_args.args[0])
    set_output.assert_not_called()


def test_missing_input(project: Path, monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> None:
    """A required input that core didn't pass is reported, not raised"""
    monkeypatch.delenv("PREPARE_INPUTS", raising=False)
    failed = mocker.patch("prepare_svg_darkmode.main.set_failed")
    main()
    failed.assert_called_once()


def test_unreadable_file(project: Path, monkeypatch: pytest.MonkeyPatch, mocker: MockerFixture) -> None:
    """A directory that matches the glob: the OS error is reported like any other failure"""
    (project / "broken.svg").mkdir()
    set_inputs(monkeypatch, inputs=["broken.svg"])
    failed = mocker.patch("prepare_svg_darkmode.main.set_failed")
    main()
    failed.assert_called_once()

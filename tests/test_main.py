from pytest_mock import MockerFixture

from svg_darkmode.main import main


def test_main(mocker: MockerFixture) -> None:

    mocker.patch('svg_darkmode.main.get_input')
    mocker.patch("svg_darkmode.main.get_matching_files", return_value=["a.svg", "b.svg"])
    mocked_add_style = mocker.patch("svg_darkmode.main.add_style")
    mocked_set_output = mocker.patch("svg_darkmode.main.set_output")

    main()

    assert mocked_add_style.call_count == 2
    mocked_set_output.assert_called_once_with("files", ["a.svg", "b.svg"])

import pytest

from tools.file_reader import read_file


def test_read_file(tmp_path):
    file = tmp_path / "notes.txt"
    file.write_text(
        "Hello AI",
        encoding="utf-8"
    )

    result = read_file(str(file))

    assert result == "Hello AI"


def test_read_file_missing():
    with pytest.raises(FileNotFoundError):
        read_file("missing.txt")
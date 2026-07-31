from pathlib import Path

from scripts.check_ste import check_file


def test_long_sentence_is_reported(tmp_path: Path) -> None:
    path = tmp_path / "long.md"
    path.write_text(
        "One two three four five six seven eight nine ten eleven twelve thirteen "
        "fourteen fifteen sixteen seventeen eighteen nineteen twenty twenty-one "
        "twenty-two twenty-three twenty-four twenty-five twenty-six.\n",
        encoding="utf-8",
    )

    assert any("maximum is 25" in problem for problem in check_file(path))


def test_code_block_is_not_checked(tmp_path: Path) -> None:
    path = tmp_path / "code.md"
    path.write_text("```\nshall utilize\n```\n", encoding="utf-8")

    assert check_file(path) == []

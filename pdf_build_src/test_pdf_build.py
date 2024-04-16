from pathlib import Path

from remove_admonitions import remove_admonitions
from process_markdowns import read_table_from_tsv


def test_remove_admonitions(tmp_path):
    input_folder = Path(__file__).parent / "tests" / "data" / "admonitions" / "input"
    expected_folder = Path(__file__).parent / "tests" / "data" / "admonitions" / "expected"

    remove_admonitions(input_folder, tmp_path)

    generated_files = list(tmp_path.glob("**/*.md"))

    for file in generated_files:

        expected = expected_folder / file.relative_to(tmp_path)

        with open(expected, "r", encoding="utf8") as f:
            expected_content = f.readlines()

        with open(file, "r", encoding="utf8") as f:
            generated_content = f.readlines()

        for expected_line, generated_line in zip(expected_content, generated_content):
            assert generated_line == expected_line


def test_read_table_from_tsv(tmp_path):
    data_path = Path(__file__).parent / "tests" / "data" / "read_from_tsv"
    input_file = data_path / "input.md"
    output_file = tmp_path / "output.md"
    expected_file = data_path / "expected.md"

    read_table_from_tsv(input_file, output_file)

    with open(expected_file, "r", encoding="utf8") as f:
        expected_content = f.readlines()

    with open(output_file, "r", encoding="utf8") as f:
        generated_content = f.readlines()

    for expected_line, generated_line in zip(expected_content, generated_content):
        assert generated_line == expected_line

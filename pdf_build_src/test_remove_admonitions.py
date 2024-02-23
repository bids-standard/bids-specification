from pathlib import Path
from remove_admonitions import remove_admonitions


def test_remove_admonitions(tmp_path):
    input_folder = Path(__file__).parent / "tests" / "data" / "input"
    remove_admonitions(input_folder, tmp_path)

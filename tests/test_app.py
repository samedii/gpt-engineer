from pathlib import Path

from gpt_programmer.main import main


def test_app():
    # equivalent to
    # gp tests/test.rs tests/preprompt tests/prompt
    main(
        file_path=Path("tests/test.rs"),
        preprompt_path=Path("tests/preprompt"),
        prompt_path=Path("tests/preprompt"),
    )

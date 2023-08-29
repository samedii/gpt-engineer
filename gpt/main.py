import logging
from pathlib import Path

import typer

from .ai import AI
from .parse_chat import parse_chat

app = typer.Typer()

instruction = """
{prompt}

{file_path}
```rust
{file_content}
```
"""


def preprompt(preprompt_path):
    preprompt = Path(preprompt_path).read_text()
    return preprompt


def prompt(prompt_path, file_path):
    prompt = Path(prompt_path).read_text()
    file_content = Path(file_path).read_text()

    return instruction.format(
        prompt=prompt, file_path=file_path, file_content=file_content
    )


@app.command()
def main(
    file_path: Path = typer.Argument(..., help="path"),
    preprompt_path: Path = typer.Argument("preprompt", help="system prompt"),
    prompt_path: Path = typer.Argument("prompt", help="instruction prompt"),
    model: str = typer.Argument("gpt-3.5-turbo", help="model id string"),
    temperature: float = 0.1,
    verbose: bool = typer.Option(True, "--verbose", "-v"),
):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    ai = AI(
        model_name=model,
        temperature=temperature,
    )

    # steps = [prompt(prompt_path, file_path)]

    messages = ai.start(
        preprompt(preprompt_path),
        prompt(prompt_path, file_path),
        "edit",
    )

    files = parse_chat(messages[-1].content.strip())

    if len(files) == 0:
        raise ValueError("No files found in chat")
    elif len(files) > 1:
        for file in files:
            print(file)
        raise ValueError(f"Multiple files ({len(files)}) found in chat")

    new_file_path, content = files[0]

    if str(new_file_path) != str(file_path):
        raise ValueError(f"File path mismatch: {new_file_path} != {file_path}")

    file_path.write_text(content)


if __name__ == "__main__":
    app()

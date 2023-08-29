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

    if len(files) == 1:
        file_path.write_text(content)
    else:
        found = False
        for output_file_path, content in files:
            if str(output_file_path) == str(file_path):
                file_path.write_text(content)
                found = True

        if not found:
            raise ValueError(f"Could not find {file_path} in output")


if __name__ == "__main__":
    app()

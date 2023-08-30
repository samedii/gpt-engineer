import logging
from pathlib import Path

import typer

from .ai import AI
from .create_directory_tree import create_directory_tree
from .parse_chat import parse_chat

app = typer.Typer()

instruction = """
This is the current implementation:

{directory_tree}

{current_implementation}

{prompt}
```
"""


file = """
{file_path}
```{language}
{file_content}
```
"""


def preprompt(preprompt_path):
    preprompt = Path(preprompt_path).read_text()
    return preprompt


suffix_to_language = dict(
    rs="rust",
    py="python",
    js="javascript",
    ts="typescript",
    md="markdown",
)


def prompt(prompt_path, directory_path):
    prompt = Path(prompt_path).read_text()

    files = []
    for file_path in Path(directory_path).glob("**/*"):
        if file_path.is_file():
            try:
                file_content = file_path.read_text()
                files.append((file_path, file_content))
            except UnicodeDecodeError:
                pass

    current_implementation = "\n\n".join(
        [
            file.format(
                file_path=file_path,
                file_content=file_content,
                language=suffix_to_language.get(file_path.suffix.replace(".", ""), ""),
            )
            for file_path, file_content in files
        ]
    )

    return instruction.format(
        prompt=prompt,
        current_implementation=current_implementation,
        directory_tree=str(create_directory_tree(directory_path)),
    )


@app.command()
def main(
    directory_path: Path = typer.Argument(..., help="directory path"),
    preprompt_path: Path = typer.Argument("preprompt", help="system prompt"),
    prompt_path: Path = typer.Argument("prompt", help="instruction prompt"),
    model: str = typer.Argument("gpt-3.5-turbo", help="model id string"),
    temperature: float = 0.1,
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    ai = AI(
        model_name=model,
        temperature=temperature,
    )

    messages = ai.start(
        preprompt(preprompt_path),
        prompt(prompt_path, directory_path),
        "edit",
    )

    files = parse_chat(messages[-1].content.strip())

    for file_path, file_content in files:
        print(f"file_path: {file_path}")
        print(file_content)

    # if len(files) == 1:
    #     file_path.write_text(content)
    # else:
    #     found = False
    #     for output_file_path, content in files:
    #         if str(output_file_path) == str(file_path):
    #             file_path.write_text(content)
    #             found = True

    #     if not found:
    #         raise ValueError(f"Could not find {file_path} in output")


if __name__ == "__main__":
    app()

import os

import click
from docx import Document

from logic import LogicPuzzle
from puzzle import Puzzle, get_driver


@click.group()
@click.option("-n", default=10, type=int, show_default=True, help="Number of puzzles.")
@click.option(
    "-f",
    "--output-file-name",
    default="puzzles",
    type=str,
    show_default=True,
    help="Name of the output document (w/o file extension).",
)
@click.option(
    "-t",
    "--timeout",
    default=10,
    type=int,
    show_default=True,
    help="The number of seconds to wait for any request to finish",
)
@click.pass_context
def cli(ctx, n: int, output_file_name: str, timeout: int):
    ctx.obj = {"n": n, "output_file_name": output_file_name, "timeout": timeout}


@cli.command()
@click.argument("grid-size", type=int, required=False)
@click.argument("difficulty", type=int, required=False)
@click.option(
    "-o", "--options", is_flag=True, help="Show grid size and difficulty options."
)
@click.pass_obj
def logic(opts, grid_size: int, difficulty: int, options: bool):
    if options:
        driver = get_driver()
        gs, diff = LogicPuzzle("1", "1").get_options(driver, opts["timeout"])
        driver.quit()

        click.echo("Grid Size:")
        for key, value in gs.items():
            click.echo(f"{key}) {value}")
        click.echo("\nDifficulty:")
        for key, value in diff.items():
            click.echo(f"{key}) {value}")
    elif grid_size is None or difficulty is None:
        click.echo("Error: Missing argument 'GRID_SIZE' or 'DIFFICULTY'.")
        sys.exit(1)
    else:
        get_puzzles(
            opts["n"],
            LogicPuzzle(str(grid_size), str(difficulty)),
            opts["output_file_name"],
            opts["timeout"],
        )


def get_puzzles(n: int, puzzle: Puzzle, output_file_name: str, timeout: int):
    driver = get_driver()
    doc = Document()
    for i in range(n):
        print(f"Puzzle {i + 1}/{n}")
        populated_puzzle = puzzle.get_puzzle(driver, timeout)
        populated_puzzle.add_to_doc(doc)
        os.remove(populated_puzzle.img)
    driver.quit()

    doc.save(f"/{os.environ.get('OUTPUT_DIR')}/{output_file_name}.docx")

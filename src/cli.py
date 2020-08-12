import os
import sys

import click
from docx import Document
from docx.shared import Inches

from acrostics import Acrostics
from logic import LogicPuzzle
from puzzle import Puzzle, get_driver
from rws import ReverseWordSearch


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


def puzzle(cli_opts, opts, puzzle, options: bool, f):
    if options:
        driver = get_driver()
        puzzle_options = puzzle.get_options(driver, cli_opts["timeout"])
        driver.quit()

        for idx, (label, puzzle_opts) in enumerate(puzzle_options):
            if idx > 0:
                click.echo("\n")
            click.echo(label + ":")
            for key, value in puzzle_opts.items():
                click.echo(f"{key}) {value}")
    elif any(value is None for name, value in opts):
        arg = [name for name, value in opts if value is None][0]
        click.echo(f"Error: Missing argument '{arg}'.")
        sys.exit(1)
    else:
        f()


@cli.command()
@click.pass_obj
def acrostics(opts):
    """Download Acrostics
    """
    puzzle(
        opts,
        [],
        Acrostics(),
        False,
        lambda: get_puzzles(
            opts["n"], Acrostics(), opts["output_file_name"], opts["timeout"],
        ),
    )


@cli.command()
@click.argument("grid-size", type=int, required=False)
@click.argument("difficulty", type=int, required=False)
@click.option(
    "-o", "--options", is_flag=True, help="Show grid size and difficulty options."
)
@click.pass_obj
def logic(opts, grid_size: int, difficulty: int, options: bool):
    """Download Logic Puzzles
    """
    puzzle(
        opts,
        [("Grid Size", grid_size), ("Difficulty", difficulty)],
        LogicPuzzle("1", "1"),
        options,
        lambda: get_puzzles(
            opts["n"],
            LogicPuzzle(str(grid_size), str(difficulty)),
            opts["output_file_name"],
            opts["timeout"],
        ),
    )


@cli.command()
@click.argument("grid-size", type=int, required=False)
@click.option("-o", "--options", is_flag=True, help="Show grid size options.")
@click.pass_obj
def rws(opts, grid_size: int, options: bool):
    """Download Reverse Word Searches
    """
    puzzle(
        opts,
        [("Grid Size", grid_size)],
        ReverseWordSearch("1"),
        options,
        lambda: get_puzzles(
            opts["n"],
            ReverseWordSearch(str(grid_size)),
            opts["output_file_name"],
            opts["timeout"],
        ),
    )


def get_puzzles(n: int, puzzle: Puzzle, output_file_name: str, timeout: int):
    driver = get_driver()
    doc = Document()

    margin = Inches(0.5)
    sections = doc.sections
    for section in sections:
        section.top_margin = margin
        section.bottom_margin = margin
        section.left_margin = margin
        section.right_margin = margin

    # TODO: Get rid of this ugly hack that fixes grid size bug for ReverseWordSearch
    for i in range(n + 1):
        if i > 0:
            print(f"Puzzle {i}/{n}")
        populated_puzzle = puzzle.get_puzzle(driver, timeout)
        if i > 0:
            populated_puzzle.add_to_doc(doc)
        os.remove(populated_puzzle.img)
    driver.quit()

    doc.save(f"/{os.environ.get('OUTPUT_DIR')}/{output_file_name}.docx")

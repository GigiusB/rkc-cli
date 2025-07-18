import os
from glob import glob
from pathlib import Path

from .main import main
import click


@main.command()
@click.argument("path", type=click.Path(exists=True, dir_okay=True, file_okay=False, writable=True, resolve_path=True, path_type=Path), nargs=1)
@click.argument("prefix", type=str)
@click.option("--recursive/--no-recursive", default=False, show_default=True)
@click.option("--move-root/--no-move-root", default=False, show_default=True)
def prefix(path: Path, prefix: str, recursive: bool, move_root: bool):
    """Prefix all files in a folder."""
    file_iterator = path.rglob("*")
    click.echo(f"Prefixing {path} with prefix: {prefix}")
    for f in file_iterator:
        if f.is_file():
            if recursive or path == f.parent:
                parent = path if move_root else f.parent
                new_name = f'{parent}/{prefix}-{f.name}'
                click.echo(f"Renaming {f} -> {new_name}")
                f.rename(new_name)
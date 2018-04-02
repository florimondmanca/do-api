"""Shell helpers."""

from subprocess import run


def success(args):
    """Execute a command and return whether if exited successfully."""
    cmd = run(args)
    return cmd.returncode == 0

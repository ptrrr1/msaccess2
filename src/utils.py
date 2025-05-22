import click
import os


class Utils:
    @staticmethod
    def parse_columns(column: (str, ...)) -> (str, str):
        if len(column) > 2:
            raise Exception("TMP MSG: Too many columns.")

        if len(column) == 1:
            left_col, right_col = column[0], column[0]
        else:
            left_col, right_col = column

        return left_col, right_col    

    @staticmethod
    def is_valid_file(filename) -> (bool, str):
        is_valid = os.path.isfile(filename)
        ext = None

        if is_valid:
            _, ext = os.path.splitext(filename)

        return (is_valid, ext)

class CustomMultiCommand(click.Group):
    def command(self, *args, **kwargs):
        """
        Receives a list of names and sets all after the first as aliases.
        By Stephen Rauch on StackOverflow
        """
        def decorator(f):
            if isinstance(args[0], list):
                _args = [args[0][0]] + list(args[1:])
                for alias in args[0][1:]:
                    cmd = super(CustomMultiCommand, self).command(
                        alias, *args[1:], **kwargs
                    )(f)
                    cmd.short_help = f"Alias for '{_args[0]}'"
            else:
                _args = args
            cmd = super(CustomMultiCommand, self).command(
                *_args, **kwargs
            )(f)

            return cmd

        return decorator

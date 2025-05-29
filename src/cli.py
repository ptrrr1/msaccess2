from utils import Utils, CustomMultiCommand
from operands import Operands
import click

# TODO: Implement a list of functions and when flag '--neg' is executed remove them
# from the list, then iterate over it to perform actions

class CLI():
    pass_operands = click.make_pass_decorator(Operands, ensure=True)

    
    @click.group(chain=True, cls=CustomMultiCommand,invoke_without_command=False)
    @click.version_option(version="0.1", prog_name="msacces2")
    @click.argument('filename_left',
                    type=click.Path(exists=True, readable=True, file_okay=True, dir_okay=False))
    @click.argument('filename_right',
                    type=click.Path(exists=True, readable=True, file_okay=True, dir_okay=False))
    @click.option('-c', '--column', type=str, multiple=True, required=True,
                  help='Name of column to perform operation. Repeat if files have different column names.')
    @click.option('-o', '--output',
                  type=click.Path(writable=True, file_okay=True, dir_okay=False), required=True,
                  help='Output file. Output is a .xlsx file where each tab corresponds to an operation.')
    @click.option('-n','--negate', is_flag=True, default=False,
                  help='List the operations that should NOT be executed.')
    @click.pass_context
    def cli(
            ctx,
            filename_left: click.Path,
            filename_right: click.Path,
            column: (str, ...),
            output: click.Path,
            negate: bool
        ) -> None:
        left_col, right_col = Utils.parse_columns(column)

        ctx.obj = Operands(
            filename_left,
            filename_right,
            left_col,
            right_col,
            output
        )

        
    @cli.command(['left-not-right', 'lnr'],
                 help='Find the rows which are unique to the left file')
    @pass_operands
    def left_not_right(operands: Operands) -> None:
        return operands.left_not_right


    @cli.command(['right-not-left','rnl'],
                 help='Find the rows which are unique to the right file')
    @pass_operands
    def right_not_left(operands: Operands) -> None:
        return operands.right_not_left


    @cli.command(['intersection','int'],
                 help='Performs a Inner Join.')
    @pass_operands
    def intersection(operands: Operands) -> None:
        return operands.intersection


    @cli.command('union',
                 help='Performs a Union, concatenating Sets vertically.')
    @pass_operands
    def union(operands: Operands) -> None:
        return operands.union


    @cli.command(['cartesian','cart'],
                 help='Do a cartesian product of the Sets.')
    @pass_operands
    def cartesian(operands: Operands) -> None:
        return operands.cartesian


    @cli.command('all',
                 help='Do all operations')
    @pass_operands
    def all(operands: Operands) -> None:
        return [
                operands.left_not_right,
                operands.right_not_left,
                operands.intersection,
                operands.union,
                operands.cartesian
            ]

    @cli.result_callback()
    @pass_operands
    @click.pass_context
    def process_chain(ctx, operands: Operands, *args, **kwargs) -> None:
        operations = args[0]
        if kwargs.get('negate'):
            operations = [op for op in ctx.invoke(CLI.all) if op not in operations]

        for operation in operations:
            operation()
            

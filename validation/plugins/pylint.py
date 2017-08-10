"""
PyLint plugin to fix the type signature of functions wrapped by
`validation.validator`
"""
from astroid import MANAGER
from astroid import scoped_nodes
import astroid
import astroid.helpers


def _looks_like_wrapped_by_validator_decorator(node):
    """
    Returns True if the `astroid.FunctionDef` node passed in looks like it has
    been wrapped by the `validator` decorator, False otherwise.
    """
    if not node.decorators:
        return False

    for decorator in node.decorators.nodes:
        if not isinstance(decorator, astroid.Name):
            continue

        decorator_func = astroid.helpers.safe_infer(decorator)
        if decorator_func in (None, astroid.Uninferable):
            continue

        if not isinstance(decorator_func, astroid.FunctionDef):
            continue

        if decorator_func.qname() == 'validation.base.validator':
            return True
    return False


def _transform_fix_validator_type_signature(node):
    """
    Fixes the type signatures of functions wrapped by the `validator`
    decorator.

    Sets a default value for the first argument, adds a `required` parameter
    and fixes the return type.
    """
    # Add a default for the first argument.
    # Sadly, in python 2, we can't have un-defaulted arguments following
    # defaulted arguments.  We have to flood fill from the beginning to have a
    # default for `value`.
    while len(node.args.args) - len(node.args.defaults):
        node.args.defaults.insert(0, astroid.const_factory(None))

    # Add the `required` argument
    node.args.args.append(
        astroid.AssignName('required', parent=node.args),
    )
    node.args.defaults.append(
        astroid.const_factory(True),
    )

    # Fix the return type.
    def _infer_call_result(caller, context=None):
        if not caller.args:
            # If no value argument is passed the validator returns a closure.
            # TODO return a node that represents a closure.
            yield astroid.Uninferable
        else:
            # If a value argument is passed the validator will not return
            # anything at all.
            pass

    node.infer_call_result = _infer_call_result

    return node


def register(linter):
    """
    Called by pylint to bind the plugin.
    """
    MANAGER.register_transform(
        scoped_nodes.FunctionDef,
        _transform_fix_validator_type_signature,
        _looks_like_wrapped_by_validator_decorator,
    )

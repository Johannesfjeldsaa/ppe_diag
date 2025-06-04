import argparse
from typing import (
    Type, TypeVar, Optional, Union,
    get_origin, get_args
)
from pathlib import Path
from dataclasses import dataclass, fields, field, MISSING


# Type variable for the dataclass itself, used for type hinting in class methods
typevar = TypeVar("typevar", bound="BaseConfig")

@dataclass
class BaseConfig:
    """Base dataclass for dataclasses in the ppe_diag.scripts module.
    Has the basic logging and verbosity settings.
    As well as methods for: help print, CLI parsing, and description of the dataclass.
    """
    verbose:    int = field(default=0, metadata={"help": "Increase verbosity level (0: WARNING, 1: INFO, 2: INFO_DETAILED, 3: DEBUG)"})
    log_file:   Path = field(default=None, metadata={"help": "Path to the log file where logs will be written. If None, logs will not be saved to a file."})
    log_mode:   str = field(default="w", metadata={"help": "Mode for opening the log file ('w' for write, 'a' for append)"})

    def __post_init__(self):

        # check the arguments
        # verbose
        if self.verbose not in [0, 1, 2, 3]:
            raise ValueError(f"Invalid verbosity level: {self.verbose}. Must be 0, 1, 2, or 3.")
        # log_file
        if self.log_file is not None:
            if not self.log_file.exists():
                self.log_file.parent.mkdir(parents=True, exist_ok=True)
                self.log_file.touch()
        # log_mode
        if self.log_mode not in ["w", "a"]:
            raise ValueError(f"Invalid log mode: {self.log_mode}. Must be 'w' or 'a'.")

    @classmethod
    def help(
        cls: Type[typevar]
    ):
        print(f"Dataclass '{cls.__name__}' expects the following fields:")
        for inputfield in fields(cls):
            desc = inputfield.metadata.get("help", "")
            if inputfield.default is not MISSING:
                desc = f"{desc} (default: {inputfield.default!r})"
            else:
                desc = f"{desc} (required)"
            print(f"  {inputfield.name.ljust(25)}: {str(inputfield.type).ljust(25)} {desc}")

    @classmethod
    def from_cli(
        cls: Type[typevar]
    ) -> typevar:
        """Parse command line arguments and return an instance of the dataclass.

        parameters
        ----------
        cls : Type[typevar]
            The dataclass type to instantiate.

        returns
        -------
        BaseConfig
            An instance of the dataclass with values populated from command line arguments.
        """

        parser = argparse.ArgumentParser(description=cls.__doc__)
        for fld in fields(cls):
            arg_name = f"--{fld.name.replace('_', '-')}"
            help_text = fld.metadata.get("help", "")
            required = fld.default is MISSING
            default = None if required else fld.default
            arg_type = fld.type if fld.type != bool else lambda x: bool(int(x))  # convert '0'/'1' for bools

             # Type deduction
            arg_type = fld.type
            origin = get_origin(arg_type)
            args = get_args(arg_type)

            # Handle Optional[X]
            if origin is Union and type(None) in args:
                # Filter out NoneType from Union
                arg_type = next(a for a in args if a is not type(None))
                required = False

            # Determine actual CLI type
            cli_type = arg_type
            if arg_type == bool:
                # Use argparse action instead of type for bools
                parser.add_argument(
                    arg_name,
                    help=help_text + (" (default: False)" if not required else ""),
                    action="store_true" if default is not True else "store_false"
                )
                continue

            # Prepare kwargs
            kwargs = {
                "help": help_text,
                "type": cli_type
            }
            if not required:
                kwargs["default"] = default
            else:
                kwargs["required"] = True

            parser.add_argument(arg_name, **kwargs)

        args = parser.parse_args()
        return cls(**vars(args))

    def describe(
        self,
        return_string: bool = False
    ) -> Optional[str]:
        lines = [f"Instance of dataclass '{self.__class__.__name__}' has the following values:"]
        for inputfield in fields(self):
            desc = inputfield.metadata.get("help", "")
            value = getattr(self, inputfield.name)
            lines.append(f"  {inputfield.name.ljust(25)}: {str(inputfield.type).ljust(25)} = {value!r}  {desc}")
        if return_string:
            return "\n".join(lines)
        else:
            print("\n".join(lines))

    def setup_logging(self):
        pass

    def get_checked_and_derived_config(self):
        pass

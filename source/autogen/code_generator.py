from dataclasses import dataclass
from typing import List, TextIO


@dataclass
class CodeGenerator:
    """Class for autogenerating code."""
    filename: str  # Name of output file.
    output_file: TextIO  # The file reference to output to.
    indentation_level: int = 0  # Number of indents.

    def write_line(self, line: str) -> None:
        self.output_file.writelines(self.indentation_level * "\t" + line + "\n")

    def indent(self) -> None:
        self.indentation_level += 1

    def unindent(self) -> None:
        if self.indentation_level > 0:
            self.indentation_level -= 1

    def write_file(self, lines: List[str]) -> None:
        for line in lines:
            if "}" in line:
                self.unindent()
            self.write_line(line)
            if "{" in line:
                self.indent()

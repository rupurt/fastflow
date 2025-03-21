from uuid import UUID

from uuid_utils.compat import uuid7


class ID:
    id: UUID

    def __init__(self):
        self.id = uuid7()

    def __str__(self) -> str:
        """
        Convert the build `ID` to its string representation.

        Returns:
            str: The string representation of the UUID7 workflow identifier
        """
        return str(self.id)

    def __fspath__(self) -> str:
        """
        Implement the file system path protocol (os.PathLike).

        This allows the ID to be used directly in file system operations
        by converting it to a string path.

        Returns:
            str: The string representation of the ID for use as a path
        """
        return str(self)

import os
import re
import sys
from contextlib import contextmanager
from typing import IO, Any


class TeeOutput:
    """A file-like object that writes to multiple streams simultaneously."""

    def __init__(self, *streams: IO[Any]):
        self.streams = streams

    def write(self, data: str) -> int:
        """Write data to all streams."""
        for i, stream in enumerate(self.streams):
            try:
                # For the first stream (console), write as-is with ANSI codes
                # For subsequent streams (log files), strip ANSI codes
                if i == 0:
                    stream.write(data)
                else:
                    # Strip ANSI escape sequences for log files
                    clean_data = re.sub(r'\x1b\[[0-9;]*[mK]', '', data)
                    stream.write(clean_data)
                stream.flush()  # Ensure immediate write
            except (OSError, AttributeError):
                # Handle cases where stream might be closed or not support flush
                pass
        return len(data)

    def flush(self) -> None:
        """Flush all streams."""
        for stream in self.streams:
            try:
                stream.flush()
            except (OSError, AttributeError):
                pass

    def fileno(self) -> int:
        """Return the file descriptor of the first stream (usually stdout/stderr)."""
        # Return the file descriptor of the first stream if it has one
        if self.streams and hasattr(self.streams[0], 'fileno'):
            try:
                return self.streams[0].fileno()
            except (OSError, AttributeError):
                pass
        # Fallback to stdout fileno
        return sys.stdout.fileno()

    def isatty(self) -> bool:
        """Return True if any of the streams is a TTY."""
        return any(hasattr(stream, 'isatty') and stream.isatty() for stream in self.streams)

    def close(self) -> None:
        """Close all streams except stdout/stderr."""
        for stream in self.streams:
            if stream not in (sys.stdout, sys.stderr) and hasattr(stream, 'close'):
                try:
                    stream.close()
                except (OSError, AttributeError):
                    pass


@contextmanager
def capture_console_output(output_file_path: str):
    """
    Context manager that captures both stdout and stderr to a file
    while still printing to the console (equivalent to `tee`).

    Args:
        output_file_path: Path where console output should be saved

    Usage:
        with capture_console_output("output.log"):
            print("This goes to both console and file")
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Open file for writing with line buffering
    with open(output_file_path, 'w', encoding='utf-8', buffering=1) as log_file:
        # Save original stdout and stderr
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        # Create tee objects that write to both console and file
        tee_stdout = TeeOutput(original_stdout, log_file)
        tee_stderr = TeeOutput(original_stderr, log_file)

        try:
            # Redirect stdout and stderr to the tee objects
            sys.stdout = tee_stdout
            sys.stderr = tee_stderr

            yield

        finally:
            # Ensure final flush before restoring
            try:
                tee_stdout.flush()
                tee_stderr.flush()
            except:
                pass

            # Restore original stdout and stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
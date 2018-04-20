"""
This module contains functions for checking file handles.


Use cases:
  - An input stream
  - An output stream
  - A seekable read-only file
  - A file that can be edited in place

It must be possible to fake all of these with BytesIO or TextIO

Things that will not be checked:
  - Whether the file has an underlying file descriptor
  - Location within the file




Format:
  - Text vs bytes
  - For text files: what encoding is used

Dimensions and offsets:
  - Size
  - Offset relative to the beginning
  - Offset relative to the end


File type:
  - Block device
  - Char device
  - Pipe/named pipe
  - Socket

  - Symlink (ignored)
  - Directory (separate)


Interfaces:
  - Write
  - Read
  - Seek




Proposal:
  - Functions will be split into variants for:
      - Pipes
      - Files
      - Sockets
  - Functions will be split into variants for:
      - Binary
      - Text
  - Read and write will be handled by the same interface


Pipes:
  - Readable
  - Writable
  - Buffered

Files:
  - Readable (default True)
  - Writable (default True)
  - Buffered (not checked)
  - Seekable (default True)
  - Size (default unenforced)
  - Offset (default unenforced)




"""
import io

def validate_text_stream():
    pass


def validate_text_file(
    value,
    allow_read_only=False, allow_write_only=False,
    min_size=None, max_size=None,    
):
    pass


def validate_binary_stream():
    pass


def validate_binary_file():
    pass






def _validate_text_file(
    value,
    allow_read_only=False, allow_write_only=False,
    allow_streaming=False,
):
    if not isinstance(value, io.TextIOBase):
        raise TypeError()
    if value.closed:
        raise ValueError()
    if not allow_streaming and not value.seekable():
        raise ValueError()
    if not allow_read_only and not value.writable():
        raise ValueError()

    if value.tell() != 0:
        raise ValueError
    # TODO validate at end of file without doing io.


class _text_file_validator(object):
    def __init__(self, allow_read_only, allow_streaming):
        _validate_bool(allow_read_only)
        _validate_bool(allow_write_only)

        if (allow_read_only and allow_write_only):
            raise ValueError("files cannot be both read-only and write-only")

        self.__allow_read_only = allow_read_only
        self.__allow_write_only = allow_write_only

        _validate_bool(allow_streaming)
        self.__allow_streaming = allow_streaming

    def __call__(self, value):
        _validate_text_file(
            value,
            allow_read_only=self.__allow_read_only, 
            allow_write_only=self.__allow_write_only,
            allow_streaming=self.__allow_streaming,
        )

    def __repr__(self):
        args = []
        if self.__validator is not None:
            args.append('validator={validator!r}'.format(
                validator=self.__validator,
            ))

        if self.__min_length is not None:
            args.append('min_length={min_length!r}'.format(
                min_length=self.__min_length,
            ))

        if self.__max_length is not None:
            args.append('max_length={max_length!r}'.format(
                max_length=self.__max_length,
            ))

        if not self.__required:
            args.append('required={required!r}'.format(
                required=self.__required,
            ))

        return 'validate_list({args})'.format(args=', '.join(args))


def validate_text_file(value, purpose='w'):
    pass




def validate_binary_file(
    value, allow_read_only=False, allow_streaming=False,
):
    pass


# validate_text_socket(require_write, require_read)

# validate_binary_socket(require_write, require_read)




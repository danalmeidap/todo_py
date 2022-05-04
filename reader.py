def read_input_as_integer(msg) -> int:
    an_integer: int = int(input(msg))
    return an_integer


def read_input_as_string(msg) -> str:
    a_string: str = str(input(msg)).strip().upper()
    return a_string

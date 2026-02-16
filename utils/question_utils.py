from service import AnalysisService


def validate_question(number: str, n: int) -> int:
    try:
        as_float = float(number)
    except ValueError:
        raise TypeError(f"Question number must be a number, got '{number}'.")

    if as_float != int(as_float):
        raise TypeError(f"Question number must be an integer, got float.")

    as_int = int(as_float)

    if not (1 <= as_int <= n):
        raise ValueError(
            f"Question number must be between 1 and {n}, got {as_int}.")

    return as_int


def questions_info():
    return AnalysisService.get_questions_info()


def is_empty_str(s: str):
    return not s or not s.strip()


def a1(number: str, q_size: int):
    errors = []
    if not is_empty_str(number):
        try:
            n = validate_question(number, q_size)
        except (ValueError, TypeError) as e:
            errors.append(str(e))
        if not errors:
            return AnalysisService.run_question(n), number, errors

    return (), number, errors


__all__ = ['a1', "questions_info"]

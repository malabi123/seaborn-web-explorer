from typing import List
from service import DataService as ds
import pandas as pd

OPERATIONS = ['=', '<=', '>=', '!=', '<', '>']
EMPTY = ''


def get_input_columns_validate(col_inp: List[str], allowed_columns: List[str]) -> List[str]:
    if not col_inp:
        return allowed_columns.copy()
    cleaned = []
    for col in col_inp:
        col = col.strip()
        if col not in allowed_columns:
            raise ValueError(f"Invalid column name: {col}")
        cleaned.append(col)
    return cleaned


def is_filters_none(filter_col, op, number):
    return (
        not (filter_col or "").strip() and
        not (op or "").strip() and
        not (number or "").strip()
    )


def get_filter_column_validate(filter_column, filter_columns):
    filter_column = filter_column.strip()
    if filter_column not in filter_columns:
        raise ValueError(f"Invalid filter column: {filter_column}")
    return filter_column


def get_number_from_str(value: str):
    if value is None or value.strip() == EMPTY:
        raise ValueError("Number is required and cannot be empty")
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        raise ValueError(f"Invalid number: {value}")


def validate_operation(op: str):
    if not op or not op.strip():
        raise ValueError("Operation is required")

    op = op.strip()

    if op not in OPERATIONS:
        raise ValueError(
            f"Invalid operation: {op}. Must be one of {OPERATIONS}")

    return op


def apply_filter(df, filter_column, operation, number):
    match operation:
        case "=":
            return df[df[filter_column] == number]
        case "!=":
            return df[df[filter_column] != number]
        case "<":
            return df[df[filter_column] < number]
        case "<=":
            return df[df[filter_column] <= number]
        case ">":
            return df[df[filter_column] > number]
        case ">=":
            return df[df[filter_column] >= number]
        case _:
            raise ValueError(f"Invalid operation: {operation}")


def get_columns():
    df = ds.get_df()
    allowed_columns = df.columns
    filter_columns = df.select_dtypes(include='number').columns
    return allowed_columns, filter_columns


def a1(col_inp: List[str], filter_column, operation, number):
    df = ds.get_df()
    errors = []
    allowed_columns, filter_columns = get_columns()

    try:
        col_inp = get_input_columns_validate(col_inp, allowed_columns)
    except ValueError as e:
        errors.append(str(e))

    if not is_filters_none(filter_column, operation, number):
        try:
            filter_column = get_filter_column_validate(
                filter_column, filter_columns)
        except ValueError as e:
            errors.append(str(e))
        try:
            number = get_number_from_str(number)
        except ValueError as e:
            errors.append(str(e))

        try:
            operation = validate_operation(operation)
        except ValueError as e:
            errors.append(str(e))
        if not errors:
            df = apply_filter(df, filter_column, operation, number)
            df = df[col_inp]
    else:
        filter_column = EMPTY
        operation = EMPTY
        number = EMPTY

    return (df.to_html().replace('_', " "), col_inp, filter_column, operation, number, errors)


__all__ = ['a1', 'OPERATIONS', 'get_columns']

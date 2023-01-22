from decimal import Decimal


SQLITE_MAPPINGS = {
    int: "INT",
    str: "TEXT",
    bytes: "BLOB",
    float: "REAL",
    bool: "INT",
    Decimal: "NUMERIC",
}

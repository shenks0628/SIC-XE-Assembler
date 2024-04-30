OPTAB = {
    "ADD":  [0x18, "3/4"],
    "ADDF": [0x58, "3/4"],
    "ADDR": [0x90, "2"],
    "AND":  [0x40, "3/4"],
    "CLEAR": [0xB4, "2"],
    "COMP": [0x28, "3/4"],
    "COMPF": [0x88, "3/4"],
    "COMPR": [0xA0, "2"],
    "DIV":  [0x24, "3/4"],
    "DIVF": [0x64, "3/4"],
    "DIVR": [0x9C, "2"],
    "FIX": [0xC4, "1"],
    "FLOAT": [0xC0, "1"],
    "HIO": [0xF4, "1"],
    "J": [0x3C, "3/4"],
    "JEQ": [0x30, "3/4"],
    "JGT": [0x34, "3/4"],
    "JLT": [0x38, "3/4"],
    "JSUB": [0x48, "3/4"],
    "LDA": [0x00, "3/4"],
    "LDB": [0x68, "3/4"],
    "LDCH": [0x50, "3/4"],
    "LDF": [0x70, "3/4"],
    "LDL": [0x08, "3/4"],
    "LDS": [0x6C, "3/4"],
    "LDT": [0x74, "3/4"],
    "LDX": [0x04, "3/4"],
    "LPS": [0xD0, "3/4"],
    "MUL": [0x20, "3/4"],
    "MULF": [0x60, "3/4"],
    "MULR": [0x98, "2"],
    "NORM": [0xC8, "1"],
    "OR": [0x44, "3/4"],
    "RD": [0xD8, "3/4"],
    "RMO": [0xAC, "2"],
    "RSUB": [0x4C, "3/4"],
    "SHIFTL": [0xA4, "2"],
    "SHIFTR": [0xA8, "2"],
    "SIO": [0xF0, "1"],
    "SSK": [0xEC, "3/4"],
    "STA": [0x0C, "3/4"],
    "STB": [0x78, "3/4"],
    "STCH": [0x54, "3/4"],
    "STF": [0x80, "3/4"],
    "STI": [0xD4, "3/4"],
    "STL": [0x14, "3/4"],
    "STS": [0x7C, "3/4"],
    "STSW": [0xE8, "3/4"],
    "STT": [0x84, "3/4"],
    "STX": [0x10, "3/4"],
    "SUB": [0x1C, "3/4"],
    "SUBF": [0x5C, "3/4"],
    "SUBR": [0x94, "2"],
    "SVC": [0xB0, "2"],
    "TD": [0xE0, "3/4"],
    "TIO": [0xF8, "1"],
    "TIX": [0x2C, "3/4"],
    "TIXR": [0xB8, "2"],
    "WD": [0xDC, "3/4"]
}

DIRECTIVE = [
    "START",
    "END",
    "WORD",
    "BYTE",
    "RESW",
    "RESB",
    "BASE",
    "CSECT",
    "EXTDEF",
    "EXTREF",
    "LTORG",
    "EQU"
]

registerOP = {
    "A": 0,
    "X": 1,
    "L": 2,
    "B": 3,
    "S": 4,
    "T": 5,
    "F": 6,
    "PC": 8,
    "SW": 9
}

def isInstruction(token):
    if token in OPTAB:
        return True
    else:
        return False

def isDirective(token):
    if token in DIRECTIVE:
        return True
    else:
        return False

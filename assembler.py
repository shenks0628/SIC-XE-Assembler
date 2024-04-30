import sys

import sicxe
import sicxeasmparser

import objfile

MAX_PC = 2047
MIN_PC = -2048
MAX_BASE = 4095
MIN_BASE = 0

instructionForm = 0

def processBYTEC(operand):
    constant = ""
    for i in range(2, len(operand)-1):
        tmp = hex(ord(operand[i]))
        tmp = tmp[2:]
        if len(tmp) == 1:
            tmp = "0" + tmp
        tmp = tmp.upper()
        constant += tmp
    return constant

def generateInstruction(opcode, operand, LOCCTR, base, SYMTAB):
    if instructionForm == 4: # opcode(6) + nixbpe(6) + address(20)
        opcode = opcode[1:]
        instruction = int(sicxe.OPTAB[opcode][0] * 16777216)
        instruction += 1048576 # e = 1
        if operand != None:
            if operand[len(operand)-2:] == ',X':
                instruction += 8388608 # x = 1
                operand = operand[:len(operand)-2]
            if operand[0] == '#':
                instruction += 16777216 # n = 0, i = 1
                operand = operand[1:]
            elif operand[0] == '@':
                instruction += 33554432 # n = 1, i = 0
                operand = operand[1:]
            else:
                instruction += 50331648 # n = 1, i = 1
            if operand in SYMTAB:
                address = int(SYMTAB[operand])
                disp = address
                if address - (LOCCTR + 4) <= MAX_PC and address - (LOCCTR + 4) >= MIN_PC:
                    instruction += 2097152 # b = 0, p = 1
                    disp = address - (LOCCTR + 4)
                    disp = format(disp & 0xFFFFF, 'x')
                    disp = int(disp, 16)
                elif address - base <= MAX_BASE and address - base >= MIN_BASE:
                    instruction += 4194304 # b = 1, p = 0
                    disp = address - base
                else:
                    pass # direct addressing (b = 0, p = 0)
                instruction += disp
            else:
                # direct addressing (b = 0, p = 0)
                address = int(operand)
                disp = address
                instruction += disp
        else:
            instruction += 50331648 # n = 1, i = 1
        return objfile.format4hexstrToWord(hex(instruction))
    if instructionForm == 3: # opcode(6) + nixbpe(6) + address(12)
        instruction = int(sicxe.OPTAB[opcode][0] * 65536)
        if operand != None:
            if operand[len(operand)-2:] == ',X':
                instruction += 32768 # x = 1
                operand = operand[:len(operand)-2]
            if operand[0] == '#':
                instruction += 65536 # n = 0, i = 1
                operand = operand[1:]
            elif operand[0] == '@':
                instruction += 131072 # n = 1, i = 0
                operand = operand[1:]
            else:
                instruction += 196608 # n = 1, i = 1
            if operand in SYMTAB:
                address = int(SYMTAB[operand])
                disp = address
                if address - (LOCCTR + 3) <= MAX_PC and address - (LOCCTR + 3) >= MIN_PC:
                    instruction += 8192 # b = 0, p = 1
                    disp = address - (LOCCTR + 3)
                    disp = format(disp & 0xFFF, 'x')
                    disp = int(disp, 16)
                elif address - base <= MAX_BASE and address - base >= MIN_BASE:
                    instruction += 16384 # b = 1, p = 0
                    disp = address - base
                else:
                    pass # direct addressing (b = 0, p = 0)
                instruction += disp
            else:
                # direct addressing (b = 0, p = 0)
                address = int(operand)
                disp = address
                instruction += disp
        else:
            instruction += 196608 # n = 1, i = 1
        return objfile.format3hexstrToWord(hex(instruction))
    if instructionForm == 2: # opcode(8) + r1(4) + r2(4)
        instruction = int(sicxe.OPTAB[opcode][0] * 256)
        if operand != None:
            operand = operand.split(',')
            if len(operand) == 1 and operand[0] in sicxe.registerOP:
                instruction += int(sicxe.registerOP[operand[0]] * 16)
            elif operand[0] in sicxe.registerOP and operand[1] in sicxe.registerOP:
                instruction += int(sicxe.registerOP[operand[0]] * 16)
                instruction += int(sicxe.registerOP[operand[1]])
            else:
                pass
        return objfile.format2hexstrToWord(hex(instruction))
    if instructionForm == 1: # opcode(8)
        instruction = int(sicxe.OPTAB[opcode][0])
        return objfile.format1hexstrToWord(hex(instruction))


if len(sys.argv) != 2:
    print("Usage: python3 assembler.py <source file>")
    sys.exit()
    
lines = sicxeasmparser.readfile(sys.argv[1])

SYMTAB = {}

# PASS 1
for line in lines:
    t = sicxeasmparser.decompositLine(line)
    if t == (None, None, None):
        continue
    if t[1] == "START":
        STARTING = int(t[2], 16)
        LOCCTR = int(STARTING)
    if t[1] == "END":
        proglen = int(LOCCTR - STARTING)
        break
    if t[0] != None:
        if t[0] in SYMTAB:
            print("Your assembly code has problem.")
            continue
        SYMTAB[t[0]] = LOCCTR
    if t[1][0] == '+':
        LOCCTR = LOCCTR + 4
    elif sicxe.isInstruction(t[1]) == True:
        if sicxe.OPTAB[t[1]][1] == "3/4":
            LOCCTR = LOCCTR + 3
        elif sicxe.OPTAB[t[1]][1] == "2":
            LOCCTR = LOCCTR + 2
        elif sicxe.OPTAB[t[1]][1] == "1":
            LOCCTR = LOCCTR + 1
    elif t[1] == "WORD":
        LOCCTR = LOCCTR + 3
    elif t[1] == "RESW":
        LOCCTR = LOCCTR + (int(t[2])*3)
    elif t[1] == "RESB":
        LOCCTR = LOCCTR + int(t[2])
    elif t[1] == "BYTE":
        if t[2][0] == 'C':
            LOCCTR = LOCCTR + (len(t[2]) - 3)
        if t[2][0] == 'X':
            LOCCTR = LOCCTR + ((len(t[2]) - 3)//2)
        

print(SYMTAB)

# PASS 2

reserveflag = False

t = sicxeasmparser.decompositLine(lines[0])
    
file = objfile.openFile(sys.argv[1])

LOCCTR = 0
if t[1] == "START":
    LOCCTR = int(t[2], 16)
    progname = t[0]
STARTING = LOCCTR

objfile.writeHeader(file, progname, STARTING, proglen)

tline = ""
tstart = LOCCTR
base = None

MRecord = []

for line in lines:
    t = sicxeasmparser.decompositLine(line)
    if t == (None, None, None):
        continue
    if t[1] == "START":
        continue
    if t[1] == "END":
        if len(tline) > 0:
            objfile.writeText(file, tstart, tline)
        PROGLEN = LOCCTR - STARTING
        address = STARTING
        if t[2] != None:
            address = SYMTAB[t[2]]
        for m in MRecord:
            objfile.writeMod(file, m[0], m[1])
        objfile.writeEnd(file, address)
        break
    if t[1][0] == '+':
        instructionForm = 4
        instruction = generateInstruction(t[1], t[2], LOCCTR, base, SYMTAB)
        if len(instruction) == 0:
            print("Undefined Symbole: %s" % t[2])
            break
        if (LOCCTR + 4 - tstart > 30) or (reserveflag == True):
            if reserveflag == True:
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR
                tline = instruction
            elif (LOCCTR + 3 - tstart <= 30):
                tline += instruction[:6]
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR + 3
                tline = instruction[6:]
            elif (LOCCTR + 2 - tstart <= 30):
                tline += instruction[:4]
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR + 2
                tline = instruction[4:]
            elif (LOCCTR + 1 - tstart <= 30):
                tline += instruction[:2]
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR + 1
                tline = instruction[2:]
            else:
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR
                tline = instruction
        else:
            tline += instruction
        reserveflag = False
        if t[2][0] == "#":
            for i in t[2][1:]:
                if i < '0' or i > '9':
                    MRecord.append((LOCCTR + 1, 20))
                    break
        else:
            MRecord.append((LOCCTR + 1, 20))
        LOCCTR += 4
    elif t[1] in sicxe.OPTAB:
        if sicxe.OPTAB[t[1]][1] == "3/4":
            instructionForm = 3
            instruction = generateInstruction(t[1], t[2], LOCCTR, base, SYMTAB)
            if len(instruction) == 0:
                print("Undefined Symbole: %s" % t[2])
                break
            if (LOCCTR + 3 - tstart > 30) or (reserveflag == True):
                if reserveflag == True:
                    objfile.writeText(file, tstart, tline)
                    tstart = LOCCTR
                    tline = instruction
                elif (LOCCTR + 2 - tstart <= 30):
                    tline += instruction[:4]
                    objfile.writeText(file, tstart, tline)
                    tstart = LOCCTR + 2
                    tline = instruction[4:]
                elif (LOCCTR + 1 - tstart <= 30):
                    tline += instruction[:2]
                    objfile.writeText(file, tstart, tline)
                    tstart = LOCCTR + 1
                    tline = instruction[2:]
                else:
                    objfile.writeText(file, tstart, tline)
                    tstart = LOCCTR
                    tline = instruction
            else:
                tline += instruction
            reserveflag = False
            LOCCTR += 3
        elif sicxe.OPTAB[t[1]][1] == "2":
            instructionForm = 2
            instruction = generateInstruction(t[1], t[2], LOCCTR, base, SYMTAB)
            if len(instruction) == 0:
                print("Undefined Symbole: %s" % t[2])
                break
            if (LOCCTR + 2 - tstart > 30) or (reserveflag == True):
                if reserveflag == True:
                    objfile.writeText(file, tstart, tline)
                    tstart = LOCCTR
                    tline = instruction
                elif (LOCCTR + 1 - tstart <= 30):
                    tline += instruction[:2]
                    objfile.writeText(file, tstart, tline)
                    tstart = LOCCTR + 1
                    tline = instruction[2:]
                else:
                    objfile.writeText(file, tstart, tline)
                    tstart = LOCCTR
                    tline = instruction
            else:
                tline += instruction
            reserveflag = False
            LOCCTR += 2
        elif sicxe.OPTAB[t[1]][1] == "1":
            instructionForm = 1
            instruction = generateInstruction(t[1], t[2], LOCCTR, base, SYMTAB)
            if len(instruction) == 0:
                print("Undefined Symbole: %s" % t[2])
                break
            if (LOCCTR + 1 - tstart > 30) or (reserveflag == True):
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR
                tline = instruction
            else:
                tline += instruction
            reserveflag = False
            LOCCTR += 1
    elif t[1] == "WORD":
        constant = objfile.hexstrToWord(hex(int(t[2])))
        if (LOCCTR + 3 - tstart > 30) or (reserveflag == True):
            if reserveflag == True:
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR
                tline = constant
            elif (LOCCTR + 2 - tstart <= 30):
                tline += constant[:4]
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR + 2
                tline = constant[4:]
            elif (LOCCTR + 1 - tstart <= 30):
                tline += constant[:2]
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR + 1
                tline = constant[2:]
            else:
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR
                tline = constant
        else:
            tline += constant
        reserveflag = False
        LOCCTR += 3
    elif t[1] == "BYTE":
        if t[2][0] == 'X':
            operandlen = int((len(t[2]) - 3)/2)
            constant = t[2][2:len(t[2])-1]
        elif t[2][0] == 'C':
            operandlen = int(len(t[2]) - 3)
            constant = processBYTEC(t[2])
        if (LOCCTR + 3 - tstart > 30) or (reserveflag == True):
            if reserveflag == True:
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR
                tline = constant
            elif (LOCCTR + 2 - tstart <= 30):
                tline += constant[:4]
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR + 2
                tline = constant[4:]
            elif (LOCCTR + 1 - tstart <= 30):
                tline += constant[:2]
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR + 1
                tline = constant[2:]
            else:
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR
                tline = constant
        else:
            tline += constant
        reserveflag = False
        LOCCTR += operandlen
    elif t[1] == "RESB":
        LOCCTR += int(t[2])
        reserveflag = True
    elif t[1] == "RESW":
        LOCCTR += (int(t[2]) * 3)
        reserveflag = True
    elif t[1] == "BASE":
        if t[2] in SYMTAB:
            base = SYMTAB[t[2]]
        else:
            print("Undefined Symbole: %s" % t[2])
            break
    else:
        print("Invalid Instruction / Invalid Directive")

    
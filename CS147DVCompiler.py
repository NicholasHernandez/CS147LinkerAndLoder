#!/usr/bin/python3

import re
import sys

print("@0001000")
#stores the type and the opcode (or funct for R type)
linkerDict = {}
opcode_width = 6
reg_width = 5
shmat_width = 5
funct_width = 6
imm_width = 16
addr_width = 26
#NameError

def link(filepath):
    global linkerDict
    with open(filepath, 'r') as f:
        lineNum = 4096 #decimal equiv of 1000
        for text in f.readlines():
            tokens = text.split()
            if len(tokens)==0:
                continue #whitespace

            if tokens[0] not in mnemonics:
                linkerDict[tokens[0][:-1]] = lineNum # appends everything to the list except the colon
            if len(tokens)>1:
                lineNum += 1
def translate(filepath, dest):
    lineNum = 4096
    with open(filepath, 'r') as f:
        with open(dest, 'w') as w:
            w.write("@0001000\n")
            for text in f.readlines():
                tokens = text.split()
                if len(tokens)==0:
                    continue
                tokens = text.split()
                if tokens[0] in mnemonics:
                    decimalRep = mnemonics[tokens[0]][0]( mnemonics[tokens[0]][1], tokens[1:], lineNum)
                    lineNum+=1
                elif len(tokens)>1 and tokens[1] in mnemonics:
                    decimalRep = mnemonics[tokens[1]][0](mnemonics[tokens[1]][1], tokens[2:], lineNum)
                    lineNum+=1
                else:
                    continue
                hexRep = str(hex(decimalRep))[2:]
                machineCode = (("0")*(8-len(hexRep)))+hexRep ##zero extends
                w.write(machineCode+ "//"+text.rstrip()+"\n")
                print(machineCode+ "//"+text.rstrip())

def R_type(funct, tokenList, lineNum):
    instr = 0 #opcode
    rd = parseRegister(tokenList[0])
    rs = parseRegister(tokenList[1])
    rt = parseRegister(removeSemicolon(tokenList[2]))
    instr = instr << reg_width
    instr+= rs
    instr = instr << reg_width
    instr+= rt
    instr = instr << reg_width
    instr+= rd
    instr = instr << shmat_width
    #no shmat
    instr = instr << funct_width
    instr += funct
    return instr

def R_type_shift(funct, tokenList, lineNum): #r_type shift
    instr = 0  # opcode
    instr = instr << opcode_width  # pointless but whatever
    rd = parseRegister(tokenList[0])
    rs = parseRegister(tokenList[1])
    shmat = parseShmat(removeSemicolon(tokenList[2]))
    instr = instr << reg_width
    instr += rs
    instr = instr << reg_width
    #no rt for shift
    instr = instr << reg_width
    instr += rd
    instr = instr << shmat_width
    instr += shmat
    instr = instr << funct_width
    instr += funct
    return instr
def removeSemicolon(token):
    return token[:-1]

def parseRegister(token):
    register_num  = int(re.search("r((\[(\d*)\])|\d*)", token).group(1))
    if register_num < 32 and register_num >=0:
        return register_num
    else:
        raise OverflowError("registers must be in between 0 and 31")
def parseShmat(token):
    shmat  = int(token)
    if shmat < 32 and shmat >= 0:
        return shmat
    else:
        raise OverflowError("registers must be in between 0 and 31")

def parseImm (token):
    if '0x' == token[0:2]: #its hex
        imm = int(token[2:], 16)
    else:
        imm = int(token)
    if imm <65536 and imm >= -32767: #has to be between these based on if its signed
        return imm
    else:
        raise OverflowError("immidate value must be must be in between 65536 and -32767")



def I_type(opcode, tokenList, lineNum):
    instr = opcode  # opcode
    rt = parseRegister(tokenList[0])
    rs = parseRegister(tokenList[1])
    imm = parseImm(removeSemicolon(tokenList[2]))
    instr = instr << reg_width
    instr += rs
    instr = instr << reg_width
    instr += rt
    if imm<0 :
        instr+=1
    instr = instr << imm_width
    instr+=imm
    return instr

def I_type_lui(opcode, tokenList, lineNum):
    instr = opcode  # opcode
    rt = parseRegister(tokenList[0])
    rs = 0
    imm = parseImm(removeSemicolon(tokenList[1]))
    instr = instr << reg_width
    instr += rs
    instr = instr << reg_width
    instr += rt
    if imm<0 :
        instr+=1
    instr = instr << imm_width
    instr+=imm
    return instr

def I_type_branch(opcode, tokenList, lineNum):
    instr = opcode  # opcode
    rt = parseRegister(tokenList[0])
    rs = parseRegister(tokenList[1])
    imm = parseBranchAddress(removeSemicolon(tokenList[2]), lineNum)
    instr = instr << reg_width
    instr += rs
    instr = instr << reg_width
    instr += rt
    if imm<0 :
        instr+=1#fixes issue with 2s compliment multiplication of a 32 bit number that should only take up 16 spaces
    instr = instr << imm_width
    instr+= imm
    return instr
def parseBranchAddress(token, lineNum):
    if token in linkerDict:
        addr = linkerDict[token]
    else:
        raise NameError("{} is not a mnumonic and was not found during linking step!".format(token))
    branchAddr = addr -lineNum -1
    if branchAddr<32767 and branchAddr >= -32767:
        return branchAddr
    else:
        raise EnvironmentError("Branch is too far away, try a jump register or something")

def parseJumpAddress(token):
    if token in linkerDict:
        addr = linkerDict[token]
        return addr
    else:
        raise NameError("{} is not a mnumonic and was not found during linking step!".format(token))

def J_type(opcode, tokenList, lineNum):
    instr = opcode  # opcode
    instr= instr << addr_width
    addr = parseJumpAddress(removeSemicolon(tokenList[0]))
    instr += addr
    return instr

def J_type_stack(opcode, tokenList, lineNum):
    instr = opcode  # opcode
    instr= instr << addr_width
    return instr

mnemonics = {'add': (R_type, 32), 'sub': (R_type, 34), 'mul':(R_type, 44), 'and': (R_type, 36), 'or': (R_type,37),
            'nor': (R_type, 39), 'slt': (R_type, 42), 'sll': (R_type_shift, 1), 'srl': (R_type_shift, 2), 'nor': (R_type, 2),
            'jr': (R_type, 8),'addi': (I_type, 8), 'muli': (I_type, 29), 'andi': (I_type, 12), 'ori': (I_type, 13),
            'lui': (I_type_lui, 15),'slti': (I_type, 10), 'beq': (I_type_branch, 4), 'bne': (I_type_branch, 5), 'lw': (I_type, 35),
            'sw': (I_type, 43), 'jmp': (J_type, 2), 'jal': (J_type, 3), 'push': (J_type_stack, 27), 'pop': (J_type_stack, 28)}

def Compile():
    filepath =  sys.argv[1]
    destination= sys.argv[2]
    link(filepath)
    translate(filepath, destination)

Compile()

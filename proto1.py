#read file
#read lines
#analyze all lines
#create file

dataConstants = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

compValues = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110011",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "A+D": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "A&D": "0000000",
    "D|A": "0010101",
    "A|D": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "M+D": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "M&D": "1000000",
    "D|M": "1010101",
    "M|D": "1010101"
}

destValues = {
    "NULL": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

jumpValues = {
    "NULL": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

variableStartLocation = 16
instructionStartLocation = 0

class Assembler:
    def __init__(self, name):
        try:
            self.file = open(name + '.asm', 'r').readlines()
        except:
            self.file = []
        self.variableLocation = variableStartLocation
        self.instructionLocation = instructionStartLocation
        self.symbols = {}
        self.bitCommands = []
        self.fileName = name

    def lineCleaner(self, line):
        splitted = line.split('//')
        return splitted[0].strip()

    def cleanCommands(self):
        data = [ self.lineCleaner(x) for x in self.file if not self.lineCleaner(x) == '' ]
        return data

    def labelDefiner(self):
        for val in self.cleanCommands():
            if val[0] == "(":
                self.symbols[val[1:-1]] = self.instructionLocation
            else:
                self.instructionLocation = self.instructionLocation + 1
        self.instructionLocation = 0

    def intToBitcodeConvertor(self, val):
        try:
            v = bin(val)[2:]
            return '0' * (16 - len(v)) + v
        except:
            return '0000000000000000'

    def fileCreator(self):
        self.file = open(self.fileName + '.me.hack', 'w')
        self.file.writelines(self.bitCommands)

    def preRun(self):
        self.labelDefiner()
        commands = self.cleanCommands()
        ln = len(commands)
        i = 0
        while(i < ln):
            if commands[i][0] == '@':
                val = commands[i][1:]
                intValue = 0
                try:
                    intValue = int(val)
                except:
                    try:
                        intValue = dataConstants[val]
                    except:
                        try:
                            intValue = self.symbols[val]
                        except:
                            self.symbols[val] = intValue = self.variableLocation
                            self.variableLocation = self.variableLocation + 1
                self.bitCommands.append(self.intToBitcodeConvertor(intValue) + '\n')
            elif commands[i][0] == '(':
                i=i+1
                continue
            else:
                jump = comp = dest = ''
                val = commands[i]
                v1 = val.split('=')
                if len(v1) == 1:
                    dest = 'NULL'
                    v2 = v1[0].split(';')
                    if len(v2) > 2:
                        raise Exception('invalid syntax, more than 1 ; found')
                    comp = v2[0]
                    jump = v2[1]
                elif len(v1) > 2:
                    raise Exception('invalid syntax in line, more than one = found')
                else:
                    jump = 'NULL'
                    if len(v1[0].split(';')) > 1:
                        raise Exception('invalid syntax, ; appeared before =')
                    dest = v1[0]
                    v2 = v1[1].split(';')
                    if len(v2) > 2:
                        raise Exception('invalid syntax, more than 1 ; found')
                    comp = v2[0]

                if dest == '' or comp == '' or jump == '':
                    raise Exception('invalid syntax')
                self.bitCommands.append('111' + compValues[comp] + destValues[dest] + jumpValues[jump] + '\n')
            i = i+1

        print(self.bitCommands)
        self.fileCreator()

a = Assembler('pong/Pong')
a.preRun()
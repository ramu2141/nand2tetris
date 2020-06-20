class CodeWriter:
    
    def __init__(self, asmfile):
        self.asmf = open(asmfile, 'w')
        self.vmfile = ''
        self.symbol_counter = 0

    def set_file_name(self, filename):
        self.vmfile = filename

    def write_arithmetic(self, command):
        vm_asm = {
            'add': '@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n',
            'sub': '@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n',
            'neg': '@SP\nA=M-1\nM=-M\n',
            'and': '@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n',
            'or' : '@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n',
            'not': '@SP\nA=M-1\nM=!M\n',
        }

        vm_asm_comp = {'eq':'JEQ', 'gt':'JGT', 'lt':'JLT'}

        if command in vm_asm:
            self.asmf.write(vm_asm[command])
        elif command in ('eq', 'gt', 'lt'):
            self.asmf.write('@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n')
            self.asmf.write('@TRUE' + str(self.symbol_counter) + '\n')
            self.asmf.write('D;' + vm_asm_comp[command] + '\n')
            self.asmf.write('@SP\nA=M-1\nM=0\n')
            self.asmf.write('@END' + str(self.symbol_counter) + '\n')
            self.asmf.write('0;JMP\n')
            self.asmf.write('(TRUE' + str(self.symbol_counter) + ')\n')
            self.asmf.write('@SP\nA=M-1\nM=-1\n')
            self.asmf.write('(END' + str(self.symbol_counter) + ')\n')
            self.symbol_counter+=1
        else:
            pass

    def write_push_pop(self, command, segment, index):
        if command == 'C_PUSH':
            self.asmf.write(self._write_push(segment, index))
        elif command == 'C_POP':
            self.asmf.write(self._write_pop(segment, index))
        else:
            pass

    def _write_push(self, segment, index):
        cmds = ''

        if segment == 'argument':
            cmds += '@ARG\nD=M\n'
            cmds += '@' + str(index) + '\n'
            cmds += 'A=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            
        elif segment == 'local':
            cmds += '@LCL\nD=M\n'
            cmds += '@' + str(index) + '\n'
            cmds += 'A=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        
        elif segment == 'static':
            cmds += '@' + self.vmfile + '.' + str(index) + '\n'
            cmds += 'D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            
        elif segment == 'constant':
            cmds += '@' + str(index) + '\n'
            cmds += 'D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        elif segment == 'this':
            cmds += '@THIS\nD=M\n'
            cmds += '@' + str(index) + '\n'
            cmds += 'A=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        elif segment == 'that':
            cmds += '@THAT\nD=M\n'
            cmds += '@' + str(index) + '\n'
            cmds += 'A=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        elif segment == 'pointer':
            cmds += '@' + str(3+index) + '\n'
            cmds += 'D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        elif segment == 'temp':
            cmds += '@' + str(5+index) + '\n'
            cmds += 'D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        else:
            pass

        return cmds

    def _write_pop(self, segment, index):
        cmds = ''

        if segment == 'argument':
            cmds += '@' + str(index) + '\n'
            cmds += 'D=A\n@ARG\nM=M+D\n@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n'
            cmds += '@' + str(index) + '\n'
            cmds += 'D=A\n@ARG\nM=M-D\n'

        elif segment == 'local':
            cmds += '@' + str(index) + '\n'
            cmds += 'D=A\n@LCL\nM=M+D\n@SP\nAM=M-1\nD=M\n@LCL\nA=M\nM=D\n'
            cmds += '@' + str(index) + '\n'
            cmds += 'D=A\n@LCL\nM=M-D\n'

        elif segment == 'static':
            cmds += '@SP\nAM=M-1\nD=M\n'
            cmds += '@' + self.vmfile + '.' + str(index) + '\n'
            cmds += 'M=D\n'

        elif segment == 'this':
            cmds += '@' + str(index) + '\n'
            cmds += 'D=A\n@THIS\nM=M+D\n@SP\nAM=M-1\nD=M\n@THIS\nA=M\nM=D\n'
            cmds += '@' + str(index) + '\n'
            cmds += 'D=A\n@THIS\nM=M-D\n'

        elif segment == 'that':
            cmds += '@' + str(index) + '\n'
            cmds += 'D=A\n@THAT\nM=M+D\n@SP\nAM=M-1\nD=M\n@THAT\nA=M\nM=D\n'
            cmds += '@' + str(index) + '\n'
            cmds += 'D=A\n@THAT\nM=M-D\n'

        elif segment == 'pointer':
            cmds += '@SP\nAM=M-1\nD=M\n'
            cmds += '@' + str(3+index) + '\n'
            cmds += 'M=D\n'

        elif segment == 'temp':
            cmds += '@SP\nAM=M-1\nD=M\n'
            cmds += '@' + str(5+index) + '\n'
            cmds += 'M=D\n'

        else:
            pass
        
        return cmds

    def close(self):
        self.asmf.close()
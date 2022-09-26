from cProfile import label


class CodeWriter:
    def __init__(self, asmfile):
        self.asmf = open(asmfile, 'w')
        self.label_counter = 0

    def close(self):
        self.asmf.close()

    def set_file_name(self, filename):
        self.file_name = filename[:-3]


    def write_arithmetic(self, command):
        arith_cmd_table = {
            'add':'// add\n@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n',
            'sub':'// sub\n@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n',
            'neg':'// neg\n@SP\nA=M-1\nM=-M\n',
            'eq':f'// eq\n@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@TRUE{self.label_counter}\n'
                +f'D;JEQ\n@SP\nA=M-1\nM=0\n@END{self.label_counter}\n0;JMP\n'
                +f'(TRUE{self.label_counter})\n@SP\nA=M-1\nD=0\nM=!D\n(END{self.label_counter})\n',
            'gt':f'// gt\n@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@TRUE{self.label_counter}\n'
                +f'D;JGT\n@SP\nA=M-1\nM=0\n@END{self.label_counter}\n0;JMP\n'
                +f'(TRUE{self.label_counter})\n@SP\nA=M-1\nD=0\nM=!D\n(END{self.label_counter})\n',
            'lt':f'// lt\n@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@TRUE{self.label_counter}\n'
                +f'D;JLT\n@SP\nA=M-1\nM=0\n@END{self.label_counter}\n0;JMP\n'
                +f'(TRUE{self.label_counter})\n@SP\nA=M-1\nD=0\nM=!D\n(END{self.label_counter})\n',
            'and':'// and\n@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n',
            'or':'// or\n@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n',
            'not':'// not\n@SP\nA=M-1\nM=!M\n',
        }
        self.asmf.write(arith_cmd_table[command])
        self.label_counter += 1
    
    def write_push_pop(self, command, segment, index):
        if command == 'C_PUSH':
            self.__write_push(segment, index)
        elif command == 'C_POP':
            self.__write_pop(segment, index)
        else:
            pass

    def __write_push(self, segment, index):
        if segment == 'pointer':
            this_or_that = ['THIS', 'THAT'][index]
        else:
            this_or_that = ''
        
        push_cmd_table = {
            'argument': f'// push argument {index}\n@ARG\nD=M\n@{index}\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'local':    f'// push local {index}\n@LCL\nD=M\n@{index}\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'static':   f'// push static {index}\n@{self.file_name}.{index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'constant': f'// push constant {index}\n@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'this':     f'// push this {index}\n@THIS\nD=M\n@{index}\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'that':     f'// push that {index}\n@THAT\nD=M\n@{index}\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'pointer':  f'// push pointer {index}\n@{this_or_that}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'temp':     f'// push temp {index}\n@R{index+5}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
        }
        self.asmf.write(push_cmd_table[segment])

    def __write_pop(self, segment, index):
        if segment == 'pointer':
            this_or_that = ['THIS', 'THAT'][index]
        else:
            this_or_that = ''

        push_cmd_table = {
            'argument': f'// pop argument {index}\n@ARG\nD=M\n@{index}\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n',
            'local':    f'// pop local {index}\n@LCL\nD=M\n@{index}\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n',
            'static':   f'// pop static {index}\n@SP\nAM=M-1\nD=M\n@{self.file_name}.{index}\nM=D\n',
            'this':     f'// pop this {index}\n@THIS\nD=M\n@{index}\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n',
            'that':     f'// pop that {index}\n@THAT\nD=M\n@{index}\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n',
            'pointer':  f'// pop pointer {index}\n@SP\nAM=M-1\nD=M\n@{this_or_that}\nM=D\n',
            'temp':     f'// pop temp {index}\n@SP\nAM=M-1\nD=M\n@R{index+5}\nM=D\n',
        }
        self.asmf.write(push_cmd_table[segment])
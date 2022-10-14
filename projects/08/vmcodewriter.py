class CodeWriter:
    label_counter = 0

    def __init__(self, asmfile):
        self.asmf = open(asmfile, 'w')

    def close(self):
        self.asmf.close()

    def set_file_name(self, filename):
        self.file_name = filename[:-3]

    def write_arithmetic(self, command):
        arith_cmd_table = {
            'add':'// add\n@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n',
            'sub':'// sub\n@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n',
            'neg':'// neg\n@SP\nA=M-1\nM=-M\n',
            'eq':f'// eq\n@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@TRUE{CodeWriter.label_counter}\n'
                +f'D;JEQ\n@SP\nA=M-1\nM=0\n@END{CodeWriter.label_counter}\n0;JMP\n'
                +f'(TRUE{CodeWriter.label_counter})\n@SP\nA=M-1\nD=0\nM=!D\n'
                +f'(END{CodeWriter.label_counter})\n',
            'gt':f'// gt\n@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@TRUE{CodeWriter.label_counter}\n'
                +f'D;JGT\n@SP\nA=M-1\nM=0\n@END{CodeWriter.label_counter}\n0;JMP\n'
                +f'(TRUE{CodeWriter.label_counter})\n@SP\nA=M-1\nD=0\nM=!D\n'
                +f'(END{CodeWriter.label_counter})\n',
            'lt':f'// lt\n@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@TRUE{CodeWriter.label_counter}\n'
                +f'D;JLT\n@SP\nA=M-1\nM=0\n@END{CodeWriter.label_counter}\n0;JMP\n'
                +f'(TRUE{CodeWriter.label_counter})\n@SP\nA=M-1\nD=0\nM=!D\n'
                +f'(END{CodeWriter.label_counter})\n',
            'and':'// and\n@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n',
            'or':'// or\n@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n',
            'not':'// not\n@SP\nA=M-1\nM=!M\n',
        }
        self.asmf.write(arith_cmd_table[command])
        CodeWriter.label_counter += 1
    
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
            'argument': f'// push argument {index}\n@ARG\nD=M\n@{index}\n'
                +'A=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'local': f'// push local {index}\n@LCL\nD=M\n@{index}\n'
                +'A=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'static': f'// push static {index}\n@{self.file_name}.{index}\n'
                +'D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'constant': f'// push constant {index}\n@{index}\n'
                +'D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'this': f'// push this {index}\n@THIS\nD=M\n@{index}\n'
                +'A=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'that': f'// push that {index}\n@THAT\nD=M\n@{index}\n'
                +'A=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'pointer': f'// push pointer {index}\n@{this_or_that}\n'
                +'D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
            'temp': f'// push temp {index}\n@R{index+5}\n'
                +'D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n',
        }
        self.asmf.write(push_cmd_table[segment])

    def __write_pop(self, segment, index):
        if segment == 'pointer':
            this_or_that = ['THIS', 'THAT'][index]
        else:
            this_or_that = ''

        push_cmd_table = {
            'argument': f'// pop argument {index}\n@ARG\nD=M\n@{index}\n'
                +'D=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n',
            'local': f'// pop local {index}\n@LCL\nD=M\n@{index}\n'
                +'D=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n',
            'static': f'// pop static {index}\n@SP\nAM=M-1\nD=M\n'
                +f'@{self.file_name}.{index}\nM=D\n',
            'this': f'// pop this {index}\n@THIS\nD=M\n@{index}\n'
                +'D=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n',
            'that': f'// pop that {index}\n@THAT\nD=M\n@{index}\n'
                +'D=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n',
            'pointer': f'// pop pointer {index}\n@SP\nAM=M-1\nD=M\n'
                +f'@{this_or_that}\nM=D\n',
            'temp': f'// pop temp {index}\n@SP\nAM=M-1\nD=M\n'
                +f'@R{index+5}\nM=D\n',
        }
        self.asmf.write(push_cmd_table[segment])

    def write_init(self):
        self.asmf.write('@256\nD=A\n@SP\nM=D\n')
        self.write_call('Sys.init')

    def write_label(self, label):
        self.asmf.write(f'// label {label}\n({label})\n')

    def write_goto(self, label):
        self.asmf.write(f'// goto {label}\n@{label}\n0;JMP\n')

    def write_if(self, label):
        self.asmf.write(f'// if-goto {label}\n@SP\nAM=M-1\nD=M\n\n@{label}\nD;JNE\n')

    def write_call(self, function_name, num_args=0):
        push_cmds = '@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        push_return_address = f'//     push return-address\n'\
            +f'@CALL{CodeWriter.label_counter}\nD=A\n' + push_cmds
        push_lcl = f'//     push LCL\n@LCL\nD=M\n' + push_cmds
        push_arg = f'//     push ARG\n@ARG\nD=M\n' + push_cmds
        push_this = f'//     push THIS\n@THIS\nD=M\n' + push_cmds
        push_that = f'//     push THAT\n@THAT\nD=M\n' + push_cmds
        arg = f'//     ARG=SP-n-5\n@SP\nD=M\n@{num_args+5}\nD=D-A\n@ARG\nM=D\n'
        lcl = '//     LCL=SP\n@SP\nD=M\n@LCL\nM=D\n'
        goto = f'//     goto {function_name}\n@{function_name}\n0;JMP\n'
        return_address = f'(CALL{CodeWriter.label_counter})\n'
        self.asmf.write(f'// call {function_name} {num_args}\n' + push_return_address)
        self.asmf.write(push_lcl + push_arg + push_this + push_that  + arg + lcl + goto + return_address)
        CodeWriter.label_counter += 1

    def write_return(self):
        frame = '//     FRAME=LCL\n@LCL\nD=M\n@R14\nM=D\n'
        ret = '//     RET=*(FRAME-5)\n@R14\nD=M\n@5\nA=D-A\nD=M\n@R15\nM=D\n'
        parg = '//     *ARG=pop()\n@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n'
        sp = '//     SP=ARG+1\n@ARG\nD=M+1\n@SP\nM=D\n'
        that = '//     THAT=*(FRAME-1)\n@R14\nA=M-1\nD=M\n@THAT\nM=D\n'
        this = '//     THIS=*(FRAME-2)\n@R14\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n'
        arg = '//     ARG=*(FRAME-3)\n@R14\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n'
        lcl = '//     LCL=*(FRAME-4)\n@R14\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n'
        goto = '//     goto RET\n@R15\nA=M\n0;JMP\n'
        self.asmf.write('// return\n' + frame + ret + parg + sp)
        self.asmf.write(that + this + arg + lcl + goto)

    def write_function(self, function_name, num_locals=0):
        self.asmf.write(f'// function {function_name} {num_locals}\n({function_name})\n')
        for i in range(num_locals):
            self.__write_push('constant', 0)

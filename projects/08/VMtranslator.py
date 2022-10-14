import sys
import os
import vmparser as ps
import vmcodewriter as cw

def main():
    vmfilepath = sys.argv[1]
    
    if os.path.isdir(vmfilepath):
        if vmfilepath[-1] == '/':
            vmfilelist = [vmfilepath + _ for _ in os.listdir(vmfilepath) if _[-3:]=='.vm']
            asmfile = vmfilepath + vmfilepath.split('/')[-2] + '.asm'
        else:
            vmfilelist = [vmfilepath + '/' + _ for _ in os.listdir(vmfilepath) if _[-3:]=='.vm']
            asmfile = vmfilepath + '/' + vmfilepath.split('/')[-1]+ '.asm'
    elif os.path.isfile(vmfilepath) and vmfilepath[-3:]=='.vm':
        vmfilelist = [vmfilepath]
        asmfile = vmfilepath[:-3] + '.asm'
    else:
        print('Error')
        return

    codewriter = cw.CodeWriter(asmfile)

    codewriter.write_init()

    for vmfile in vmfilelist:
        codewriter.set_file_name(os.path.basename(vmfile))
        parser = ps.Parser(vmfile)
        
        while parser.has_more_commands():
            parser.advance()

            if parser.command_type() == 'C_ARITHMETIC':
                codewriter.write_arithmetic(parser.arg1())
            elif parser.command_type() in ('C_PUSH', 'C_POP'):
                codewriter.write_push_pop(
                    parser.command_type(), parser.arg1(), parser.arg2())
            elif parser.command_type() == 'C_LABEL':
                codewriter.write_label(parser.arg1())
            elif parser.command_type() == 'C_GOTO':
                codewriter.write_goto(parser.arg1())
            elif parser.command_type() == 'C_IF':
                codewriter.write_if(parser.arg1())
            elif parser.command_type() == 'C_FUNCTION':
                codewriter.write_function(parser.arg1(), parser.arg2())
            elif parser.command_type() == 'C_RETURN':
                codewriter.write_return()
            elif parser.command_type() == 'C_CALL':
                codewriter.write_call(parser.arg1(), parser.arg2())

    codewriter.close()

if __name__ == '__main__':
    main()

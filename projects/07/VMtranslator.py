import sys
import os
import vmparser as ps
import vmcodewriter as cw

def main():
    vmfilepath = sys.argv[1]
    
    if os.path.isdir(vmfilepath):
        vmfilelist = [vmfilepath + _ for _ in os.listdir(vmfilepath) if _[-3:]=='.vm']
        if vmfilepath[-1] == '/':
            asmfile = vmfilepath[:-1] + '.asm'
        else:
            asmfile = vmfilepath + '.asm'
    elif os.path.isfile(vmfilepath) and vmfilepath[-3:]=='.vm':
        vmfilelist = [vmfilepath]
        asmfile = vmfilepath[:-3] + '.asm'
    else:
        print('Error')
        return

    codewriter = cw.CodeWriter(asmfile)
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
                pass
            elif parser.command_type() == 'C_GOTO':
                pass
            elif parser.command_type() == 'C_IF':
                pass
            elif parser.command_type() == 'C_FUNCTION':
                pass
            elif parser.command_type() == 'C_RETURN':
                pass
            elif parser.command_type() == 'C_CALL':
                pass

        codewriter.close()
        


if __name__ == '__main__':
    main()

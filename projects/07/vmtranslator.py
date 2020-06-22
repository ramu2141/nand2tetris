import sys
import os
import vmparser
import vmcodewriter

def main():
    vmpath = sys.argv[1]
    asmfile = ''
    vmfiles = []

    # vmファイルが単一の場合
    if os.path.isfile(vmpath) and vmpath[-3:] == '.vm':
        vmfiles.append(vmpath)
        asmfile = vmpath[:-2] + 'asm'
    # vmファイルが複数の場合(ディレクトリー指定の場合)
    elif os.path.isdir(vmpath) and vmpath[-1] == '/':
        vmdir = os.path.dirname(vmpath)
        vmfiles = [vmpath + vmf for vmf in os.listdir(vmdir) if vmf[-3:]=='.vm']
        asmfile = vmpath + vmpath[vmpath.rfind('/', 0, -1)+1:-1] + '.asm'
    else:
        return None

    convert(vmfiles, asmfile)


## vm -> asm 変換処理 ##
def convert(vmfiles, asmfile):
    cw = vmcodewriter.CodeWriter(asmfile)

    for vmfile in vmfiles:
        ps = vmparser.Parser(vmfile)
        cw.set_file_name(os.path.basename(vmfile)[:-3])

        while ps.has_more_commands():
            ps.advance()

            if ps.command_type() == 'C_ARITHMETIC':
                cw.write_arithmetic(ps.arg1())
            elif ps.command_type() in ('C_PUSH', 'C_POP'):
                cw.write_push_pop(ps.command_type(), ps.arg1(), ps.arg2())
            elif ps.command_type() == 'C_LABEL':
                pass
            elif ps.command_type() == 'C_GOTO':
                pass
            elif ps.command_type() == 'C_IF':
                pass
            elif ps.command_type() == 'C_FUNCTION':
                pass
            elif ps.command_type() == 'C_RETURN':
                pass
            elif ps.command_type() == 'C_CALL':
                pass

    cw.close()

if __name__ == '__main__':
    main()
# シンボル非対応アセンブラー

import sys
import hparser as ps
import hcode as cd

def main():

    asmfile = sys.argv[1]
    hackfile = asmfile[:-3] + 'hack'
    hackf = open(hackfile, 'w')

    parser = ps.Parser(asmfile)

    while parser.has_more_commands():
        parser.advance()
        
        if parser.command_type() == 'A_COMMAND':

            if parser.symbol()[0].isdigit():
                # アドレスの場合
                hackf.write(f'0{int(parser.symbol()):015b}\n')
            else:
                # シンボルの場合
                pass

        elif parser.command_type() == 'C_COMMAND':
            hackf.write(f'111{cd.comp(parser.comp())}'
                + f'{cd.dest(parser.dest())}{cd.jump(parser.jump())}\n')
        
        elif parser.command_type() == 'L_COMMAND':
            # 出力なし
            pass

        else:
            pass

    hackf.close()

if __name__ == '__main__':
    main()

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

            # アドレスの場合
            if parser.symbol()[0].isdigit():    
                hackf.write('0'
                            + '{:015b}'.format(int(parser.symbol()))
                            + '\n'
                            )
            # シンボルの場合
            else:
                pass

        elif parser.command_type() == 'C_COMMAND':
            hackf.write('111'
                        + cd.comp(parser.comp())
                        + cd.dest(parser.dest())
                        + cd.jump(parser.jump())
                        + '\n'
                        )
        
        elif parser.command_type() == 'L_COMMAND':
            # 出力なし
            pass

        else:
            pass

    hackf.close()

if __name__ == '__main__':
    main()

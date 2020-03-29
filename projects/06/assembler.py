# シンボル対応アセンブラー

import sys
import hparser as ps
import hcode as cd
import hsymtbl as st

def main():

    asmfile = sys.argv[1]
    hackfile = asmfile[:-3] + 'hack'
    hackf = open(hackfile, 'w')

    parser = ps.Parser(asmfile)
    symtbl = st.SymbolTable()

    # 1回目のパス

    rom_address = 0

    while parser.has_more_commands():
        parser.advance()

        if parser.command_type() in ['A_COMMAND', 'C_COMMAND']:
            rom_address += 1
        elif parser.command_type() == 'L_COMMAND':
            if not symtbl.contains(parser.symbol()):
                symtbl.add_entry(parser.symbol(), rom_address)
        else:
            pass

    # 2回目のパス

    parser.reset()
    new_sym_address = 16    # 新規登録シンボル用アドレス(シンボル対応)

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
                # シンボル登録済みの場合
                if symtbl.contains(parser.symbol()):
                    hackf.write('0' 
                                + '{:015b}'.format(symtbl.get_address(parser.symbol()))
                                + '\n'
                                )
                # シンボル未登録の場合
                else:
                    symtbl.add_entry(parser.symbol(), new_sym_address)
                    hackf.write('0' 
                                + '{:015b}'.format(new_sym_address)
                                + '\n'
                                )
                    new_sym_address += 1

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

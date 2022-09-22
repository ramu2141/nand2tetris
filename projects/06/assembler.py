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

            if parser.symbol()[0].isdigit():    
                # アドレスの場合
                hackf.write(f'0{int(parser.symbol()):015b}\n')
            else:
                # シンボルの場合
                if symtbl.contains(parser.symbol()):
                    # シンボル登録済みの場合
                    hackf.write(f'0{symtbl.get_address(parser.symbol()):015b}\n')
                else:
                    # シンボル未登録の場合
                    symtbl.add_entry(parser.symbol(), new_sym_address)
                    hackf.write(f'0{new_sym_address:015b}\n')
                    new_sym_address += 1

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

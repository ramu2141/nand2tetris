# トークナイザーテスト用

import sys
import os

import jack_tokenizer

def main():
    jackfilepath = sys.argv[1]
    
    if os.path.isdir(jackfilepath):
        if jackfilepath[-1] == '/':
            jackfilelist = [jackfilepath + _ for _ in os.listdir(jackfilepath) if _[-5:]=='.jack']
        else:
            jackfilelist = [jackfilepath + '/' + _ for _ in os.listdir(jackfilepath) if _[-5:]=='.jack']
    elif os.path.isfile(jackfilepath) and jackfilepath[-5:]=='.jack':
        jackfilelist = [jackfilepath]
    else:
        print('Error')
        return

    for jackfile in jackfilelist:
        xmlfile = jackfile[:-5] + 'T.xml'
        with open(xmlfile, mode='w') as xmlf:
            write_xml(jack_tokenizer.JackTokenizer(jackfile), xmlf)

def write_xml(jt, xmlf):
    xmlf.write('<tokens>\n')
    while(jt.has_more_tokens()):
        jt.advance()
        if jt.token_type() == 'KEYWORD':
            xmlf.write('<keyword> ' + jt.keyword() + ' </keyword>\n')
        elif jt.token_type() == 'SYMBOL':
            s = jt.symbol()
            if s == '<': s = '&lt;'
            elif s == '>': s = '&gt;'
            elif s == '&': s = '&amp;'
            xmlf.write('<symbol> ' + s + ' </symbol>\n')
        elif jt.token_type() == 'IDENTIFIER':
            xmlf.write('<identifier> ' + jt.identifier() + ' </identifier>\n')
        elif jt.token_type() == 'INT_CONST':
            xmlf.write('<integerConstant> ' + jt.int_val() + ' </integerConstant>\n')
        elif jt.token_type() == 'STRING_CONST':
            xmlf.write('<stringConstant> ' + jt.string_val() + ' </stringConstant>\n')
        else:
           pass

    xmlf.write('</tokens>\n')

if __name__ == '__main__':
    main()

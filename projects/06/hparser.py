import re

class Parser:
    def __init__(self, asmfile):
        with open(asmfile, 'r') as self.asmf:
            self.commands = self.asmf.readlines()
            self.count = 0

    def has_more_commands(self):
        if self.count < len(self.commands):
            return True
        else:
            return False

    def advance(self):
        while(True):
            cmd = self.commands[self.count].strip()
            self.count += 1

            
            if cmd != '' and cmd[0:2] != '//':
                # 空行でもコメント行でもないとき
                
                if '//' in cmd:
                    # //が見つかれば、それより手前までを取得
                    self.cur_cmd = cmd[:cmd.find('//')].strip()
                else:
                    # //が見つからなければ、一行全て取得
                    self.cur_cmd = cmd
                break

            else:
                # 空行もしくはコメント行の場合、何もせず次の行に進む
                pass
        
    def command_type(self):
        
        if re.match(r'^@[0-9]+$', self.cur_cmd):
            # @数字
            return 'A_COMMAND'
        elif re.match(r'^@[a-zA-Z_.$:][a-zA-Z_.$:0-9]*$', self.cur_cmd):
            # @シンボル
            return 'A_COMMAND'
        elif re.match(r'^[ADM]{1,3}=[01ADM\-!+&|]+;J[A-Z]{2}$', self.cur_cmd):
            # dest=comp;jump
            return 'C_COMMAND'
        elif re.match(r'^[ADM]{1,3}=[01ADM\-!+&|]+$', self.cur_cmd):
            # dest=comp
            return 'C_COMMAND'
        elif re.match(r'^[01ADM\-!+&|]+;J[A-Z]{2}$', self.cur_cmd):
            # comp;jump
            return 'C_COMMAND'
        elif re.match(r'^\([a-zA-Z_.$:][a-zA-Z_.$:0-9]*\)$', self.cur_cmd):
            # (シンボル)
            return 'L_COMMAND'
        else:
            return None
    
    def symbol(self):
        if self.cur_cmd[0]=='@':
            return self.cur_cmd[1:]
        elif self.cur_cmd[0]=='(':
            return self.cur_cmd[1:-1]

    def dest(self):
        eq = self.cur_cmd.find('=')
        if eq > 0:
            return self.cur_cmd[:eq]
        else:
            return None
    
    def comp(self):
        sc = self.cur_cmd.find(';')
        eq = self.cur_cmd.find('=')

        if eq > 0 and sc > 0:
            # =も;もある場合
            return self.cur_cmd[eq+1:sc]
        elif eq > 0 and sc < 0:
            # ;が無い場合
            return self.cur_cmd[eq+1:]
        elif eq < 0 and sc > 0:
            # =が無い場合
            return self.cur_cmd[:sc]
        else:
            return None

    def jump(self):
        sc = self.cur_cmd.find(';')
        if sc > 0:
            return self.cur_cmd[sc+1:]
        else:
            return None

    # シンボルを含むプログラム用
    # 次に読むコマンドを先頭コマンドにする
    def reset(self):
        self.count = 0
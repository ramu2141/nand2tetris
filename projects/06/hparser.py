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

            # 空行でもコメント行でもないとき
            if cmd != '' and cmd[0:2] != '//':
                # //が見つかれば、それより手前までを取得
                if '//' in cmd:
                    self.cur_cmd = cmd[:cmd.find('//')].strip()
                # //が見つからなければ、一行全て取得
                else:
                    self.cur_cmd = cmd
                break
            # 空行もしくはコメント行の場合、何もせず次の行に進む
            else:
                pass
        
    def command_type(self):
        # @数字
        if re.match(r'^@[0-9]+$', self.cur_cmd):
            return 'A_COMMAND'
        # @シンボル
        elif re.match(r'^@[a-zA-Z_.$:][a-zA-Z_.$:0-9]*$', self.cur_cmd):
            return 'A_COMMAND'
        # dest=comp;jump
        elif re.match(r'^[ADM]{1,3}=[01ADM\-!+&|]+;J[A-Z]{2}$', self.cur_cmd):
            return 'C_COMMAND'
        # dest=comp
        elif re.match(r'^[ADM]{1,3}=[01ADM\-!+&|]+$', self.cur_cmd):
            return 'C_COMMAND'
        # comp;jump
        elif re.match(r'^[01ADM\-!+&|]+;J[A-Z]{2}$', self.cur_cmd):
            return 'C_COMMAND'
        # (シンボル)
        elif re.match(r'^\([a-zA-Z_.$:][a-zA-Z_.$:0-9]*\)$', self.cur_cmd):
            return 'L_COMMAND'
        # それ以外
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

        # =も;もある場合
        if eq > 0 and sc > 0:
            return self.cur_cmd[eq+1:sc]
        # ;が無い場合
        elif eq > 0 and sc < 0:
            return self.cur_cmd[eq+1:]
        # =が無い場合
        elif eq < 0 and sc > 0:
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
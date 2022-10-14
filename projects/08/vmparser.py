class Parser:
    def __init__(self, vmfile):
        with open(vmfile, 'r') as self.asmf:
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
                    self.cur_cmd = cmd[:cmd.find('//')].strip().split()
                else:
                    # //が見つからなければ、一行全て取得
                    self.cur_cmd = cmd.split()
                break

            else:
                # 空行もしくはコメント行の場合、何もせず次の行に進む
                pass

    def command_type(self):
        cmd_type = {
            'add':'C_ARITHMETIC',
            'sub':'C_ARITHMETIC',
            'neg':'C_ARITHMETIC',
            'eq':'C_ARITHMETIC',
            'gt':'C_ARITHMETIC',
            'lt':'C_ARITHMETIC',
            'and':'C_ARITHMETIC',
            'or':'C_ARITHMETIC',
            'not':'C_ARITHMETIC',
            'push':'C_PUSH',
            'pop':'C_POP',
            'label':'C_LABEL',
            'goto':'C_GOTO',
            'if-goto':'C_IF',
            'function':'C_FUNCTION',
            'return':'C_RETURN',
            'call':'C_CALL',
        }

        if self.cur_cmd[0] in cmd_type:
            self.cur_cmd_type = cmd_type[self.cur_cmd[0]]
            return self.cur_cmd_type

    def arg1(self):
        if self.cur_cmd_type == 'C_ARITHMETIC':
            return self.cur_cmd[0]
        elif self.cur_cmd_type == 'C_RETURN':
            return None
        elif len(self.cur_cmd) > 1:
            return self.cur_cmd[1]
        else:
            return None

    def arg2(self):
        if len(self.cur_cmd) < 3:
            return None
            
        if self.cur_cmd_type in ('C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL'):
            return int(self.cur_cmd[2])
        else:
            return None

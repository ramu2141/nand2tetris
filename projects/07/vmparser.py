class Parser:

    cmd_tbl = {
        'add'      : 'C_ARITHMETIC',
        'sub'      : 'C_ARITHMETIC',
        'neg'      : 'C_ARITHMETIC',
        'eq'       : 'C_ARITHMETIC',
        'gt'       : 'C_ARITHMETIC',
        'lt'       : 'C_ARITHMETIC',
        'and'      : 'C_ARITHMETIC',
        'or'       : 'C_ARITHMETIC',
        'not'      : 'C_ARITHMETIC',
        'push'     : 'C_PUSH',
        'pop'      : 'C_POP',
        'label'    : 'C_LABEL',
        'goto'     : 'C_GOTO',
        'if-goto'  : 'C_IF',
        'function' : 'C_FUNCTION',
        'return'   : 'C_RETURN',
    }

    def __init__(self, vmfile):
        with open(vmfile, 'r') as self.vmf:
            self.commands = self.vmf.readlines()
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
        self.cmd_type = Parser.cmd_tbl[self.cur_cmd.split()[0]]
        return self.cmd_type

    def arg1(self):
        if self.cmd_type == 'C_ARITHMETIC':
            return self.cur_cmd.split()[0]
        else:
            return self.cur_cmd.split()[1]

    def arg2(self):
        return int(self.cur_cmd.split()[2])
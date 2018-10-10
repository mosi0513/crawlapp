
from scheduler import Schedule

import os

def main():
    s = Schedule()
    s.go()


def run():
    print('操作配置信息请按1')
    print('启动程序请按0')
    nums = input()
    if nums == '1':
        main()
    elif nums == '0':
        os.system('mitmdump -s huafen.py & python3 start.py')
    else:
        print('输出有误， 退出程序')


if __name__ == '__main__':
    run()

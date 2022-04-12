import time
import sys
from tqdm import tqdm
import random
import Serial
import Base_func
import numpy as np

sys.path.append(r'D:/FGO_R2')


# def character_skill(character_no, skill_no, para=None):  # 角色编号，技能编号，选人（可选）
#     Current_state.WaitForBattleStart()
#     Position = (
#         416 - np.random.randint(0, 22) + (character_no - 2) * 263 + (skill_no - 2) * 80, 500 - np.random.randint(0, 30))
#     Serial.touch(Position[0], Position[1])
#     if para != None:
#         Position = (605 - np.random.randint(0, 131) + (para - 2) * 263, 430 - np.random.randint(0, 120))  # 技能选人
#         Serial.touch(Position[0], Position[1])
#     time.sleep(3)  # 等待技能动画时间
#
#     print(' Character{}\'s skill{} has pressed'.format(character_no, skill_no))


Serial.port_open('com5')  # 写入通讯的串口号
Serial.mouse_set_zero()
while():
    Flag, Position = Base_func.match_template('roll')
    if Flag:
        Serial.touch(Position[0] , Position[1] )
Serial.port_close()
print(' All done!')


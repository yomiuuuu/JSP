import numpy as np
from time import perf_counter
from JSP import FT
import random
import copy

perf_counter()

# 时间
PT = PT = [[1,3,6,7,3,6],[8,5,10,10,10,4],[5,4,8,9,1,7],[5,5,5,3,8,9],[9,3,5,4,3,1],[3,3,9,10,4,1]]
# 机器
MN = [[3,1,2,4,6,5],[2,3,5,6,1,4],[3,4,6,1,2,5],[2,1,3,4,5,6],[3,2,5,6,1,4],[2,4,6,1,5,3]]

# 初始化
Ft=FT(PT,MN)
S=[0 for i in range(Ft.JobNum)]
dimension = copy.copy(Ft.O_num)  # 各工件工序数集
for i in range(Ft.JobNum):
    dimension[i] += 1
dimension.append(Ft.JobNum)
Q = np.zeros(dimension)  # Q初始化为0列表,其维度为每个工件的工序数*工件数

# 基本的数据
alpha=0.1
gamma=0.9
epsilon=0.8     # 贪婪
episode_num=10000
BestFinishTime=100

# 循环
for e in range(episode_num):
    # 每一次循环都要初始化的
    Ft.reset()
    S=[0 for i in range(Ft.JobNum)] # 已完成工序数
    A_list=[]   # 当前未被加工的工件
    C = []  # 新加工件的完工时间
    startTime=[[0 for j in range(Ft.JobNum)] for i in range(Ft.JobNum)]    # 各个工序的开工时间
    finTime=Ft.CostJob  # 各个工序的完工时间
    MfinTime=Ft.CostMac     # 机器的完工时间
    m_state=[0 for i in range(6)]   # 机器状态 0为未工作
    j_state=[0 for i in range(6)]   # 工件状态 0为未工作
    timeIndex=0     # 计时器
    finiJobNum = 0  # 加工完的工件数

    # 存在未加工的工件和机器
    while finiJobNum<6:
        A_list=Ft.getList(j_state,S)
        while len(A_list)>0:
            x=np.random.random()
            if x<epsilon:   # 选择最优Q
                A = A_list[0] - 1
                for j in A_list:
                    # 选择较大Q
                    j-=1
                    if Q[S[0]][S[1]][S[2]][S[3]][S[4]][S[5]][j] > Q[S[0]][S[1]][S[2]][S[3]][S[4]][S[5]][A]:
                        A = j
                proNum = S[A]  # 正在加工工序编号-1(已完成数
                proMac = MN[A][proNum]-1  # 正在加工机器编号-1
                if m_state[proMac] == 0:
                    # 该工件的加工机器空闲
                    m_state[proMac] = 1
                    j_state[A] = 1

                    # 写入开工完工时间
                    startTime[A][proNum] = timeIndex  # 各个工序的开工时间
                    finTime[A][proNum] = PT[A][proNum] + timeIndex  # 各个工序的完工时间
                    MfinTime[proMac] = PT[A][proNum] + timeIndex  # 机器的完工时间
                    A_list.remove(A + 1)

                    # 更新c
                    C.append(Ft.schedul(finTime))
                    # print('C' + str(C))

                    # 更新Q
                    S_next = copy.copy(S)
                    S_next[A] += 1
                    if len(C) > 1 and C[-1] - C[-2] > 0:
                        R = 1 / (C[-1] - C[-2])
                    else:
                        R = 1
                    Q[S[0]][S[1]][S[2]][S[3]][S[4]][S[5]][A] += alpha * (R + gamma * np.max(Q[S_next[0]][S_next[1]][S_next[2]][S_next[3]][S_next[4]][S_next[5]]) - Q[S[0]][S[1]][S[2]][S[3]][S[4]][S[5]][A])
                    S = S_next
                else:
                    # 该机器不空闲
                    A_list.remove(A + 1)

            else:   # 随机
                A=np.random.choice(A_list)-1
                proNum = S[A]  # 正在加工工序编号-1(已完成数
                proMac = MN[A][proNum]-1  # 正在加工机器编号-1
                if m_state[proMac] == 0:
                    # 该工件的加工机器空闲
                    m_state[proMac]=1
                    j_state[A]=1

                    # 写入开工完工时间
                    startTime[A][proNum] = timeIndex  # 各个工序的开工时间
                    finTime[A][proNum] = PT[A][proNum] + timeIndex  # 各个工序的完工时间
                    MfinTime[proMac] = PT[A][proNum] + timeIndex  # 机器的完工时间
                    A_list.remove(A+1)

                    # 更新c
                    C.append(Ft.schedul(finTime))
                    # print('C' + str(C))

                    # 更新Q
                    S_next = copy.copy(S)
                    S_next[A] += 1
                    if len(C) > 1 and C[-1] - C[-2] > 0:
                        R = 1 / (C[-1] - C[-2])
                    else:
                        R = 1
                    Q[S[0]][S[1]][S[2]][S[3]][S[4]][S[5]][A] += alpha * (
                            R + gamma * np.max(
                        Q[S_next[0]][S_next[1]][S_next[2]][S_next[3]][S_next[4]][S_next[5]]) -
                            Q[S[0]][S[1]][S[2]][S[3]][S[4]][S[5]][A])
                    S = S_next
                else:
                    # 该机器不空闲
                    A_list.remove(A+1)

        timeIndex+=1
        #print('时间'+str(timeIndex))

        m_state = Ft.MacReset(timeIndex, m_state, MfinTime)
        j_state = Ft.JobReset(timeIndex, j_state, finTime)

        finiJobNum = 0  # 加工完的工件数
        for i in S:
            if i == 6:
                finiJobNum += 1

    if finiJobNum == 6:  # 全部加工完了
        if C[-1] < BestFinishTime:
            BestFinishTime = C[-1]
            print('开工'+str(startTime))
            print('完工'+str(finTime))
            print("运行时间：" + str(perf_counter()))
            print(BestFinishTime)


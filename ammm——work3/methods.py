import random
import copy
import numpy as np
# 随机生成单个染色体
def com_tr(t_table):
    topo_order = []
    for j_num, o_num in enumerate(t_table):  # 根据时间表获取工件数索引和其工序列表
        topo_order = topo_order+(np.ones([1, len(o_num)], int) * (j_num + 1)).tolist()
    combin = []
    for li in topo_order:  # 将列表中各工件独立列表加起来
        combin = combin+li

    random.shuffle(combin)  # 随机打乱列表中元素
    return combin

# 种群初始化(种群大小，染色体
def init_population(pop_size, chrom):
    pop = []
    for i in range(pop_size):
        c = copy.deepcopy(chrom)    # deepcopy的是原对象 chrom即使改变也不会影响c
        random.shuffle(c)
        pop.append(c)
    return pop

def Arrange(li,t_table,m_table):
    Jfinish=[[0 for i in range(6)]for i in range(6)]
    Mfinish=[0 for i in range(6)]
    Jprocess=[0 for i in range(6)]  # 工件已完成工序数
    start=[[0 for i in range(6)]for i in range(6)]
    for i in li:
        # i是编号 -1才是下标
        i-=1
        Mnum=m_table[i][Jprocess[i]]-1    # 加工机器下标
        if Jprocess[i]==0:
            start[i][Jprocess[i]]=0
            Jfinish[i][Jprocess[i]]=Mfinish[Mnum]+t_table[i][Jprocess[i]]
            Mfinish[Mnum]=Jfinish[i][Jprocess[i]]
        else:
            start[i][Jprocess[i]]=max(Mfinish[Mnum],Jfinish[i][Jprocess[i]-1])
            Jfinish[i][Jprocess[i]]=max(Mfinish[Mnum],Jfinish[i][Jprocess[i]-1])+t_table[i][Jprocess[i]]   # 机器和该工件的上一工序谁后完工
            Mfinish[Mnum] = Jfinish[i][Jprocess[i]]
        Jprocess[i]+=1
        #print('process',Jprocess)
        #print('jf',Jfinish)
        #print('mf',Mfinish)
    return Jfinish,Mfinish

def two_points_cross(chro1, chro2):
    # 不改变原始数据进行操作
    chro1_1 = copy.deepcopy(chro1)
    chro2_1 = copy.deepcopy(chro2)
    # 交叉位置，point1<point2
    point1 = random.randint(0, len(chro1_1))
    point2 = random.randint(0, len(chro1_1))
    while point1>point2 or point1==point2:
        point1 = random.randint(0, len(chro1_1))
        point2 = random.randint(0, len(chro1_1))

    # 记录交叉片段
    frag1 = chro1[point1:point2]
    frag2 = chro2[point1:point2]

    random.shuffle(frag1)
    random.shuffle(frag2)
    # 交叉
    chro1_1[point1:point2], chro2_1[point1:point2] = chro2_1[point1:point2], chro1_1[point1:point2]
    child1 = chro1_1[:point1] + frag1 + chro1_1[point2:]
    child2 = chro2_1[:point1] + frag2 + chro2_1[point2:]
    return child1, child2

def mutation(chrom):
    point1 = random.randint(0, len(chrom) - 1)
    point2 = random.randint(0, len(chrom) - 1)
    while point1 > point2 or point1 == point2:
        point1 = random.randint(0, len(chrom) - 1)
        point2 = random.randint(0, len(chrom) - 1)
    chrom[point1], chrom[point2] = chrom[point2], chrom[point1]
    return chrom
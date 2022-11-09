import copy
import random
from methods import com_tr,init_population,Arrange,two_points_cross,mutation

jobs = 6  # 工件数
machines = 6  # 机器数
t_table = [[1,3,6,7,3,6],[8,5,10,10,10,4],[5,4,8,9,1,7],[5,5,5,3,8,9],[9,3,5,4,3,1],[3,3,9,10,4,1]] # 时间表
m_table = [[3,1,2,4,6,5],[2,3,5,6,1,4],[3,4,6,1,2,5],[2,1,3,4,5,6],[3,2,5,6,1,4],[2,4,6,1,5,3]]   # 机器表

pc=0.8  # 交叉概率
pm=0.9  # 变异概率
pop_size=8  # 种群大小
episode_num=1000    # 迭代次数
bestFinishTime=100    # 全局最短时间
bestCombin=[]   #最优工序
bestJTime=[]    #最优加工时间表

combin = com_tr(t_table)    # 生成单个染色体 加工工序
population = init_population(pop_size, combin)  # 生成种群

# 根据工序安排机器
TotalJTime=[]   # 种群工件加工时间
TotalMTime=[]   # 种群机器加工时间
bestTime=[]     # 每个染色体的最优解
for i in population:
    JfinTime,MfinTime=Arrange(i,t_table,m_table)
    TotalJTime.append(JfinTime)
    TotalMTime.append(MfinTime)
    bestTime.append(max(MfinTime))
#print(TotalJTime,TotalMTime)

for i in range(episode_num):
    # 交叉变异
    pop_new=copy.deepcopy(population)
    tempList=list(range(pop_size))
    while(len(tempList)>1):
        index1=random.choice(tempList)
        index2=random.choice(tempList)
        while index1==index2:
            index2 = random.choice(tempList)
        if random.random()>pc:
            chrom_new1, chrom_new2 = two_points_cross(pop_new[index1],
                                                      pop_new[random.randint(round(pop_size / 2), pop_size - 1)])
            # 如果子代更优就替换，否则不换
            JTime1,MTime1=Arrange(chrom_new1, t_table, m_table)
            if max(MTime1)<max(bestTime):
                index=bestTime.index(max(bestTime)) # 最大解的下标
                TotalJTime[index]=JTime1
                TotalMTime[index]=MTime1
                bestTime[index]=max(MTime1)
            JTime2, MTime2 = Arrange(chrom_new2, t_table, m_table)
            if max(MTime2) < max(bestTime):
                index = bestTime.index(max(bestTime))  # 最大解的下标
                TotalJTime[index] = JTime2
                TotalMTime[index] = MTime2
                bestTime[index] = max(MTime2)
        tempList.remove(index1)
        tempList.remove(index2)

    # 突变
    for i in range(pop_size):
        if random.random()>pm:
            chrom_new3=mutation(population[i])
            JTime3, MTime3 = Arrange(chrom_new3, t_table, m_table)
            if max(MTime3) < max(bestTime):
                index = bestTime.index(max(bestTime))  # 最大解的下标
                TotalJTime[index] = JTime3
                TotalMTime[index] = MTime3
                bestTime[index] = max(MTime3)

    # 更新最优解
    if min(bestTime)<bestFinishTime:
        index3=bestTime.index(min(bestTime))
        bestFinishTime=bestTime[index3]
        bestCombin = population[index3]
        bestJTime = TotalJTime[index3]


print('makespan',bestFinishTime)
print('工序',bestCombin)
print('完工时间',bestJTime)
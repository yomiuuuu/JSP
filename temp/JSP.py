
class FT:
    def __init__(self, PT, MN):
        self.PT=PT
        self.MN=MN
        self.JobNum=len(self.PT)
        self.O_num = [len(self.PT[i]) for i in range(self.JobNum)]


    def reset(self):
        self.CostMac = [0 for i in range(self.JobNum)]    # 该机器加工结束时间
        self.CostJob = [[0 for i in range(self.JobNum)]for j in range(self.JobNum)]   # 每个工件每个工序加工结束时间

    # 计算空闲个数 0为未工作
    def countSpare(self,lis):
        count=0
        for i in lis:
            if i==0:
                count+=1
        return count

    # 空闲Job编号 没有正在工作并且没
    def getList(self,l,S):
        Joblist=[]
        for i in range(len(l)):
            if l[i]==0:
                if S[i]<6:
                    Joblist.append(i+1)
        return Joblist

    def schedul(self,start):
        Cmax=0
        for i in start:
            if max(i)>Cmax:
                Cmax=max(i)
        return Cmax

    def MacReset(self,time,m_state,MfinTime):
        for i in range(len(MfinTime)):
            if MfinTime[i]<=time:
                m_state[i]=0
        return m_state

    def JobReset(self,time,j_state,finTime):
        for i in range(len(finTime)):
            if time>=max(finTime[i]):
                j_state[i]=0
        return j_state
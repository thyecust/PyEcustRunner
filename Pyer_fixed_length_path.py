import vertex

class Pyer_fixed_length_path(object):
    '''
    计算固定长度的路径
    '''
    def __init__(self,start,vlist,edges,vset):
        self.Vlist=vlist
        self.Vset=vset
        self.edges=edges
        self.current=start
        self.path=[0,start]

    def complete_path(self,length):
        #补完跑完目标点后剩余距离
        origin=self.path.copy()#复制当前刚好走完目标点的路径
        des=self.current#补完路径的终点
        dist=vertex.get_path(self.current,des,self.Vlist,self.Vset,self.edges).get('dist')
        for each in self.Vlist:#附加优先度后选择优先度最高（即权值最小）的目标作为终点
            if vertex.get_path(self.current,each.vid,self.Vlist,self.Vset,self.edges):
                if (vertex.get_path(self.current,each.vid,self.Vlist,self.Vset,self.edges).get('dist')+self.Vlist[each.vid].priority)<(dist+self.Vlist[des].priority):
                    des=each.vid
                    dist=vertex.get_path(self.current,each.vid,self.Vlist,self.Vset,self.edges).get('dist')
        #为path加上到终点的最短路径
        self.path+=vertex.get_path(self.current,des,self.Vlist,self.Vset,self.edges).get('path')[1:]
        self.path[0]+=vertex.get_path(self.current,des,self.Vlist,self.Vset,self.edges).get('dist')
        self.current=des
        temp_path=[self.current]#长度不足时的补完路径
        last=None
        while self.path[0]<length and length!=float('inf'):
            #当长度不足时，不断寻找当前点的最近相邻点构成环，直到满足长度
            temp1=float('inf')
            for each in self.Vlist[self.current].outlist:
                if self.edges[(self.current,each)]<temp1 and each!=last:
                    #为避免来回重复走一条路，判断时排除上一个走过的点
                    temp1=self.edges[(self.current,each)]
                    temp2=each
            self.path[0]+=temp1*2#因为是回路，找到的路径长度翻倍加到原长度上
            last=temp_path[-1]
            temp_path.append(temp2)
            self.current=temp2
        self.path+=temp_path[1:]+temp_path[::-1][1:]#所得路径正序倒序相加构成回路
        while self.path[0]>length*1.1 and len(self.path)>len(origin):
            #理想长度为目标长度1-1.1倍范围内，超出长度则削减路径
            #判断path长度大于origin确保包含目标点的路径不会被删除
            delt=self.path.pop()
            self.path[0]-=vertex.get_path(self.path[-1],delt,self.Vlist,self.Vset,self.edges).get('dist')
            if self.path[0]<length:
                #若削减后小于目标长度，立刻补回削减路径，结束循环
                self.path[0]+=vertex.get_path(self.path[-1],delt,self.Vlist,self.Vset,self.edges).get('dist')
                self.path.append(delt)
                break

    def path_to(self,markers,length,end=None):
        #单人运动路径计算
        for each in markers:
            #按顺序计算各目标点之间最短距离，组成路径
            self.path+=vertex.get_path(self.current,each,self.Vlist,self.Vset,self.edges).get('path')[1:]
            self.path[0]+=vertex.get_path(self.current,each,self.Vlist,self.Vset,self.edges).get('dist')
            self.current=each
        if end!=None:#若输入目标终点，则目标终点优先度为最高，即负无穷
            self.Vlist[end].priority=float('-inf')
        self.complete_path(length)#补完剩余距离
        Dict={}
        Dict['dist']=self.path[0]
        Dict['path']=self.path[1:]
        return Dict

#测试
if __name__=="__main__":
    path1=Pyer_fixed_length_path(1,vertex.Vlist,vertex.edges)
    print(path1.path_to([4,77],length=2000))
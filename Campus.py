import json
import vertex
from vertex import Vertex
from Pyer_fixed_length_path import Pyer_fixed_length_path

class Campus(object):
    def __init__(self,graph,priority):
        self.Vlist=[]
        self.Vset=set()
        self.edges = dict()
        self.adj=graph['adj']

        for i in self.adj:
            list=[]
            for j in i[1:]:
                self.edges[(i[0],j[0])]=j[1]
                list.append(j[0])
            new=Vertex(i[0],list)
            self.Vlist.append(new)
            self.Vset.add(new)
        for i in priority:
            self.Vlist[i].priority=-1000

    def add_edge(self,l):
        new=len(self.Vlist)
        self.edges[(new,l[0])]=l[2]
        self.edges[(l[0],new)]=l[2]
        self.edges[(new,l[1])]=l[3]
        self.edges[(l[1],new)]=l[3]
        outlist=l[:2]
        added=Vertex(new,outlist)
        self.Vlist.append(added)
        self.Vset.add(added)
        self.Vlist[l[0]].outlist.append(new)
        self.Vlist[l[1]].outlist.append(new)

    def delete_edge(self,d):
        self.edges.pop((d[0],d[1]))
        self.edges.pop((d[1],d[0]))
        self.Vlist[d[0]].outlist.remove(d[1])
        self.Vlist[d[1]].outlist.remove(d[0])

    def get_path(self,start,end,vias=None):
        if vias==None:
            return vertex.get_path(start,end,self.Vlist,self.Vset,self.edges)
        else:
            return self.get_fixed_path(start,vias,float('inf'),end)

    def get_fixed_path(self,start,vias,length,priority=None):
        path=Pyer_fixed_length_path(start,self.Vlist,self.edges,self.Vset)
        return path.path_to(vias,length,priority)

#测试
# f=open('graph.json','r')
# raw=f.read()
# f.close()
# graph = json.loads(raw)
# priority=[20,59,63,66,67,72]
# campus=Campus(graph,priority)

# ae=[[80,127,52,50],[87,88,90,15],[55,129,4,48],[92,98,154,5]]
# vias=[132,133]
# for item in ae:
#     campus.add_edge(item)
# print(campus.get_path(130,131,vias))
# campus.add_edge([0,2,30,52])
# print(campus.get_path(0,2))
# print(campus.get_path(0,4,[1,2,3]))
# print(campus.get_fixed_path(2,[0,23,128],2000,55))

import copy
import json

#顶点类
class Vertex(object):
    def __init__(self,vid,outlist):
        '''
        vid       出边
        outlist   出边指向的顶点id
        know      标志位，默认为假
        dist      到该点的距离，默认为无穷大
        prev      上一个顶点的id，默认为0
        '''
        self.vid=vid
        self.outlist=outlist
        self.know=False
        self.dist=float('inf')
        self.prev=0
        self.priority=0
    def __eq__(self, other):
        if isinstance(other,self.__class__):
           return self.vid==other.vid
        else:
           return False
    def __hash__(self):
        return hash(self.vid)

def get_path(a,b,Vlist,Vset,edges):
    
    vlist=copy.deepcopy(Vlist)
    vset=copy.deepcopy(Vset)
    vlist[a].dist=0
    while(vset):
        v=get_edge_min(vlist,vset)        
        vlist[v].know = True
        for w in vlist[v].outlist:
            if(vlist[w].know is True):
                continue
            if(vlist[w].dist == float('inf')):
                vlist[w].dist = vlist[v].dist + edges[(vlist[v].vid,w)]
                vlist[w].prev = vlist[v].vid
            else:
                if((vlist[v].dist + edges[(vlist[v].vid,w)])<vlist[w].dist):
                    vlist[w].dist = vlist[v].dist + edges[(vlist[v].vid,w)]
                    vlist[w].prev = vlist[v].vid
                else:
                    pass
    if(vlist[b].dist==float('inf')):
        return False
    else:
        Dict={}
        Dict['dist']=vlist[b].dist
        path=[]
        def the_path(x,y):
            path.append(y)
            if x==y:
                return path
            else:
                return the_path(x,vlist[y].prev)
        Dict['path']=the_path(a,b)[::-1]
        return(Dict)

def get_edge_min(vlist,vset):
    the_min=0
    the_id=0
    j=0
    for i in range(0,len(vlist)):
        if(vlist[i].know is True):
            continue
        else:
            if(j==0):
                the_min=vlist[i].dist
                the_id=i
            else:
                if(vlist[i].dist<the_min):
                    the_min=vlist[i].dist
                    the_id=i
            j=j+1
    vset.remove(vlist[the_id])
    return the_id

if __name__=='__main__':
    Dict1=get_path(3,3,Vlist)
    print(Dict1)

    Dict2=get_path(2,5,Vlist)
    print(Dict2)


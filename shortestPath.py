import csv
import numpy as np
import  pandas as pd

def read_data(file_name):
    data=dict()
    with open(file_name, "rt", encoding="utf-8") as file:
        n=int(file.readline())
        for i in range(n):
            value=""
            line=file.readline().split()
            for i in line[1:]:
                value=value+i+" "
            data[line[0]]=value
    return data

def build_subway(**lines):
    for key in lines.keys():
        #取出每条线路的所有站点，但此时还是整个字符串的状态
        value = lines[key]
        #对整个字符穿进行分词处理，并更新字典line信息
        lines[key] = value.split()
    #创建一个无序不重复元素集
    stations = set()
    for key in lines.keys():
        #取出所有站点进去去重处理并存放到stations中
        stations.update(set(lines[key]))
    #创建一个空字典，用来存放邻接表
    system = {}
    #遍历所有站点
    for station in stations:
        #创建一个新的空字典用来存放站点的相邻站点信息，包括站点名和所属线路名
        next_station = {}
        #遍历更新过的lines
        for key in lines:
            #判断站点是否在该线路中
            if station in lines[key]:
                line = lines[key]
                #找出该站点在该线路的下标
                idx = line.index(station)
                if idx == 0:
                    #如果下标为零说明是起始站点，那么在该线路中的相邻站点就只有一个就是下标为1的站点，将其加入邻接表
                    next_station[line[1]] = key
                elif idx == len(line)-1:
                    #如果下标为values值的长度-1说明是终点站，那么在该线路中的相邻站点就只有一个就是下标为values长度-2的站点，将其加入邻接表
                    next_station[line[idx-1]]=key
                else:
                    #剩下的情况就是中间站点，将其两边的站点加入邻接表
                    next_station[line[idx-1]] = key
                    next_station[line[idx+1]] = key
        #更新站点的相邻站点信息
        system[station] = next_station
    return system



def shorter_path(start, goal):
    #BFS算法
    if start == goal:
        return [start]
    explored = set()
    queue = [ [start] ]
    while queue:
        path = queue.pop(0)
        s = path[-1]
        for state, action in bj_subway[s].items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if state == goal:
                    return path2
                else:
                    queue.append(path2)
    return []

def printinfo(start,end):
    nodeSum = 0
    if start not in bj_subway.keys():
        print("请输入正确的出发站点")
        return
    if end not in bj_subway.keys():
        print("请输入正确的终点站")
        return
    path=shorter_path(start,end)
    if(len(path)==1):
        print(path[0])
        return 0
    linename=path[1]
    print("请先乘坐",path[1])
    for i in range(len(path)):
        if((i+1)%2==1):
            print(path[i])
            nodeSum = nodeSum+1
        else:
            if(linename!=path[i] and i!=1):
                print("------换乘",path[i],"-------")
                linename=path[i]
                nodeSum = nodeSum+1
    print('nodeSum = '+ str(nodeSum))
    return nodeSum

if __name__ == '__main__':
    listdata = read_data('C:/Users/PC/Desktop/Subway/shortestPath/hz_data.txt')
    bj_subway = build_subway(**listdata)

    oid_array = np.zeros((720))
    fid_array = np.zeros((720))
    dis_array = np.zeros((720))
    count_array = np.zeros((720, 720))

    # 打开distance.csv文件
    # 获取文件第1列数据OID
    with open("C:/Users/PC/Desktop/Subway/distance.csv") as f:
        reader = csv.reader(f)
        column_0 = [row[0] for row in reader]
        print(column_0)
    # 获取文件第3列数据FID
    with open("C:/Users/PC/Desktop/Subway/distance.csv") as f:
        reader = csv.reader(f)
        column_2 = [row[2] for row in reader]
        print(column_2)
    # 获取文件第4列数据Distance
    with open("C:/Users/PC/Desktop/Subway/distance.csv") as f:
        reader = csv.reader(f)
        column_3 = [row[3] for row in reader]
        print(column_3)

    oid_array = np.array(column_0[1:])
    fid_array = np.array(column_2[1:])
    dis_array = np.array(column_3[1:])

    # i是起点，j是终点
    for i in range(720):
        for j in range(i+1,720):
            print('i = '+str(i)+'  fid_array '+str(i)+'= '+str(fid_array[i]))
            print('j = '+str(j)+'  fid_array '+str(j)+'= '+str(fid_array[j]))
            count_array[i,j] = printinfo(fid_array[i], fid_array[j])

    f = open('C:/Users/PC/Desktop/Subway/PathResult_0.csv','w',newline='', encoding='utf-8')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['OID1','FID1','Distance1','OID2','FID2','Distance2','Delta'])

    for i in range(720):
        for j in range(i+1,720):
            OID1 = oid_array[i]
            FID1 = fid_array[i]
            Distance1 = dis_array[i]
            OID2 = oid_array[j]
            FID2 = fid_array[j]
            Distance2 = dis_array[j]
            Delta = count_array[i,j]
            csv_writer.writerow([OID1, FID1, Distance1, OID2, FID2, Distance2, Delta])

    f.close()

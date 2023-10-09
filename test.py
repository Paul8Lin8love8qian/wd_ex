import json


"""
with open(file_path_2, 'r', encoding='utf-8') as file:
    #data = file.readlines()
    #print(len(data), type(data))
    #print(len(data[0]), type(data[0]))
    

"""

def ex_1():
    # data是list，有917个元素，第一个元素是字符串，长度为120
    with open(file_path_1, 'r', encoding='utf-8') as file:
        data = file.readlines() 
        print(len(data), type(data))
        print(len(data[0]), type(data[0]))

def ex_2():
    #第一行是“[“
    with open(file_path_3, 'r', encoding='utf-8') as file:
        num = 0
        for line in file:
            print(len(line))
            print(line[-2])
            print(line[-1])
            if num >= 2:
                break
            num += 1

def ex_3():
    with open(file_path_3, 'r', encoding='utf-8') as file:
        #函数load()作用为读取JSON文件生成Python对象
        #函数loads()作用为读取JSON 字符串流生成Python对象
        data = json.load(file)
        print(len(data[0]), type(data[0]))
        """
        for line in file:
            data = json.loads(line) #大于1个，loads加载后是一个list，否则知识字典
            print(len(data), type(data))

        num = 0
        for line in file:
            print(len(line), type(line))
            data = json.loads(line)
            print(len(data), type(data))
            if num >= 2:
                break
            num += 1
        """
        for line in file:
            data = json.loads(line) #大于1个，loads加载后是一个list，否则知识字典
            print(len(data), type(data))
        
        

file_path_1 = "C:\\Users\\zsl\\Desktop\\Database\\example\\病例分析题.json"
file_path_2 = "F:\\wikidata\\20141027.json"
file_path_3 = "C:\\Users\\zsl\\Desktop\\Database\\example\\chunk_0.json"
file_path_4 = "E:\\code\\python\\wikidata\\wikidata_test.json"

with open(file_path_4, 'r', encoding='utf-8') as file:
        data = json.load(file)
        print(len(data), type(data))
        print(len(data[0]), type(data[0]))
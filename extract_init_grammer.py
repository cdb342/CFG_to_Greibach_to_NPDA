import re
class extract_init_grammer():
    def __init__(self,index1,index2):
        self.index1=index1
        self.index2=index2
    def load_data(self):
        with open('NPDA-Production.txt', 'r',encoding='utf-8') as f:
            data = f.read().splitlines()#把每一行数据以字符串存储在列表里（不储存换行符）
        return data[self.index1:self.index2]
    def extract_start_symbol(self,data):
        S=re.search('(.*?) ->',data[0]).group(1)
        return S
    def extract_production(self,data):#从输入的数据中抽取产生式并保存成字典格式
        P = {}
        for i in data:
            tem = re.search('(.*?) -> (.*)', i)
            if tem:
                if '|' in tem.group(2):
                    tem2 = set(tem.group(2).split('|'))
                else:
                    tem2 = {tem.group(2)}
                self.add_production(P, tem.group(1),  tem2)
        return P
    def build_terminator_alphabet(self,P):#从产生式中抽取终结符，构造终结符字母表
        VT=set()
        for value in P.values():
            for t in value:
                VT=VT|set(re.findall('[a-zε]',t))#找到所非终结符（所有非终结符都为小写字母或者ε）
        return VT
    def build_nonterminator_alphabet(self,P):
        VN = set()
        for key in P.keys():
            for t in key:
                VN = VN | set(re.findall('[A-Z]', t))#找到所有非终结符（所有非终结符为大写字母）
        return VN
    def add_production(self,P,left,right):
        if left in P.keys():
            P[left].update(right)
        else:
            P.update({left: right})
def init_grammer(ext):
    data=ext.load_data()
    S=ext.extract_start_symbol(data)
    P=ext.extract_production(data)
    VT=ext.build_terminator_alphabet(P)
    VN=ext.build_nonterminator_alphabet(P)
    return VN,VT,P,S
import re
class NPDA():
    def __init__(self):
        pass
    def load_table(self):
        self.table = []
        with open('table-NPDA.txt', 'r',encoding='utf-8') as f:
            self.lines = f.readlines()#要求同一非终结符的产生式在同一行,|符号两边不能有相同串
            self.P=''.join(self.lines)
            #print(self.lines)
    def remove_single_production_and_ε_rule(self):
        while re.search('([A-R]\d?|[T-Z]\d?) -> (ε|.*\|ε)',self.P,re.M):#如果存在直接推导出ε的非终结符
            tem=re.findall('(([A-R]\d?|[T-Z]\d?) -> ε\n)',self.P)#产生式左端非终结符只推导出ε
           # print('tem:',tem,'\n','tem[0]:',tem[1])
            if tem:
                for element in tem:
                    self.P=re.sub(element[0],'',self.P)#删除ε产生式
                    #包含该非终结符的产生式右端中，若该非终结符单独出现
                    self.P=re.sub(' '+element[1]+'\n',' '+'ε'+'\n',self.P)
                    self.P=re.sub(' '+element[1]+'\|',' '+'ε'+'|',self.P)
                    self.P=re.sub('\|' + element[1] + '\|', '|' + 'ε' + '|', self.P)
                    self.P=re.sub('\|' + element[1] + '\n', '|' + 'ε' + '\n', self.P)
                    #若该非终结符与其他符号一起出现
                    self.P=re.sub(element[1],'',self.P)
                print(1,self.P)
            tem=re.findall('(([A-R]\d?|[T-Z]\d?) -> ε)\|.*?\n',self.P)#产生式左端非终结符不只推导出ε，且ε在第一项
            if tem:
                for element in tem:
                    self.P=re.sub(element[0]+'\|',element[1]+' -> ',self.P)#删除ε产生式
                    #包含该非终结符的产生式右端中，若该非终结符单独出现
                    self.P=re.sub(' ' + element[1] + '\n', ' ' + element[1] + '|ε\n', self.P)
                    self.P=re.sub(' ' + element[1] + '\|', ' '+'ε|' + element[1] + '|', self.P)
                    self.P=re.sub('\|' + element[1] + '\|', '|' + 'ε' + '|'+element[1] + '|', self.P)
                    self.P=re.sub('\|' + element[1] + '\n', '|' + element[1] +'|' + 'ε' + '\n', self.P)
                    # 若该非终结符与其他符号一起出现
                    self.P = re.sub('\|' + '(([a-zA-Z0-9]*?)' + element[1] + '([a-zA-Z0-9]*?))' + '\|','|\g<1>|\g<2>\g<3>|', self.P)  # 中间
                    self.P = re.sub('-> ' + '(([a-zA-Z0-9]*?)' + element[1] + '([a-zA-Z0-9]*?))' + '\|','-> \g<1>|\g<2>\g<3>|', self.P)  # 最前
                    self.P = re.sub('\|' + '(([a-zA-Z0-9]*?)' + element[1] + '([a-zA-Z0-9]*?))' + '\n','|\g<1>|\g<2>\g<3>\n', self.P)  # 最后
                    self.P = re.sub('-> ' + '(([a-zA-Z0-9]*?)' + element[1] + '([a-zA-Z0-9]*?))' + '\n','-> \g<1>|\g<2>\g<3>\n', self.P)  # 只有一条
                print(2, self.P)
            tem = re.findall('((([A-R]\d?|[T-Z]\d?) -> .*\|)ε\|).*?\n',self.P)  # 产生式左端非终结符不只推导出ε，且ε在两个|中间
            if tem:
                for element in tem:
                    self.P=re.sub('\|ε','',self.P)#删除ε产生式
                    #包含该非终结符的产生式右端中，若该非终结符单独出现
                    self.P=re.sub(' ' + element[2] + '\n', ' ' + element[2] + '|ε\n', self.P)
                    self.P=re.sub(' ' + element[2] + '\|', ' '+'ε|' + element[2] + '|', self.P)
                    self.P=re.sub('\|' + element[2] + '\|', '|' + 'ε' + '|'+element[2] + '|', self.P)
                    self.P=re.sub('\|' + element[2] + '\n', '|' + element[2] +'|' + 'ε' + '\n', self.P)
                    # 若该非终结符与其他符号一起出现
                    self.P = re.sub('\|' + '(([a-zA-Z0-9]*?)' + element[2] + '([a-zA-Z0-9]*?))' + '\|','|\g<1>|\g<2>\g<3>|', self.P)  # 中间
                    self.P = re.sub('-> ' + '(([a-zA-Z0-9]*?)' + element[2] + '([a-zA-Z0-9]*?))' + '\|','-> \g<1>|\g<2>\g<3>|', self.P)  # 最前
                    self.P = re.sub('\|' + '(([a-zA-Z0-9]*?)' + element[2] + '([a-zA-Z0-9]*?))' + '\n','|\g<1>|\g<2>\g<3>\n', self.P)  # 最后
                    self.P = re.sub('-> ' + '(([a-zA-Z0-9]*?)' + element[2] + '([a-zA-Z0-9]*?))' + '\n','-> \g<1>|\g<2>\g<3>\n', self.P)  # 只有一条
                print(3, self.P)
            tem = re.findall('((([A-R]\d?|[T-Z]\d?) -> .*)\|ε)\n', self.P)  # 产生式左端非终结符不只推导出ε，且ε在|和\n中间
            if tem:
                for element in tem:
                    print(element[0],0,element[1],000,element[2])
                    self.P=re.sub('\|ε','',self.P)#删除ε产生式
                    print(self.P)
                    #包含该非终结符的产生式右端中，若该非终结符单独出现
                    self.P=re.sub(' ' + element[2] + '\n', ' ' + element[2] + '|ε\n', self.P)
                    self.P=re.sub(' ' + element[2] + '\|', ' '+'ε|' + element[2] + '|', self.P)
                    self.P=re.sub('\|' + element[2] + '\|', '|' + 'ε' + '|'+element[2] + '|', self.P)
                    self.P=re.sub('\|' + element[2] + '\n', '|' + element[2] +'|' + 'ε' + '\n', self.P)
                    # 若该非终结符与其他符号一起出现
                    self.P = re.sub('\|' + '(([a-zA-Z0-9]*?)' + element[2] + '([a-zA-Z0-9]*?))' + '\|', '|\g<1>|\g<2>\g<3>|', self.P)  # 中间
                    self.P = re.sub('-> ' + '(([a-zA-Z0-9]*?)' + element[2] + '([a-zA-Z0-9]*?))' + '\|', '-> \g<1>|\g<2>\g<3>|', self.P)#最前
                    self.P = re.sub('\|' +'(([a-zA-Z0-9]*?)'+element[2] +'([a-zA-Z0-9]*?))'+'\n', '|\g<1>|\g<2>\g<3>\n', self.P)#最后
                    self.P = re.sub('-> ' + '(([a-zA-Z0-9]*?)' + element[2] + '([a-zA-Z0-9]*?))' + '\n', '-> \g<1>|\g<2>\g<3>\n',self.P)  # 只有一条
                print(4, self.P)



a=NPDA()
a.load_table()
print(a.P)
a.remove_single_production_and_ε_rule()
print(a.P)
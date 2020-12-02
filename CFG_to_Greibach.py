import re
import copy
import show
class CFG_to_Greibach():
    def __init__(self):
        pass
    '''
    消除多余产生式和无效符号
    '''
    def deleting_superfluous_symbol_and_production(self,VN,VT,P,S):
        #算法2.1步骤1
        VN_1=set()
        P_1=dict()
        #算法2.1步骤2、3
        len1=0
        len2=1
        while(len1!=len2):#len1=len2代表一次循环后集合VN_1没有增大
            len1=len(VN_1)#本次循环开始时VN_1的大小
            for key in P:#对于每一个产生式左部部
                for i in P[key]:#对于该左部对应的所有右部
                    tem = set(re.findall('[A-Z]_[0-9]+|[A-Z]|' + '|'.join(VT), i))
                    if tem.issubset(VT|VN_1):#如果该右部属于VT和VN_1的并集的闭包
                        VN_1.add(key)#把该左部加到VN_1中
            len2 = len(VN_1)#本次循环结束后VN_1的大小
        #算法2.1步骤4
        for key in P:
            string=set()
            for i in P[key]:
                tem=set(re.findall('[A-Z]_[0-9]+|[A-Z]|'+'|'.join(VT),i))
                if tem.issubset(VT | VN_1):
                    string.add(i)
            if string:
                P_1.update({key:string})
        #算法2.2步骤1
        VT_2=set()
        VN_2=set()
        VN_2.add(S)
        #算法2.2步骤2、3
        len11 = 0
        len12 =1
        len21=0
        len22 = 1
        while len11!=len12 or len21!=len22:
            len11 = len(VN_2)#循环开始时VN_2的大小
            len21 = len(VT_2)#循环开始时VT_2的大小
            for key in P_1.keys():
                if key in VN_2:
                    for i in P_1[key]:
                        VN_2=VN_2|set(re.findall('[A-Z]_[0-9]+|[A-Z]',i))
                        VT_2=VT_2|set(re.findall('[a-zε]',i))
            len12 = len(VN_2)#循环结束后VN_2的大小
            len22 = len(VT_2)#循环结束后VT_2的大小
        #算法2.2步骤4
        P_2=dict()
        for key in P_1:
            if key in VN_2:
                string=set()
                for i in P_1[key]:
                    tem = set(re.findall('[A-Z]_[0-9]+|[A-Z]|' + '|'.join(VT), i))
                    if tem.issubset(VT_2 | VN_2):
                        string.add(i)
                if string:
                    P_2.update({key: string})
        return VN_2,VT_2,P_2,S
    '''
    消除空产生式
    '''
    def Eliminate_empty_production(self,VN, VT, P, S):
        W = set()  # 能推导出ε的非终结符集合
        # 把所有能直接推导出ε的非终结符放到W集合中
        for key in P.keys():
            if 'ε' in P[key]:
                W.add(key)
        #如果W集合为空代表文法中没有空产生式
        if not W:
            return VN, VT,P,S
        #如果W集合不为空代表文法中存在空产生式，则把所有能间接推导出ε的非终结符也放入W集合
        P_new = dict()#消除空产生式后的产生式合集
        len1 = 0
        len2 = 1
        '''
        构造W集合
        '''
        while len1 != len2:#当一次循环中W集合没有增大，则循环终止
            len1 = len(W)#本次循环开始前W的大小
            for key in P.keys():
                for i in P[key]:
                    # 如果key直接推导出的右部全部由W中非终结符构成
                    tem = ''.join(W)
                    tem = re.search('[' + tem + ']*', i)
                    if tem:
                        if tem.group() == i:
                            #将key加到W中
                            W.add(key)
            len2 = len(W)#本次循环结束后W的大小
        for key in P.keys():
            right_new = set()#key的新右部
            for i in P[key]:
                i_new = ['']#储存由key的右部i衍生的新右部，刚开始仅有空字符，随着对i从左向右扫描，逐渐添加字符
                for j in range(len(i)):#对于i中的每一个字符
                    if i[j] in W:#如果某一字符在集合W中
                        for t in range(len(i_new)):
                            if i_new[t]=='':
                                i_new.insert(t, i_new[t] + i[j])#将增加该字符后的结果和增加ε后的结果放入i_new中
                            else:
                                i_new.append(i_new[t] + i[j])#将增加该字符后的结果和增加ε后的结果放入i_new中
                    elif i[j] in (VN-W)|VT-{'ε'}:#如果某一字符不在集合W中
                        for t in range(len(i_new)):
                            # 仅将增加该字符后的结果放入i_new中
                            i_new.insert(t, i_new[t] + i[j])
                            del i_new[t+1]
                i_new=set(i_new)
                if i_new!={''}:#如果i_new为空，意味着i='ε',无需把该产生式右部放入新右部，如果i_new不为空，将i_new放入由i产生的新右部
                    i_new.discard('')
                    right_new.update(i_new)
            if right_new:#如果key的新右部集合不为空，意味着key能直接推导出非空产生式
                P_new.update({key:right_new})
        if S not in W:  # 考虑开始符号不在W集合中的情况
            VT=VT-{'ε'}
            return VN,VT,P_new,S
        else:# 考虑开始符号在W集合中的情况
            if S in P_new.keys():
                tem=P_new[S]|{'ε'}
                P_new.update({S+'_1':tem})
            else:
                P_new.update({S + '_1': {'ε'}})
            VN.add(S+'_1')
            return VN,VT,P_new,S+'_1'
    def Eliminate_single_production(self,VN, VT, P, S):
        P_new = P
        for key in P.keys():
            # 用单一产生式右部符号直接推导出的产生式右部替换自身，直到该非终结符不不推导出单一产生式
            while P[key] & VN:#当key直接推导出的右部集合和非终结符存在交集，即key推出单一产生式，循环条件成立
                tem = P[key] & VN#tem即为key推出的单一产生式右部集合
                for i in tem:
                    #用单一产生式右部符号直接推导出的产生式右部替换自身
                    P_new[key].update(P[i])
                    P_new[key].remove(i)
        return VN,VT,P_new,S
    def convert_to_Chomsky(self,VN,VT,P,S):
        #如果有必要的话，增加非递归开始符号
        left_recursion_set=set()
        for i in P[S]:#检查开始符号是否存在左递归
            right_first=re.match('[A-Z]_[0-9]+|[A-Z]|'+'|'.join(VT),i).group()
            if right_first==S:
                left_recursion_set.add(i)
        if left_recursion_set:
            P.update({'S_1':P[S]})
            VN.add('S_1')
            S='S_1'
        P_1={}
        P_tem={}#新产生的非终结符推导出终结符的产生式集合
        #把所有直接推导出单个终结符的产生式放入P_1
        for key in P.keys():
            tem2=P[key]&VT
            if tem2:
                P_1.update({key:tem2})
        #把其余产生式中的终结符替换为新的非终结符
        for key in P.keys():
            tem3 = set()#保存产生式左部key对应的所有处理完成的产生式右部（不包含产生式右部为单个终结符的情况）
            for i in P[key]:
                if i not in VT:#如果产生式右部不为单个终结符（单个终结符的情况已在之前处理）
                    for j in i:#对于产生式右部的每一个字符
                        if j in VT:#如果该字符是终结符
                            if {j} not in P_tem.values():#如果j无法由新产生的非终结符直接推导出，则再产生一个非终结符用以直接推导出j
                                tem4=len(P_tem)+1#新产生的非终结符为B下标数字形式，tem4即为不与之前重复的数字
                                P_tem.update({'B_'+'%d'%tem4:{j}})#将新产生的产生式加入P_tem中
                                i=re.sub(j,'B_'+'%d'%tem4,i)#将该产生式右部的所有字符j替换为新的非终结符
                            else:#如果j可以由新产生的非终结符直接推导出
                                for k in P_tem.keys():#在P_tem中找到直接推出该终结符的非终结符
                                    if P_tem[k]== {j}:
                                        i = re.sub(j, k, i)#用找到的非终结符替换该产生式右部所有字符j
                                        break#已找到直接推出该终结符的非终结符即可退出
                    tem3.add(i)#将处理完的产生式右部加到tem3中
            if tem3:#如果tem3非空，即key能直接推导出除单一终结符外的串
                self.add_production(P_1, key, tem3)#把这些key推导出串的产生式加入P_1
        P_1.update(P_tem)#把所有新产生的非终结符直接推导出单一终结符的产生式加入P_1
        VN_1=set(P_tem.keys())|VN#把所有新产生的非终结符加入非终结符集合
        show.show_all(VN_1, VT, P_1, S, '构造G1后')
        P_c=dict()
        VN_c=VN_1
        subscript = 0  # 新生成非终结符的下标，每次新生成一个非终结符时都会加一
        # """
        # 按照书上算法的构造Gc的方法
        # """
        # for key in P_1.keys():
        #     for i in P_1[key]:
        #         if len(i)==1:#如果产生式右部长度为1（经过上面转换后显然只有单个终结符）
        #             self.add_production(P_c, key, {i})#将该产生式直接加入Pc
        #         else:#如果产生式右部长度大于等于2（经过上面转换后产生式右部为2个或多个非终结符）
        #             tem6=re.findall('[A-Z]_[0-9]+|[A-Z]',i)#找出产生式右部所有的字符
        #             if len(tem6)==2:#如果产生式右部长度等于2
        #                 self.add_production(P_c, key, {i})#将该产生式直接加入Pc
        #             else:#如果产生式右部长度大于2
        #                 t = key
        #                 for j in range(len(tem6)-2):#从左到右扫描产生式右部，若还没扫描的字符长度大于2，则需要新生成非终结符
        #                     subscript = subscript+1
        #                     self.add_production(P_c, t,{tem6[j] + 'T_' + '%d'%subscript})  # 将该产生式直接加入Pc
        #                     VN_c.add('T_' + '%d' % subscript)
        #                     t = 'T_' + '%d'%subscript#上次新生成的非终结符，下次生成新产生式时用到
        #                 self.add_production(P_c, t, {tem6[-2] + tem6[-1]})#若仅剩下两个非终结符还没扫描，不需要新生成非终结符
        """
        改良版的方法（产生的新非终结符更少）
        """
        string_dic = {}
        P_tem = {}#保存所有左部非终结符仅推出一个右部且右部不为终结符的产生式和过程中产生的符合此规则的产生式
        '''
        对于P_1中所有右部长度等于2且左部仅直接推导出该右部的产生式，
        把右部所有符号作为键，左部符号作为值放入字典string_dic中，把这样的产生式添加到P_tem中
        若后续扫描到这样的字符组合，可以直接用左部符号替换
        '''
        for key in P_1.keys():
            if len(P_1[key]) == 1:
                if len(list(P_1[key])[0]) >1:
                    tem6 = re.findall('[A-Z]_[0-9]+|[A-Z]', list(P_1[key])[0])
                    if len(tem6)==2:
                        string_dic.update({''.join(tem6): key})
                        P_tem.update({key: P_1[key]})
        subscript = 0  # 新生成非终结符的下标，每次新生成一个非终结符时都会加一
        for key in P_1.keys():
            for i in P_1[key]:
                if len(i) == 1:  # 如果产生式右部长度为1（经过上面转换后显然只有单个终结符）
                    self.add_production(P_c, key, {i})  # 将该产生式直接加入Pc
                else:  # 如果产生式右部长度大于等于2（经过上面转换后产生式右部为2个或多个非终结符）
                    tem6 = re.findall('[A-Z]_[0-9]+|[A-Z]', i)  # 找出产生式右部所有的字符
                    if len(tem6) == 2:  # 如果产生式右部长度等于2
                        self.add_production(P_c, key, {i})  # 将该产生式直接加入Pc
                    else:  # 如果产生式右部长度大于2
                        if i in string_dic.keys():#如果该产生式右部在string_dic的键中，即已经存在替换该右部的符合规则的两个非终结符
                            self.add_production(P_c,key,P_tem[string_dic[i]])
                        else:
                            t = key
                            for j in range(len(tem6) - 2):
                                if ''.join(tem6[j+1:]) in string_dic.keys():#如果当前字符后面的所有字符连起来的串在string_dic中
                                    self.add_production(P_c, t, {tem6[j] + string_dic[''.join(tem6[j+1:])]})  # 将该产生式直接加入Pc
                                    if not (t == key and len(P_1[key]) > 1):#如果当前扫描的是第一个字符且key对应于多个产生式，则不更新string_dic和P_tem
                                        string_dic.update({''.join(tem6[j:]): t})
                                        self.add_production(P_tem, t, {tem6[j] + string_dic[''.join(tem6[j+1:])]})
                                    break
                                else:
                                    subscript += 1#如果要生成新的非终结符，编号加一
                                    if not (t == key and len(P_1[key]) > 1):#如果当前扫描的是第一个字符且key对应于多个产生式，则不更新string_dic和P_tem
                                        string_dic.update({''.join(tem6[j:]): t})
                                        self.add_production(P_tem, t, {tem6[j] + 'T_' + '%d' % subscript})
                                    self.add_production(P_c, t, {tem6[j] + 'T_' + '%d' % subscript})  # 将该产生式直接加入Pc
                                    VN_c.add('T_' + '%d' % subscript)#更新非终结符集合
                                    t = 'T_' + '%d' % subscript  # 上次新生成的非终结符，作为下次生成新产生式时的左部
                                    if j==len(tem6) - 3:
                                        string_dic.update({''.join(tem6[j+1:]): t})
                                        self.add_production(P_tem, t, {''.join(tem6[j+1:])})
                                        self.add_production(P_c, t, {''.join(tem6[j+1:])})  # 将该产生式直接加入Pc
        # """
        # 再次改良的方法（产生的新非终结符更少）
        # """
        # string_dic = {}
        # P_tem = {}  # 保存所有左部非终结符仅推出一个右部且右部不为终结符的产生式和过程中产生的符合此规则的产生式
        # '''
        # 对于P_1中所有右部长度等于2且左部仅直接推导出该右部的产生式，
        # 把右部所有符号作为键，左部符号作为值放入字典string_dic中，把这样的产生式添加到P_tem中
        # 若后续扫描到这样的字符组合，可以直接用左部符号替换
        # '''
        # for key in P_1.keys():
        #     if len(P_1[key]) == 1:
        #         if len(list(P_1[key])[0]) > 1:
        #             tem6 = re.findall('[A-Z]_[0-9]+|[A-Z]', list(P_1[key])[0])
        #             if len(tem6) == 2:
        #                 string_dic.update({' '.join(tem6)+' ': key})
        #                 P_tem.update({key: P_1[key]})
        # subscript = 0  # 新生成非终结符的下标，每次新生成一个非终结符时都会加一
        # for key in P_1.keys():
        #     for i in P_1[key]:
        #         if len(i) == 1:  # 如果产生式右部长度为1（经过上面转换后显然只有单个终结符）
        #             self.add_production(P_c, key, {i})  # 将该产生式直接加入Pc
        #         else:  # 如果产生式右部长度大于等于2（经过上面转换后产生式右部为2个或多个非终结符）
        #             tem6 = re.findall('[A-Z]_[0-9]+|[A-Z]', i)  # 找出产生式右部所有的字符
        #             if len(tem6) == 2:  # 如果产生式右部长度等于2
        #                 self.add_production(P_c, key, {i})  # 将该产生式直接加入Pc
        #             else:  # 如果产生式右部长度大于2
        #                 if ' '.join(tem6)+' ' in string_dic.keys():  # 如果该产生式右部在string_dic的键中（这个方法中string_dic中的字符用空格做间隔），即已经存在替换该右部的符合规则的两个非终结符
        #                     self.add_production(P_c, key, P_tem[string_dic[i]])
        #                 else:
        #                     if not string_dic:#如果string_dic为空，则直接按照原始方法生成新的非终结符
        #                         t = key
        #                         for j in range(len(tem6) - 2):  # 从左到右扫描产生式右部，若还没扫描的字符长度大于2，则需要新生成非终结符
        #                             subscript = subscript + 1
        #                             self.add_production(P_c, t, {tem6[j] + 'T_' + '%d' % subscript})  # 将该产生式直接加入Pc
        #                             if not (t == key and len(P_1[key]) > 1):  # 如果当前扫描的是第一个字符且key对应于多个产生式，则不更新string_dic和P_tem
        #                                 string_dic.update({' '.join(tem6[j:])+' ': t})
        #                                 self.add_production(P_tem, t, {tem6[j] + 'T_' + '%d' % subscript})
        #                             VN_c.add('T_' + '%d' % subscript)
        #                             t = 'T_' + '%d' % subscript  # 上次新生成的非终结符，下次生成新产生式时用到
        #                             if j == len(tem6) - 3:
        #                                 string_dic.update({' '.join(tem6[j + 1:])+' ': t})
        #                                 self.add_production(P_tem, t, {''.join(tem6[j + 1:])})
        #                                 self.add_production(P_c, t, {''.join(tem6[j + 1:])})  # 将该产生式直接加入Pc
        #                     else:
        #                         tem20=' '.join(tem6)+' '#string_dic中字符为A T_1 形式，即每一个字符后面跟一个空格，否则在匹配时会遇到匹配AT的情况
        #                         tem9=re.search('|'.join(sorted(list(string_dic.keys()), key=lambda i: len(i), reverse=True)),tem20)#在string_dic中寻找能匹配i中字符串的最长字符串
        #                         while tem9:#如果能找到，则进行替换，再在替换后的字符串中反复寻找，替换，直到找不到匹配的字符串
        #                             tem20=re.sub(tem9.group(),string_dic[tem9.group()],tem20)
        #                             tem9 = re.search('|'.join(sorted(list(string_dic.keys()), key=lambda i: len(i), reverse=True)),tem20)
        #                         tem6=re.findall('[A-Z]_[0-9]+|[A-Z]', tem20)
        #                         if len(tem6)==1:#如果多次替换后剩下的字符串长度为1（为避免生成单一产生式，用P_tem中该字符对应的产生式右部替换）
        #                             self.add_production(P_c, key, P_tem[re.sub(' ','',tem20)])
        #                             if not len(P_1[key]) > 1:  # 如果、key对应于多个产生式，则不更新string_dic和P_tem
        #                                 iii=re.findall('[A-Z]_[0-9]+|[A-Z]', i)
        #                                 string_dic.update({' '.join(iii)+' ': key})
        #                                 self.add_production(P_tem, key, {i})
        #                         elif len(tem6)==2:#如果多次替换后剩下的字符串长度为2
        #                             self.add_production(P_c, key, {re.sub(' ','',tem20)})
        #                             if not len(P_1[key]) > 1:  # 如果、key对应于多个产生式，则不更新string_dic和P_tem
        #                                 iii = re.findall('[A-Z]_[0-9]+|[A-Z]', i)
        #                                 string_dic.update({' '.join(iii)+' ': key})
        #                                 self.add_production(P_tem, key, {i})
        #                         else:#如果多次替换后剩下的字符串长度大于2，则像之前那样添加新的非终结符进行替换
        #                             t=key
        #                             for j in range(len(tem6) - 2):  # 从左到右扫描产生式右部，若还没扫描的字符长度大于2，则需要新生成非终结符
        #                                 subscript = subscript+1
        #                                 self.add_production(P_c, t,{tem6[j] + 'T_' + '%d'%subscript})  # 将该产生式直接加入Pc
        #                                 if not (t == key and len(P_1[key]) > 1):  # 如果当前扫描的是第一个字符且key对应于多个产生式，则不更新string_dic和P_tem
        #                                     string_dic.update({' '.join(tem6[j:])+' ': t})
        #                                     self.add_production(P_tem, t, {tem6[j] + 'T_' + '%d' % subscript})
        #                                 VN_c.add('T_' + '%d' % subscript)
        #                                 t = 'T_' + '%d'%subscript#上次新生成的非终结符，下次生成新产生式时用到
        #                                 if j == len(tem6) - 3:
        #                                     string_dic.update({' '.join(tem6[j + 1:])+' ': t})
        #                                     self.add_production(P_tem, t, {''.join(tem6[j + 1:])})
        #                                     self.add_production(P_c, t, {''.join(tem6[j + 1:])})  # 将该产生式直接加入Pc
        return VN_c, VT, P_c, S
    '''
    《形式语言与自动机》P47推论3.1
    '''
    def algorithm_3_1(self,VN,VT,P,S):
        #对非终结符进行排序，首先对开始符号赋予序号1，然后对开始符号的非终结first集合分别赋予序号
        prio=[S]
        for i in range(len(prio)):
            for j in P[list(prio)[i]]:
                tem=re.match('[A-Z]_[0-9]+|[A-Z]',j)
                if tem:
                    if tem.group() not in prio:
                        prio.append(tem.group())
        for i in VN:#对其他非终结符随机赋予序号
            if i not in prio:
                prio.append(i)
        count=0#如果在过程在产生左递归，需要增加新非终结符，用count来标记新非终结符的序号
        P_new = copy.deepcopy(P)#新的产生式合集，因为循环过程中会对字典进行增删，所有不能对P直接改动
        tem = set()
        for i in prio:#对于优先级序列中的每一个非终结符
            tem2 = (VN-tem)|VT#序号大于i的终结符和非终结符集合的并集
            for j in P[i]:
                tem7=re.match('[A-Z]_[0-9]+|[A-Z]|'+'|'.join(VT),j)#找到j的首字母
                tem8 = set()
                if tem7.group() not in tem2:
                    tem3 = [j]#对于产生式i->j,把j的首字母用其对应的产生式右部替换并加到tem3中，直到tem3中所有字符串的首位都在tem2中
                    start=0
                    after=1
                    tem8.add(j)#保存改变前的产生式右部，最后再删去
                    while start!=after:#当tem3不再变化时循环终止
                        start=copy.deepcopy(tem3)#本次循环开始时tem3的值
                        tem4 = []#用来保存替换后的字符串
                        tem5=[]#用来保存替换前的字符串
                        for k in tem3:
                            tem6 = re.findall('[A-Z]_[0-9]+|[A-Z]|'+'|'.join(VT), k)#找到k的所有字符
                            if tem6[0] not in tem2:#如果k的首字符不在tem2中，即序号小于i
                                for t in P_new[tem6[0]]:#所有序号小于i的非终结符直接推导的产生式都已在P_new中
                                    tem4.append(t + ''.join(tem6[1:]))#用t替换k的首字符并加到tem4中
                                tem5.append(k)#把未替换的原字符串存到tem5中
                        for t in tem5:
                            tem3.remove(t)#删除替换前的字符串
                        tem3.extend(tem4)#把替换后的字符串加到tem3中
                        after=tem3#本次循环结束时tem3的值
                    self.add_production(P_new, i, set(tem3))
                P_new[i]=P_new[i]-tem8
            tem.add(i)
            #如果本次处理后产生直接左递归
            left_recursion_set = set()
            ttt = set()
            for j in P_new[i]:
                right_first = re.match('[A-Z]_[0-9]+|[A-Z]|' + '|'.join(VT), j).group()
                if right_first == i:
                    left_recursion_set.add(j)
                    ttt.add(re.sub(right_first, '', j, count=1))
            if left_recursion_set:
                count+=1
                new_N = 'Z_' + '%d' % count
                P_tem = copy.deepcopy(P_new)
                del P_new[i]
                P_new.update({new_N: set([j + new_N for j in ttt]) | ttt})
                P_new.update({i: set([j + new_N for j in P_tem[i] - left_recursion_set]) | P_tem[i] - left_recursion_set})
                VN.add(new_N)
                tem.add(new_N)
        return VN,VT,P_new,S,prio
    def convert_to_Start_with_Terminator(self,VN,VT,P,S):
        for key in P:
            tem2=set()
            tem1=set()
            for i in P[key]:
                first_character = re.match('[A-Z]_[0-9]+|[A-Z]|' + '|'.join(VT), i).group()  # 找到i的首字符
                if first_character in VT:#如果首字符是终结符
                    pass#无需操作
                else:#如果首字符不是终结符
                    tem3 = [i]  # 对于产生式key->i,把i的首字符用其对应的产生式右部替换并加到tem3中，删去原字符串，对tem3中字符串重复以上操作，直到tem3中所有字符串的首位都在VT中
                    start = 0#本次循环开始时tem3的值
                    after = 1#本次循环结束后tem3的值
                    while(start!=after):  # 当tem3不再变化时循环终止
                        start = copy.deepcopy(tem3)#循环开始时tem3的值
                        tem4 = []#储存所有替换后的值，最后要增加
                        tem5 = []#储存所有替换前的值，最后要删去
                        for k in tem3:
                            tem6 = re.findall('[A-Z]_[0-9]+|[A-Z]|'+'|'.join(VT), k)  # 找到k的首字符
                            if tem6[0] not in VT:  # 如果k的首字符不是终结符
                                for t in P[tem6[0]]:#用所有左部为k的首字符的产生式替换
                                    tem4.append(t + ''.join(tem6[1:]))
                                tem5.append(k)
                        for t in tem5:
                            tem3.remove(t)
                        tem3.extend(tem4)
                        after = tem3#循环结束时tem3的值
                    tem2.update(set(tem3))
                    tem1.update({i})
            P[key].update(tem2)#增加替换后的字符串
            P[key]=P[key]-tem1#删去所有非终结符开头的字符串
        return VN,VT,P,S
    def Eliminate_direct_left_recursion(self,VN,VT,P,S):
        P_tem = copy.deepcopy(P)#复制产生式字典作为循环条件，防止循环过程中字典发生变化
        count = 0#生成的新非终结符的下标
        for key in P_tem.keys():#对于每一个产生式左部
            tem1 = set()#保存key的所有直接左递归产生式右部
            tem2 = set()#保存key的所有直接左递归产生式右部删去首字符后的字符串
            for i in P_tem[key]:#对于产生式左部的每一个右部
                tem = re.match('[A-Z]_[0-9]+|[A-Z]|' + '|'.join(VT), i).group()#找到i的首字符
                if tem == key:#如果右部首字符等于左部（意味着直接左递归）
                    tem1.add(i)#把该右部加到tem1中
                    tem2.add(re.sub(tem, '', i, count=1))#把删去首字符的右部加到tem2中（因为不存在无用产生式，所有删去首字符后一定还有字符）
            if tem1:#如果该左部存在直接左递归产生式
                count += 1#下标计数加一
                # 删去P中所有key对于的产生式，后续把删去左递归后的产生式重新加入P
                del P[key]
                new_N='Z_' +'%d' % count
                P.update({new_N: set([j + new_N for j in tem2]) | tem2})
                P.update({key: set([j + new_N for j in P_tem[key] - tem1])|P_tem[key] - tem1})
                VN.add( new_N)
        return VN,VT,P,S
    def add_production(self,P,left,right):
        if left in P.keys():
            P[left].update(right)
        else:
            P.update({left: right})


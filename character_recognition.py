import copy
import re
def build_transfer_function( VN, VT, P, S):
    transfer_function = {('q_0', 'ε', 'z'): [('q_1', S + 'z')]}
    for key in P.keys():
        for i in P[key]:
            if len(i) > 1:
                if ('q_1', i[0], key) not in transfer_function:
                    transfer_function.update({('q_1', i[0], key): [('q_1', i[1:])]})
                else:
                    transfer_function[('q_1', i[0], key)].extend([('q_1', i[1:])])
            else:
                if ('q_1', i[0], key) not in transfer_function:
                    transfer_function.update({('q_1', i, key): [('q_1', 'ε')]})
                else:
                    transfer_function[('q_1', i, key)].extend([('q_1', 'ε')])
    transfer_function.update({('q_1', 'ε', 'z'): [('q_f', 'z')]})
    return transfer_function, 'q_0', 'q_f'
class character_recognition():
    def __init__(self,transfer_function,q_0,q_f):
        self.transfer_function = transfer_function
        self.q_0=q_0
        self.q_f=q_f
    def rec(self,str):
        self.str=str
        tape=['ε']+list(str)+['ε']*3
        state=self.q_0#初始化状态（即将初始状态赋给state变量）
        head=0#初始化读头位置
        character_sta=['z']#初始化字符栈（开始时栈中只有一个字符z）
        print('初始状态:',state, tape[head], character_sta)  # 输出开始时的状态、读头对应字符和字符栈
        print('===============================================================')
        dequeue=[]#用一个双端队列保存每次遇到分支时的选择
        while(state!=self.q_f and state!=-1):#匹配成功时状态变为终态，匹配不成功时状态变为-1，这两种情况都能使循环结束
            #print(head)
            if (state,tape[head],character_sta[-1]) in self.transfer_function.keys():#如果在状态转移函数字典中能找到当前状态对应的状态转移函数
                tem = self.transfer_function[(state,tape[head],character_sta[-1])]#tem为当前状态、输入字符、栈顶元素对应的转移函数所能转向的所有情况
                if len(tem)==1:#如果当前状态、输入字符、栈顶元素对应的转移函数只有一个右部
                    pass
                else:  # 如果存在分支
                    dequeue.append(
                        [state, head, copy.deepcopy(character_sta), 1])  # 将转移前的状态、读头位置、字符栈和下一条转移函数在分支中的序号保存到双端队列
                '''
                使用分支中第一个转移函数转移状态
                '''
                print('直接使用字典中的转移函数：|所有的可能转移：', 'δ('+state+','+tape[head]+','+character_sta[-1]+') =',tem)
                print('                         |使用的状态转移函数：','δ('+state+','+tape[head]+','+character_sta[-1]+') =',tem[0] )
                state,tem2=tem[0]#将转移后的状态值赋给state，把要放入栈中的字符串赋给tem2
                head += 1#读头向后移
                tem2 = re.findall('[A-Z]_[0-9]*|[A-Z]|ε|z', tem2)#找到tem2中所有字符
                del (character_sta[-1])#栈顶元素出栈
                for i in range(len(tem2)):#tem2中字符不为ε的情况下按照从右到左的顺序依次入栈
                    if tem2[-i - 1]!='ε':
                        character_sta.append(tem2[-i - 1])
                print('                         |转移后状态，转移后读头对应符号，字符栈：',state, tape[head], character_sta)
                print('                         |转移后的双端队列状态：',dequeue)
                print('===============================================================')
            else:#如果在状态转移函数字典中找不到当前状态对应的状态转移函数
                if not dequeue:#首先检查双端队列的状态，如果双端队列为空，意味着状态未转移到终态的情况下找不到下一条转移函数
                    state=-1#把状态置为-1，意味着匹配失败
                else:#如果双端队列不为空，则回溯到上一次出现分支的状态，使用分支中下一条转移函数进行状态转移
                    #print(3,dequeue)
                    tem=dequeue[-1]#把双端队列中最后一个值（即上一次遇到分支时的转移前状态、读头位置、字符栈、和本次转移应使用的状态函数在分支中的序号）赋给tem
                    del dequeue[-1]#删除上一次保存的断点
                    print('使用双端队列中的转移函数：|剩下的所有的可能转移：', 'δ('+tem[0]+','+tape[tem[1]]+','+tem[2][-1]+') =',self.transfer_function[(tem[0],tape[tem[1]],tem[2][-1])][tem[3]:])


                    print('                         |使用的状态转移函数：', 'δ('+ tem[0]+','+tape[tem[1]]+','+tem[2][-1]+ ') =', self.transfer_function[(tem[0],tape[tem[1]],tem[2][-1])][tem[3]])


                    #print('2',dequeue)
                    if tem[3]==len(self.transfer_function[(tem[0],tape[tem[1]],tem[2][-1])])-1:#如果这次使用了分支中最后一个转移函数
                        pass
                    else:#如果这次使用的不是分支中最后一个转移函数
                        dequeue.append([tem[0],tem[1],tem[2],tem[3]+1])#把分支中下一个转移函数的序号以及现场信息放入双端队列
                    character_sta=copy.deepcopy(tem[2])#把状态栈还原到上次遇到分支时转移前的状态
                    state, tem2=self.transfer_function[(tem[0],tape[tem[1]],tem[2][-1])][tem[3]]#转移状态
                    head =tem[1]+1#把读头位置移动到上次遇到分支前的读头位置的下一个位置
                    tem2 = re.findall('[A-Z]_[0-9]*|[A-Z]|ε|z', tem2)#找到tem2中所有字符
                    del character_sta[-1]#栈顶元素出栈
                    for i in range(len(tem2)):#tem2中字符不为ε的情况下按照从右到左的顺序依次入栈
                        if tem2[-i - 1] != 'ε':
                            character_sta.append(tem2[-i - 1])
                    print('                         |转移后状态，转移后读头对应符号，字符栈', state, tape[head], character_sta)
                    print('                         |转移后的双端队列状态：', dequeue)
                    print('===============================================================')
        '''
        保存及输出匹配的字符及使用的转移函数
        '''
        state_saved=[]#用以保存状态,方便后续输出
        if state==-1:
            state_saved= -1
        else:#如果匹配成功，从初始状态开始向后转移，如果遇到分支，检查遇到分支时的状态在不在双端队列首部，
            # 如果在，则使用双端队列首部保存的转移函数序号-1对应的转移函数
            # 如果不在，则使用分支中最后一条转移函数
            state = self.q_0
            head = 0
            character_sta = ['z']
            state_saved.append((state,tape[head],copy.deepcopy(character_sta)))#保存开始时的状态、读头对应字符和字符栈
            while(state!=self.q_f):
                tem = self.transfer_function[(state, tape[head], character_sta[-1])]#tem为当前状态、输入字符、栈顶元素对应的转移函数所能转向的所有情况
                if len(tem)==1:#如果没有遇到分支
                    '''
                    转移状态
                    '''
                    state, tem2 = tem[0]
                    head += 1
                    tem2 = re.findall('[A-Z]_[0-9]*|[A-Z]|ε|z', tem2)
                    #print('tem2',tem2)
                    del (character_sta[-1])
                    for i in range(len(tem2)):
                        if tem2[-i - 1] != 'ε':
                            character_sta.append(tem2[-i - 1])
                    state_saved.append((state,tape[head],copy.deepcopy(character_sta)))#保存转移后的状态
                else:#如果遇到分支
                    if dequeue and(state,head,character_sta)==(dequeue[0][0],dequeue[0][1],dequeue[0][2]):#如果双端队列给出了遇到分支时的转移函数:
                        tem = dequeue[0]#把遇到分支时的解决方案赋给tem
                        del dequeue[0]  # 删除使用过的分支判断材料
                        '''
                        转移状态
                        '''
                        state, tem2 = self.transfer_function[(state, tape[head], character_sta[-1])][tem[3]-1]#使用双端队列首部保存的转移函数序号-1对应的转移函数
                        head += 1
                        tem2 = re.findall('[A-Z]_[0-9]*|[A-Z]|ε|z', tem2)
                        del character_sta[-1]
                        for i in range(len(tem2)):
                            if tem2[-i - 1] != 'ε':
                                character_sta.append(tem2[-i - 1])
                        # 保存转移后的状态
                        state_saved.append((state,tape[head],copy.deepcopy(character_sta)))
                    else:#如果双端队列没有给出遇到分支时的转移函数，就用最后一个分支
                        '''
                        转移状态
                        '''
                        state, tem2 = self.transfer_function[(state, tape[head], character_sta[-1])][- 1]
                        head += 1
                        tem2 = re.findall('[A-Z]_[0-9]*|[A-Z]|ε|z', tem2)
                        del character_sta[-1]
                        for i in range(len(tem2)):
                            if tem2[-i - 1] != 'ε':
                                character_sta.append(tem2[-i - 1])
                        #保存转移后状态
                        state_saved.append((state,tape[head],copy.deepcopy(character_sta)))
        self.show_instantaneous_description_transition(state_saved)#瞬时描述过程迁移输出
        self.show_State_transition(state_saved)#可视化展示输出
    def show_instantaneous_description_transition(self,state_saved):
        if state_saved==-1:
            print('\033[5;36m识别失败！')
        else:
            print('\033[5;36m瞬时描述：')
            for i in range(len(state_saved)):
                if i<len(self.str):
                    print('('+state_saved[i][0]+','+self.str[i:]+','+''.join([state_saved[i][2][-1-j] for j in range(len(state_saved[i][2]))])+') ├ ',end='')
                else:
                    print('(' + state_saved[i][0] + ',' + 'ε' + ',' + ''.join(
                        [state_saved[i][2][-1 - j] for j in range(len(state_saved[i][2]))]) + ') ├ ',end='')
            print('\b\b')
            print('识别成功！')
    def show_State_transition(self,state_saved):
        if state_saved==-1:
            print('\033[5;33m识别失败！')
        else:
            print('\033[5;33m迁移过程可视化描述：')
            for i in range(len(state_saved)):
                print('┌————' + '┬————' * 15 + '┐')
                print('| ' + ' ' + '  ', end='')
                for t in range(len(self.str)):
                    print('| ' + self.str[t] + '  ', end='')
                for t in range(15 - len(self.str)):
                    print('| ' + ' ' + '  ', end='')
                print('|', end='')
                print('\n' + '└————' + '┴————' * 15 + '┘')
                print('     ' * i + '   ↑')
                print('     ' * i +'┌—————┐' + '         ┌—————┐')
                if len(state_saved[i][2][-1])==3:
                    print('     ' * i + '| ' + state_saved[i][0] + ' |' + '————————→│ ' + state_saved[i][2][-1] + ' │')
                else:
                    print('     ' * i +'| '+state_saved[i][0]+' |' + '————————→│　'+state_saved[i][2][-1]+'　│')
                print('     ' * i +'└—————┘' + '         ├—————┤')
                for j in range(len(state_saved[i][2])-1):
                    if len(state_saved[i][2][-2-j]) == 3:
                        print('     ' * i +'     　　　    　│ '+state_saved[i][2][-2-j]+' │')
                    else:
                        print('     ' * i +'      　　　   　│　'+state_saved[i][2][-2-j]+'　│')
                    print('     ' * i +'     　　 　　　 ├—————┤')
            print('识别成功！')

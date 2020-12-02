def show_transfer_function(transfer_function,S):
    result='δ('+','.join(('q_0','ε','z'))+')'+' = {'+','.join(('q_1',S+'z'))+'}\n'
    for key in transfer_function.keys()-{('q_0','ε','z')}-{('q_1','ε','z')}:
        tem='δ('+','.join(key)+')'
        tem2=[]
        for i in transfer_function[key]:
            tem2.append('('+','.join(i)+')')
        tem2='{'+','.join(tem2)+'}'
        result=result+'          '+tem+' = '+tem2+'\n'
    result = result+'          '+'δ(' + ','.join(('q_1', 'ε', 'z')) + ')' + ' = {' + ','.join(('q_f', 'z')) + '}\n'
    print('\033[1;32m转移函数:',result)
def show_production(production,S):
    result='|'+S+' -> '+'|'.join(production[S])+'\n'
    for key in production.keys()-{S}:
        tem=key+' -> '
        tem2='|'.join(production[key])
        result=result+'   |'+tem+tem2+'\n'
    print('\033[1;35mP:',result)
def show_all(VN,VT,P,S,string):
    boundary=int((66-len(string))/2)*'='
    print('\033[1;31m'+boundary+string+boundary+'\n')
    print('\033[0;33m开始符号:',S, '\n')
    print('VT:', VT, '\n')
    print('VN:', VN, '\n')
    show_production(P, S)
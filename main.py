import CFG_to_Greibach as ctg
import character_recognition as cr
import extract_init_grammer as eig
import show
if __name__ == '__main__':
    ext=eig.extract_init_grammer(19,24)
    VN, VT, P, S = eig.init_grammer(ext)
    show.show_all(VN, VT, P, S, '开始')

    a=ctg.CFG_to_Greibach()
    VN, VT, P, S = a.deleting_superfluous_symbol_and_production(VN, VT, P, S)

    show.show_all(VN, VT, P, S, '消除无用产生式与无用符号后')

    VN, VT, P, S = a.Eliminate_empty_production(VN, VT, P, S)
    VN, VT, P, S = a.deleting_superfluous_symbol_and_production(VN, VT, P, S)
    show.show_all(VN, VT, P, S, '消除空产生式后')

    VN, VT, P, S = a.Eliminate_single_production(VN, VT, P, S)
    VN, VT, P, S = a.deleting_superfluous_symbol_and_production(VN, VT, P, S)
    show.show_all(VN, VT, P, S, '消除单一产生式后')

    # VN,VT,P,S=a.Eliminate_direct_left_recursion(VN,VT,P,S)
    # show_all(VN,VT,P,S,'消除直接左递归后')

    VN, VT, P, S = a.convert_to_Chomsky(VN, VT, P, S)
    show.show_all(VN, VT, P, S, '转换成乔姆斯基范式后')

    VN, VT, P, S, prio = a.algorithm_3_1(VN, VT, P, S)
    show.show_all(VN, VT, P, S, '使用《形式语言与自动机》P47推论3.1后')
    print('非终结符序号:', prio)

    VN, VT, P, S = a.convert_to_Start_with_Terminator(VN, VT, P, S)
    VN, VT, P, S = a.deleting_superfluous_symbol_and_production(VN, VT, P, S)
    show.show_all(VN, VT, P, S, '格雷巴赫范式')

    transfer_function, q_0, q_f = cr.build_transfer_function(VN, VT, P, S)
    print('\033[1;31m===============================转移函数如下===============================', '\n')
    print('\033[1;33m开始状态:', q_0, '\n')
    print('终止状态:', q_f, '\n')
    show.show_transfer_function(transfer_function, S)

    print('\033[5;34m---------------------------------------------------------------')
    b = cr.character_recognition(transfer_function, q_0, q_f)
    b.rec('aa')
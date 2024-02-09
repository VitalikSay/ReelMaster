#import Reelset
#import Reel
from Source.Reelset import Reelset
from Source.Reel import Reel
import numpy as np

class Replace_Symbols:
    def __init__(self, reelset: Reelset):
        self.reelset = reelset

    # table_of_replacement = {}
    #                            #symbol    # weight
    # table_of_replacement[51] = [[12, 11], [0.5, 0.5]]  # Double
    # table_of_replacement[52] = [[12, 12], [0.5, 0.5]]  # Double
    # table_of_replacement[53] = [[11, 13], [0.5, 0.5]]  # Double
    # table_of_replacement[53] = [[13, 12], [0.5, 0.5]]  # Double
    # table_of_replacement[54] = [[14, 12], [0.5, 0.5]]  # Double
    # table_of_replacement[55] = [[15, 11], [0.5, 0.5]]  # Double
    # table_of_replacement[56] = [[16, 11], [0.5, 0.5]]  # Double
    # table_of_replacement[57] = [[11, 12, 13], [0.3, 0.35, 0.35]]  # Triple
    # table_of_replacement[58] = [[12, 13, 14, 15], [0.2, 0.3, 0.25, 0.25]]  # Triple

    def insert_right_symbols(self):
        for reelset in self.reelset.reels:
            for symbol_ind in range(reelset.symbols):
                if reelset.symbols[symbol_ind] in self.table_of_replacement:
                    reelset.symbols[symbol_ind] = np.random.choice(self.table_of_replacement[reelset.symbols[symbol_ind]],
                                                                   p=self.table_of_replacement[reelset.symbols[symbol_ind]])


class CF_Reel(Reel):
    table_of_replacement = {}
    # symbol    # weight
    # first common symbol - 11 LtL
    table_of_replacement[50] = [12, 11]  # Double
    table_of_replacement[51] = [11, 13]  # Double
    table_of_replacement[52] = [13, 12]  # Double
    table_of_replacement[53] = [14, 12]  # Double
    table_of_replacement[54] = [11, 15]  # Double
    table_of_replacement[55] = [13, 14]  # Double
    table_of_replacement[56] = [16, 11]  # Double
    table_of_replacement[57] = [11, 12, 11]  # Triple
    table_of_replacement[58] = [13, 11, 12]  # Triple

    # first common symbol - 14 SLD
    # table_of_replacement[50] = [15, 14]  # Double
    # table_of_replacement[51] = [14, 16]  # Double
    # table_of_replacement[52] = [16, 15]  # Double
    # table_of_replacement[53] = [17, 15]  # Double
    # table_of_replacement[54] = [14, 18]  # Double
    # table_of_replacement[55] = [16, 17]  # Double
    # table_of_replacement[56] = [19, 14]  # Double
    # table_of_replacement[57] = [14, 15, 14]  # Triple
    # table_of_replacement[58] = [16, 14, 15]  # Triple


    def _UnpackSymbolStacks(self):
        for stack in self.symbol_in_stacks:
            if stack[1] in self.table_of_replacement:
                self.symbols += self.table_of_replacement[stack[1]]
            else:
                self.symbols += [stack[1] for _ in range(stack[0])]



class CF_Reelset(Reelset):
    def MakeSymbols(self):
        for i in range(self.data.number_of_reels):
            current_reel = CF_Reel(i)
            if self.data.working_mode != 2:
                current_reel.MakeReel(self.data.common_symbols[i],
                                      self.data.special_symbols[i],
                                      self.data.dist_between_sp_symbols[i],
                                      self.data.window_height)
            else:
                current_reel.SetSymbols(self.data.read_symbol_weights[i][0])
                current_reel.ln = len(current_reel.symbols)
            self.reels.append(current_reel)



def Insert_CF_Symbols_instead_of_11(reelset: Reelset):
    # first symbol - 11, LtL
    symbls = [11, 12, 13, 14, 15, 16, 17, 18, 19, 30, 31, 32]
    weight = [3,   3,  3,  5, 10, 14, 20, 21, 13,  4,  3,  1]

    # first symbol - 14, SLD
    #symbls = [14, 15, 16, 17, 18, 19, 20, 21, 22, 33, 34, 35]
    #weight = [3, 3, 3, 5, 10, 14, 20, 21, 13, 4, 3, 1]
    symb_lst = []
    for i in range(len(symbls)):
        for c in range(weight[i]):
            symb_lst.append(symbls[i])

    symb_positions_by_reels = []
    for reel in reelset.reels:
        symb_pos = []
        for i in range(len(reel.symbols)):
            if (reel.symbols[i] == 11) and (
                    reel.symbols[i - 1] == 11 or reel.symbols[(i + 1) % len(reel.symbols)] == 11):
                symb_pos.append(i)
        symb_positions_by_reels.append(symb_pos)

    for i, reel_position in enumerate(symb_positions_by_reels):
        for position in reel_position:
            rand_symb = np.random.choice(symb_lst)
            reelset.reels[i].symbols[position] = rand_symb

    for i in range(len(reelset.reels)):
        if len(symb_positions_by_reels[i]) == 0:
            continue
        reel = reelset.reels[i]
        for symbl in symbls:
            if symbl not in reel.symbols:
                rand_index = np.random.choice(symb_positions_by_reels[i])
                while reel.symbols.count(reel.symbols[rand_index]) <= 1:
                    rand_index = np.random.choice(symb_positions_by_reels[i])
                reel.symbols[rand_index] = symbl
                del symb_positions_by_reels[i][symb_positions_by_reels[i].index(rand_index)]



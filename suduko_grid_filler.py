import numpy as np
import sys

main_grid = np.zeros((9,9), dtype='i')

class Suduko_gird_value_generator:
    
    def __init__(self, main_grid):
        self.A1 = np.zeros((3, 3), dtype='i')
        self.A2 = np.zeros((3, 3), dtype='i')
        self.A3 = np.zeros((3, 3), dtype='i')
        self.A4 = np.zeros((3, 3), dtype='i')
        self.A5 = np.zeros((3, 3), dtype='i')
        self.A6 = np.zeros((3, 3), dtype='i')
        self.A7 = np.zeros((3, 3), dtype='i')
        self.A8 = np.zeros((3, 3), dtype='i')
        self.A9 = np.zeros((3, 3), dtype='i')
        
        self.filler = np.arange(1,10)
        self.__sub_grid_value_generator()
        
        
        
        main_grid[:3, :3], main_grid[:3, 3:6], main_grid[:3, 6:9]    = self.A1 , self.A2, self.A3
        main_grid[3:6, :3], main_grid[3:6, 3:6], main_grid[3:6, 6:9] = self.A4 , self.A5, self.A6
        main_grid[6:9, :3], main_grid[6:9, 3:6], main_grid[6:9, 6:9] = self.A7 , self.A8, self.A9
                
        
    
    def __sub_grid_value_generator(self):
        self.A5 = self.__mid_sub_grid_filler(self.A5)
        self.A2, self.A8 = self.__side_neighbour_grid_filler(self.A5, self.A2, self.A8)
        self.A4, self.A6 = self.__side_neighbour_grid_filler(self.A5, self.A4, self.A6, horizontal=True)
    
    
    def __mid_sub_grid_filler(self, mid):
        
        np.random.shuffle(self.filler)    
        mid = self.filler.reshape((3, 3)).copy()
        return mid
        
    
    def __side_neighbour_grid_filler(self, mid, side , opo_side, horizontal=False):
        
        #rotate if grid horizontal
        if horizontal:
            mid = np.rot90(mid)
            side = np.rot90(side)
            opo_side = np.rot90(opo_side)
            

        def __backtrack(mid, side, opo_side, prev_t):
            
            side = np.zeros((3, 3), dtype='i')
            opo_side = np.zeros((3, 3), dtype='i')
            
            t = mid[:, 1:].copy()
            if prev_t is not None:
                while prev_t != t:
                    t = np.random.permutation(t.flatten()).reshape(3, 2)
            else:
                t = np.random.permutation(t.flatten()).reshape(3, 2)
            
            side[:, 0] = t[:, 0].copy()
            opo_side[:, 0] = t[:, 1].copy()
            
            for x in range(1,3):
                
                f = [i for i in range(1,10) if i not in mid[:, x]]
                count = 0
                while True:
                    np.random.shuffle(f)
                    
                    e_sub_grid = 0
                    if not any(ele in side for ele in f[:3]):
                        if not any(ele in opo_side for ele in f[3:]):
                            side[:, x] = f[:3].copy()
                            opo_side[:, x] = f[3:].copy()
                            break
                        else:
                            e_sub_grid = 1
                            
                    
                    count += 1
                    if count > 1000:
                        
                        print("side_neighbour : Invalid suduko\ncol_no :",x ,', direction-horizontal :',horizontal)
                        print("pos :",e_sub_grid)
                        
                        
                        
                        return side, opo_side, t, False
                        
                    continue
                
            return side, opo_side,None, True
                
        fill = False
        o_count = 0
        prev_t = None
        while not fill:
            side, opo_side, prev_t, fill = __backtrack(mid, side, opo_side, prev_t)
            if o_count > 1000:
                print("still invalid")
                sys.exit()
            
         #rotate back to original form   
        if horizontal:
            mid = np.rot90(mid, 3)
            side = np.rot90(side, 3)
            opo_side = np.rot90(opo_side, 3)
                    
        return side, opo_side
        
    
a = Suduko_gird_value_generator(main_grid)

for i in range(9):
    for j in range(9):
        if main_grid[i, j] != 0:
            print(main_grid[i, j],end = ' ')
        else:
            print('-',end=' ')
    print()

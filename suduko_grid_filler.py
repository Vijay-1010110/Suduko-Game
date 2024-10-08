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
        self.A1, self.A7 = self.__fill_subgrid_corner(self.A1, self.A2, self.A3, self.A4, self.A7, self.A8, self.A9)
        self.A3, self.A9 = self.__fill_subgrid_corner(self.A3, self.A2, self.A1, self.A4, self.A9, self.A8, self.A7)
    
    #function to fill middle subgrid
    def __mid_sub_grid_filler(self, mid):
        
        np.random.shuffle(self.filler)    
        mid = self.filler.reshape((3, 3)).copy()
        return mid
        
    #function to fill direct neighbour subgrid
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
        
    #function to fill corner grid
    #focus sub gird : m, n
    #corelated grid : start counting from left to right and top to bottom
    def __fill_subgrid_corner(self, m, mh1, mh2, mnv, n, nh1, nh2):
        
        def __backtrack(m, mh1, mh2, mnv, n, nh1, nh2):
            
            
            def __nested_backtrack(m, mh1, mh2, n, nh1, nh2, t, i):
                
                def __fill(x,y,z,t,i,j,s,e):
                    inner_count = 0
                    while inner_count < 50:
                        if  t[s:e][j] not in y[j, :] and t[s:e][j] not in z[j, :]:
                            x[j, i] = t[s:e][j]
                            break
                        else:
                            t[j+s:e] = np.random.permutation(t[j+s:e])
                            inner_count += 1
                            continue 
                    else:
                        return False
                    return True
                    
                count = 0
                while 50 > count:
                    if not any(ele in m for ele in t[:3]) and not any(ele in n for ele in t[3:]):
                        filled = False
                        for j in range(3):
                            
                            x = __fill(m,mh1,mh2,t,i,j,0,3)
                            y = __fill(n,nh1,nh2,t,i,j,3,6)
                            
                            if not x or not y:
                                break
                            
                        else:
                            break
                    else:
                        t = np.random.permutation(t)
                        count += 1
                else:
                    return  False
                return True
            
            valid = False
            for i in range(3):
                
                t = [x for x in range(1,10) if x not in mnv[:, i]]
                x =  __nested_backtrack(m, mh1, mh2, n, nh1, nh2, t, i)
                if not x:
                    break
            else:
                valid = True
            return valid
        
        count = 0
        is_filled = True
        while 500 > count:
            
            x = __backtrack(m, mh1, mh2, mnv, n, nh1, nh2)
            if x:
                break
            m = np.zeros((3, 3), dtype='i')
            n = np.zeros((3, 3), dtype='i')
            count += 1
        else:
            is_filled = False
            print('failed !!!!invalid suduko')

        return m , n 
        
    
a = Suduko_gird_value_generator(main_grid)

for i in range(9):
    for j in range(9):
        if main_grid[i, j] != 0:
            print(main_grid[i, j],end = ' ')
        else:
            print('-',end=' ')
    print()

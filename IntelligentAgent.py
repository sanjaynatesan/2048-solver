import random
import time
import math
from BaseAI import BaseAI

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        start_time = time.process_time()
        # Selects a random move and returns it
        #moveset = grid.getAvailableMoves()
        remaining, maxdepth, bestmove, bestUtility = 0.2, 0, None, 0 
        while time.process_time() - start_time <= 0.2 and maxdepth <= 4:
            maxdepth += 2
            move, _, utility = self.maximize(grid, float('-inf'), float('inf'), start_time, remaining, maxdepth)
            if utility > bestUtility:
                bestmove, bestUtility = move, utility
            #print("monotonicity: ", (self.monotonicity(grid)*0))
            # print("edge: ", (self.isedge(grid)*100))
            # print("max: ", (self.maxValue(grid)**2))
            # print("empty: ", (self.emptyleft(grid)**2))
            # print("smoothness: ", (self.smoothness(grid)*50))
            # print("snake: ", (self.snake(grid)**2))
        return bestmove
        #return random.choice(moveset)[0] if moveset else None
    def minimize(self, grid, alpha, beta, start_time, remaining_time, maxdepth):
        if (maxdepth == 0 or remaining_time < 0.00000001):
            return (None, None, self.eval(grid)) #CHECK
        minMove, minChild, minUtil = None, 0, float('inf')
        for loc in grid.getAvailableCells():
            newGrid2 = grid.clone()
            newGrid2.insertTile(loc, 2) 
            remaining_time = (0.2 - (time.process_time() - start_time)) / len(grid.getAvailableMoves())
            _, _, utility2 = self.maximize(newGrid2, alpha, beta, start_time, remaining_time, maxdepth - 1)

            newGrid4 = grid.clone()
            newGrid4.insertTile(loc, 4) 
            _, _, utility4 = self.maximize(newGrid4, alpha, beta, start_time, remaining_time, maxdepth - 1)

            utility = utility2 * 0.9 + utility4 * 0.1
            if utility < minUtil:
                minMove, minChild, minUtil = loc, newGrid2, utility
            if minUtil <= alpha:
                break
            if minUtil < beta:
                beta = minUtil
        return (minMove, minChild, minUtil)
    def maximize(self, grid, alpha, beta, start_time, remaining_time, maxdepth):
        if (maxdepth == 0 or time.process_time() - start_time >= 0.2):
            return (None, None, self.eval(grid)) #CHECK
        maxMove, maxChild, maxUtil = None, 0, float('-inf')
        for move, child in grid.getAvailableMoves():
            remaining_time = (0.2 - (time.process_time() - start_time)) / len(grid.getAvailableMoves())
            _, _, utility = self.minimize(child, alpha, beta, start_time, remaining_time, maxdepth - 1)

            if utility > maxUtil:
                maxMove ,maxChild, maxUtil = move, child, utility
            if maxUtil >= beta:
                break
            if maxUtil > alpha:
                alpha = maxUtil
        return (maxMove, maxChild, maxUtil)
    def eval(self, grid):
        # maxValHeur = self.maxValue(grid)
        # smoothnessHeur = self.smoothness(grid)
        # emptyHeur = self.emptyleft(grid)
        # isedgeHeur = self.isedge(grid)
        # monotonicityHeur = self.monotonicity(grid)
        snakeHeur = self.snake(grid)
        return snakeHeur**2 #+ maxValHeur**2 + emptyHeur**2 + (100)*isedgeHeur + 0 * monotonicityHeur + smoothnessHeur*50
    def maxValue(self, grid):
        maxTile = grid.getMaxTile()
        return math.log(maxTile, 2)
    def monotonicity(self, grid):
        r, c = 0, 0
        for i in range(4):
            arr = []
            for j in range(4):
                t = grid.getCellValue([i, j])
                if t != 0:
                    arr.append(math.log(t, 2))
            if arr == sorted(arr) or arr == sorted(arr, reverse=True):
                r += 1
        for col in range(4):
            temp = []
            for row in range(4):
                tc = grid.getCellValue([row, col])
                if tc != 0:
                    temp.append(math.log(tc, 2))
            if temp == sorted(temp) or temp == sorted(temp, reverse = True): 
                c += 1
        return abs(r + c) / 8
    def smoothness(self, grid):
        score = 1
        for r in range(4):
            for c in range(4):
                value = grid.getCellValue([r, c])
                right = grid.getCellValue([r+1, c])
                bottom = grid.getCellValue([r, c+1])
                if value != 0:
                    if grid.crossBound([r, c+1]) and bottom != 0:
                        score += abs(math.log(value, 2)**1.4 - math.log(bottom, 2)**1.4)
                    if grid.crossBound([r+1, c]) and right != 0:
                        score += abs(math.log(value, 2)**1.4 - math.log(right, 2)**1.4)
        return -score/(16-len(grid.getAvailableCells())) / 8
    def emptyleft(self, grid):
        return len(grid.getAvailableCells())
    def isedge(self, grid):
        largest = grid.getMaxTile()
        #r, c = 0, 0
        value = 0
        for i in range(4):
            for j in range(4):
                if grid.getCellValue([i, j]) == largest:
                    if i == 0 and j == 0:
                        value = max(1, value)
                    elif (i == 0 or i == 4) and (j == 0 or j == 4):
                        value = max(0.8, value)
                    elif ((i == 0 or i == 4) and (j == 1 or j == 3)) or ((i == 1 or i == 3) and (j == 0 or j == 4)):
                        value = max(0.5, value)
                    else:
                        value -= 0.1

        return value
    def snake(self, grid):
        #from top left
        tlscore, trscore, tldscore, trdscore = 0, 0, 0, 0

        # mask1 = [[0 for _ in range(4)] for _ in range(4)]
        # for i in range(4):
        #     for j in range(4):
        #         tempval = grid.getCellValue([i, j])
        #         mask1[i][j] = tempval
        
        mask1 = [[0 for _ in range(4)] for _ in range(4)]
        count = 15
        for i in range(4):
            if i%2 == 0:
                for j in range(4):
                    mask1[i][j] = 2**count
                    count -= 1
            else:
                for j in range(3, -1, -1):
                    mask1[i][j] = 2**count
                    count -= 1

        mask2 = [[mask1[j][i] for j in range(4)] for i in range(3, -1, -1)]
        mask3 = [[mask2[j][i] for j in range(4)] for i in range(3, -1, -1)]
        mask4 = [[mask3[j][i] for j in range(4)] for i in range(3, -1, -1)]

        total1 = sum([(mask1[i][j] * grid.getCellValue((i, j))) for i in range(4) for j in range(4)])
        total2 = sum([(mask2[i][j] * grid.getCellValue((i, j))) for i in range(4) for j in range(4)])
        total3 = sum([(mask3[i][j] * grid.getCellValue((i, j))) for i in range(4) for j in range(4)])
        total4 = sum([(mask4[i][j] * grid.getCellValue((i, j))) for i in range(4) for j in range(4)])

        return max(total1, total2, total3, total4)
        # arr = []
        # for i in range(4):
        #     for j in range(4):
        #         tempval = grid.getCellValue([i, j])
        #         arr.append(tempval)
        # tlorder = [0, 1, 2, 3, 7, 6, 5, 4, 8, 9, 10, 11, 15, 14, 13, 12]
        # for i in range(15):
        #     if arr[tlorder[i]] >= arr[tlorder[i+1]] and arr[tlorder[i]] != 0:
        #         tlscore += math.log(arr[tlorder[i]], 2)**1.1
        #     else:
        #         break
        
        # trorder = [3, 2, 1, 0, 4, 5, 6, 7, 11, 10, 9, 8, 12, 13, 14, 15]
        # for i in range(15):
        #     if arr[trorder[i]] >= arr[trorder[i+1]] and arr[trorder[i]] != 0:
        #         trscore += math.log(arr[trorder[i]], 2)**1.1
        #     else:
        #         break
                    
        # tldorder = [0, 4, 8, 12, 13, 9, 5, 1, 2, 6, 10, 14, 15, 11, 7, 3]
        # for i in range(15):
        #     if arr[tldorder[i]] >= arr[tldorder[i+1]] and arr[tldorder[i]] != 0:
        #         tldscore += math.log(arr[tldorder[i]], 2)**1.1
        #     else:
        #         break

        # trdorder = [3, 7, 11, 15, 14, 10, 6, 2, 1, 5, 9, 13, 12, 8, 4, 0]
        # for i in range(15):
        #     if arr[trdorder[i]] >= arr[trdorder[i+1]] and arr[trdorder[i]] != 0:
        #         trdscore += math.log(arr[trdorder[i]], 2)**1.1
        #     else:
        #         break

        # return max(trscore, tlscore, trdscore, tldscore)
#eval function with heuristics... smoothness and monotonicity, highest value, tile in corner
#make sure heuristics are scaled properly
#eval will call all the heuristics
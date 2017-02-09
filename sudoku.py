#!/usr/bin/env python3
import time
class Solution(object):
    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        self.board=[''.join(i) for i in board]
        self.b1b=lambda x:x&(x-1)
        self.num=[1<<i for i in range(9)]
        c2b=lambda c: 0x1ff if c=='.' else self.num[int(c)-1]
        self.sol={self.num[i]:i+1 for i in range(9)}
        self.board={(i,j):c2b(board[i][j]) for i in range(9) for j in range(9)}
        self.notrmv={(i,j): True for i in range(9) for j in range(9)}
        self.rows=[[(i,j) for j in range(9)]for i in range(9)]
        self.cols=[[(i,j) for i in range(9)]for j in range(9)]
        self.sqrs=[[(ii,jj) for ii in range(i,i+3) for jj in range(j,j+3)]for i in range(0,9,3) for j in range(0,9,3)]
        self.rows_left=[[(i,j) for j in range(9)]for i in range(9)]
        self.cols_left=[[(i,j) for i in range(9)]for j in range(9)]
        self.sqrs_left=[[(ii,jj) for ii in range(i,i+3) for jj in range(j,j+3)]for i in range(0,9,3) for j in range(0,9,3)]
        self.idxs=self.board.keys()
        self.sub=self.rows
        self.sub.extend(self.cols)
        self.sub.extend(self.sqrs)
        self.solve()
        b2c=lambda b: str(self.sol[b]) if b in self.sol else '.'
        for i in range(9):
            board[i]=''.join(map(b2c,[self.board[(i,j)] for j in range(9)]))
    def __str__(self):
        b2c=lambda b: str(self.sol[b]) if b in self.sol else ' '
        return ''.join(['['+'|'.join([b2c(self.board[(r,c)]) for c in xrange(9)])+']\n' for r in xrange(9)])
    def solve(self):
        self.first_stage()
        if self.quick_check():
            return
        self.second_stage()
        if self.quick_check():
            return
        self.third_stage()
    def first_stage(self):
        for p in self.idxs:
            if self.board[p] in self.sol and self.notrmv[p]:
                self.removev(p)
    def second_stage(self):
        for i in range(9):
            for cc in self.rows_left:
                b=0
                for p in cc: b=(b<<1)|(self.board[p]>>i & 1)
                if b in self.sol and b:
                    p=cc[-self.sol[b]]
                    self.board[p]=self.num[i]
                    if self.notrmv[p]:
                        self.removev(p)
            for cc in self.cols_left:
                b=0
                for p in cc: b=(b<<1)|(self.board[p]>>i & 1)
                if b in self.sol and b:
                    p=cc[-self.sol[b]]
                    self.board[p]=self.num[i]
                    if self.notrmv[p]:
                        self.removev(p)
            for cc in self.sqrs_left:
                b=0
                for p in cc: b=(b<<1)|(self.board[p]>>i & 1)
                if b in self.sol and b:
                    p=cc[-self.sol[b]]
                    self.board[p]=self.num[i]
                    if self.notrmv[p]:
                        self.removev(p)
    def solve2(self):
        for i in range(9):
            for cc in self.rows_left:
                b=0
                for p in cc: b=(b<<1)|(self.board[p]>>i & 1)
                if b in self.sol and b:
                    p=cc[-self.sol[b]]
                    self.board[p]=self.num[i]
                    if self.notrmv[p]:
                        self.removev2(p)
            for cc in self.cols_left:
                b=0
                for p in cc: b=(b<<1)|(self.board[p]>>i & 1)
                if b in self.sol and b:
                    p=cc[-self.sol[b]]
                    self.board[p]=self.num[i]
                    if self.notrmv[p]:
                        self.removev2(p)
            for cc in self.sqrs_left:
                b=0
                for p in cc: b=(b<<1)|(self.board[p]>>i & 1)
                if b in self.sol and b:
                    p=cc[-self.sol[b]]
                    self.board[p]=self.num[i]
                    if self.notrmv[p]:
                        self.removev2(p)
        if self.check():
            return True
        else:
            return self.third_stage()

    def third_stage(self):
        for p in self.idxs:
#            if self.b1b(self.board[p]) in self.num or self.b1b(self.b1b(self.board[p])) in self.num:
            if self.notrmv[p]:
                for i in [j for j in self.num if j&self.board[p]]:
                    t={pp:self.board[pp] for pp in self.idxs}
                    tt={pp:self.notrmv[pp] for pp in self.idxs}
                    self.board[p]=i
                    self.removev2(p)
                    if self.solve2():
                        return True
                    self.board={pp:t[pp] for pp in self.idxs}
                    self.notrmv={pp:tt[pp] for pp in self.idxs}
        return False
    def quick_check(self):
        for p in self.idxs:
            if self.notrmv[p]:
                return False
        return True
    def check(self):
        for p in self.idxs:
            if not self.board[p] in self.sol:
                return False
        for cc in self.sqrs:
            if len({self.sol[self.board[p]] for p in cc})!=9:
                return False
        for cc in self.rows:
            if len({self.sol[self.board[p]] for p in cc})!=9:
                return False
        for cc in self.cols:
            if len({self.sol[self.board[p]] for p in cc})!=9:
                return False
        return True

    def removev(self,posi):
        (r,c)=posi
        self.notrmv[posi]=False
        value=self.board[posi]
        norvalue=~value
        self.rows_left[r].remove(posi)
        self.cols_left[c].remove(posi)
        self.sqrs_left[int(r/3)*3+int(c/3)].remove(posi)
        for p in self.rows[r]:
            if self.notrmv[p]:
                self.board[p]=self.board[p]&norvalue
                if self.board[p] in self.sol:
                    self.removev(p)
        for p in self.cols[c]:
            if self.notrmv[p]:
                self.board[p]=self.board[p]&norvalue
                if self.board[p] in self.sol:
                    self.removev(p)
        for p in self.sqrs[int(r/3)*3+int(c/3)]:
            if self.notrmv[p]:
                self.board[p]=self.board[p]&norvalue
                if self.board[p] in self.sol:
                    self.removev(p)
    def removev2(self,posi):
        (r,c)=posi
        self.notrmv[posi]=False
        value=self.board[posi]
        norvalue=~value
        for p in self.rows_left[r]:
            if self.notrmv[p]:
                self.board[p]=self.board[p]&norvalue
                if self.board[p] in self.sol:
                    self.removev2(p)
        for p in self.cols_left[c]:
            if self.notrmv[p]:
                self.board[p]=self.board[p]&norvalue
                if self.board[p] in self.sol:
                    self.removev2(p)
        for p in self.sqrs_left[int(r/3)*3+int(c/3)]:
            if self.notrmv[p]:
                self.board[p]=self.board[p]&norvalue
                if self.board[p] in self.sol:
                    self.removev2(p)
if __name__=='__main__':
    start=time.clock()
    board=["..9748...","7........",".2.1.9...","..7...24.",".64.1.59.",".98...3..","...8.3.2.","........6","...2759.."]
    s=Solution()
    s.solveSudoku(board)
    print(s)
    print('use time ',time.clock()-start)

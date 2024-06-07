class SelectNews :
	
    def __init__(self, matrix) :
        self.matrix = matrix
        self.col_size = len(matrix[0])
        self.row_size = 5
        self.col = [0] * 5
        self.result =[]
        self.found = 0

    def exec_algorithm(self) :
        self.result = []
        self.select(-1)
        return self.result

    def promising(self, i) :
        k = 0
        switch = 1
        while (k < i and switch) :
            if (self.col[i] == self.col[k] or self.found) :
                switch = 0
            k += 1
        return switch

    def select(self, i) :
        if (self.promising(i)) :
            if (i==self.row_size-1) :
                location = []
                for idx in range(0, self.row_size) :
                    location.append(self.col[idx])

                # 만약 matrix[idx][location[idx]] 값이 0인 게 하나라도 있으면 not solution
                # 발견된 첫 번째 solution을 result에 저장

                self.found = 1
                for idx in range(self.row_size) :
                    if (self.matrix[idx][location[idx]] == 0) :
                        self.found = 0
                
                if (self.found == 1) :
                    self.result = location

            else : 
                for j in range(0, self.col_size) :
                    self.col[i+1] = j
                    self.select(i+1)


import requests
from SelectNews import SelectNews

def split_news_list(list) :
    length = len(list)

    partition_size = length // 3
    start = 0

    high_news = []
    mid_news = []
    low_news  = []

    low_news = list[:partition_size]
    start += partition_size
    mid_news = list[start:start+partition_size]
    start += partition_size
    high_news = list[start:]

    return high_news, mid_news, low_news

def find_index(list, media) :
    for idx in range(len(list)) :
        if list[idx] == media:
            return idx
    return None

def create_row(row, list, matrix, media) :
    ### matrix 열 크기를 최대 열 크기에 맞춤
    matrix = pad_matrix(matrix, 0)

    for news in list :
        index = find_index(media, news["media"])
        if index != None :
                matrix[row][index] = news
        else :
            matrix[row].append(news)
            media.append(news["media"])
    
    return matrix

                
def pad_matrix(matrix, value) :
    max_length = max(len(row) for row in matrix)
    return [row + [value] * (max_length - len(row)) for row in matrix]


####### execution #######
query = [100, 101, 102, 103, 105]

### 2-dimension array
highMatrix = [[] * 1 for row in range(5)]
midMatrix = [[] * 1 for row in range(5)]
lowMatrix = [[] * 1 for row in range(5)]

### media list
highMedia = []
midMedia = []
lowMedia = []

# 카테고리별로 뉴스 3개씩 찾기
for i in range(5) :
    response = requests.get(f"http://localhost:8002/getLevel?category={query[i]}")
    if (response.status_code == 200) :
        data = response.json()
        newsList = data["news"]

        highList, midList, lowList = split_news_list(newsList)
        highMatrix = create_row(i, highList, highMatrix, highMedia)
        midMatrix = create_row(i, midList, midMatrix, midMedia)
        lowMatrix = create_row(i, lowList, lowMatrix, lowMedia)

highMatrix = pad_matrix(highMatrix, 0)
midMatrix = pad_matrix(midMatrix, 0)
lowMatrix = pad_matrix(lowMatrix, 0)

highObject = SelectNews(highMatrix)
highSolution = highObject.exec_algorithm()

print(highSolution)

for i in range(5) :
    print("=========="+str(i)+"==========")
    print(highMatrix[i][highSolution[i]])
    print()
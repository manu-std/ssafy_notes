# input.txt 미사용
import copy
arr = list(range(1, 11))


result = []
def recur(subset, i, arr):	      
  if i == len(arr):
    if sum(subset)==10:
     		     # 재귀함수의 탈출조건
        result.append(copy.copy(subset)) # 결과에 들어가는 모든 원소에 해당하는 부분집합의 레퍼런스가 
        return			     # subset으로 같기 때문에 subset을 카피하여 넣어줘야 한다.
				     # 이렇게 하지 않으면 result에 들어가는 모든 부분집합이 공집합으로 나온다.
  else:
    subset.append(arr[i])
    i += 1
    recur(subset, i, arr) 	     # i번째 원소가 '있을' 때의 경우에서 분화
    subset.pop()					
    recur(subset, i, arr)	     # i번째 원소가 '없을' 때의 경우에서 분화
    
recur([], 0, arr)
print(result)
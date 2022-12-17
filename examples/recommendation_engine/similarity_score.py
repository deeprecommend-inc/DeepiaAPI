from cmath import sqrt
from dataset import dataset

# ユークリッド距離

def similarity_score(person1, person2):
    both_viewed = {}

    for item in dataset[person1]:
        if item in dataset[person2]:
            both_viewed[item] = 1
    
    if len(both_viewed) == 0:
        return 0
    
    sum_of_eclidean_distane = []

    for item in dataset[person1]:
        if item in dataset[person2]:
            sum_of_eclidean_distane.append(
                pow(dataset[person1][item] - dataset[person2][item], 2)
            )
    total_of_eclidean_distance = sum(sum_of_eclidean_distane)

    return 1 / (1 + sqrt(total_of_eclidean_distance))

print("山田さんと鈴木さんの類似度 (ユークリッド距離)", similarity_score('山田', '鈴木'))

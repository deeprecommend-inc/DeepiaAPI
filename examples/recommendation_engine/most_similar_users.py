from pearson_correlation import pearson_correlation
from dataset import dataset

def most_similar_users(person, number_of_users):
    scores = [(pearson_correlation(person, other_person), other_person)
        for other_person in dataset if other_person != person]
    
    scores.sort()
    scores.reverse()
    return scores[0:number_of_users]

print("山田さん似た人ベスト 3", most_similar_users('山田', 3))
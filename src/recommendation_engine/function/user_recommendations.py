from pearson_correlation import pearson_correlation
from dataset import dataset

def user_recommendations(person):
    totals = {}
    simSums = {}
    for other in dataset:
        if other == person:
            continue
        sim = pearson_correlation(person, other)
    
        if sim <= 0:
            continue
        for item in dataset[other]:
            if item not in dataset[person] or dataset[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += dataset[other][item] * sim

                simSums.setdefault(item, 0)
                simSums[item] += sim
    
    rankings = [(total / simSums[item], item) for item, total in list(totals.items())]
    rankings.sort()
    rankings.reverse()
    recommendations_list = [
        recommend_item for score, recommend_item in rankings]
    return recommendations_list

print("下ばやしさんにおすすめのメニュー", user_recommendations('下林'))
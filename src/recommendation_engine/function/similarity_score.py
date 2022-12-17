from cmath import sqrt


dataset = {
    '0': {
        'youtube.com': 3,
        'twitter.com': 4,
        'facebook.com': 1,
        'tiktok.com': 2,
        'instagram.com': 20,
    },
    '1': {
        'youtube.com': 31,
        'twitter.com': 33,
        'facebook.com': 31,
        'tiktok.com': 354,
        'instagram.com': 13,
    },
    '2': {
        'youtube.com': 37,
        'twitter.com': 33,
        'facebook.com': 43,
        'tiktok.com': 3,
        'instagram.com': 3,
    },
    '3': {
        'youtube.com': 3,
        'twitter.com': 3,
        'facebook.com': 3,
        'tiktok.com': 3,
        'instagram.com': 3,
    },
    '4': {
        'youtube.com': 3,
        'twitter.com': 3,
        'facebook.com': 3,
        'tiktok.com': 3,
        'instagram.com': 3,
    },
    '5': {
        'youtube.com': 3,
        'twitter.com': 3,
        'facebook.com': 3,
        'tiktok.com': 3,
        'instagram.com': 3,
    },
    '6': {
        'youtube.com': 3,
        'twitter.com': 3,
        'facebook.com': 3,
        'tiktok.com': 3,
        'instagram.com': 3,
    },
}

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
                pow(dataset[person1][item] - dataset[person2][item], 2))
    total_of_eclidean_distance = sum(sum_of_eclidean_distane)

    return 1 / (1 + sqrt(total_of_eclidean_distance))

print("0と1の類似度 (ユークリッド距離)", similarity_score('0', '1'))

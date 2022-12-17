from dataset import dataset
from math import sqrt

# ピアソン相関係数

def pearson_correlation(person1, person2):
    both_rated = {}
    for item in dataset[person1]:
        if item in dataset[person2]:
            both_rated[item] = 1
    
    number_of_ratings = len(both_rated)

    if number_of_ratings == 0:
        return 0
    
    person1_preferences_sum = sum(
        [dataset[person1][item] for item in both_rated]
    )
    person2_preferences_sum = sum(
        [dataset[person2][item] for item in both_rated]
    )

    product_sum_of_both_users = sum(
        [dataset[person1][item] * dataset[person2][item] for item in both_rated]
    )

    numerator_value = product_sum_of_both_users - \
        (person1_preferences_sum * person2_preferences_sum / number_of_ratings)
    denominator_value = sqrt((person1_preferences_sum - pow(person1_preferences_sum, 2) / number_of_ratings) * (person2_preferences_sum - pow(person2_preferences_sum, 2) / number_of_ratings))
    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r

print("山田と田中の類似度（ピアソン相関係数)", (pearson_correlation('山田', '田中')))
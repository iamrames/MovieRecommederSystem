from math import sqrt

def pearson(pairs):
    series_1 = [float(pair[0]) for pair in pairs]
    series_2 = [float(pair[1]) for pair in pairs]

    sum1 = sum(series_1)
    sum2 = sum(series_2)

    squares1 = sum([ n*n for n in series_1 ])
    squares2 = sum([ n*n for n in series_2 ])

    product_sum = sum([ n * m for n,m in pairs ])

    size = len(pairs)

    numerator = product_sum - ((sum1 * sum2)/size)
    denominator = sqrt((squares1 - (sum1*sum1) / size) * (squares2 - (sum2*sum2)/size))

    if denominator == 0:
        return 0
    
    return numerator/denominator

# Example of uncorrelated data
corr1 = pearson([(1,2), (2,5), (3,5), (5,1)])
print(corr1)
# value is -.355

# Example of correlated data
corr2 = pearson([(2,2), (2,3), (4,3), (5,5)])
print(corr2)
# value is .83
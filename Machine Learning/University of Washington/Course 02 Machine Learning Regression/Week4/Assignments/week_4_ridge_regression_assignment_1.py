# -*- coding: utf-8 -*-
"""Week 4: Ridge Regression Assignment 1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qjkYYJiZmLzZ2709P4o_CidWoRj8kKv4

Regression Week 4: Ridge Regression Assignment 1
In this assignment, we will run ridge regression multiple times with different L2 penalties to see which one produces the best fit. We will revisit the example of polynomial regression as a means to see the effect of L2 regularization. In particular, we will:

Use a pre-built implementation of regression to run polynomial regression
Use matplotlib to visualize polynomial regressions
Use a pre-built implementation of regression to run polynomial regression, this time with L2 penalty
Use matplotlib to visualize polynomial regressions under L2 regularization
Choose best L2 penalty using cross-validation.
Assess the final fit using test data.
We will continue to use the House data from previous assignments. (In the next programming assignment for this module, you will implement your own ridge regression learning algorithm using gradient descent.)
"""

!pip install turicreate

import turicreate
from turicreate import SFrame
import numpy as np
import math

def polynomial_sframe(feature, degree):
    # assume that degree >= 1
    # initialize the SFrame:
    poly_sframe = turicreate.SFrame()
    # and set poly_sframe['power_1'] equal to the passed feature
    poly_sframe['power_1'] = feature
    # first check if degree > 1
    if degree > 1:
        # then loop over the remaining degrees:
        for power in range(2, degree+1):
            # first we'll give the column a name:
            name = 'power_' + str(power)
            # assign poly_sframe[name] to be feature^power
            poly_sframe[name] = feature.apply(lambda x: x**power)
    return poly_sframe

sales = turicreate.SFrame('/content/drive/My Drive/Colab Notebooks/Machine Learning/Course 2 Machine Learning Regression/Week2/Assignment1/home_data.sframe')
sales = sales.sort(['sqft_living','price'])
sales

"""3. Let us revisit the 15th-order polynomial model using the 'sqft_living' input. Generate polynomial features up to degree 15 using `polynomial_sframe()` and fit a model with these features. When fitting the model, use an L2 penalty of 1.5e-5:
    
       l2_small_penalty = 1.5e-5
"""

l2_small_penalty = 1.5e-5

"""**Note:** When we have so many features and so few data points, the solution can become highly numerically unstable, which can sometimes lead to strange unpredictable results. Thus, rather than using no regularization, we will introduce a tiny amount of regularization (l2_penalty=1.5e-5) to make the solution numerically stable. (In lecture, we discussed the fact that regularization can also help with numerical stability, and here we are seeing a practical example.)

With the L2 penalty specified above, fit the model and print out the learned weights. Add "alpha=l2_small_penalty" and "normalize=True" to the parameter list of linear_model.Ridge:

      from sklearn import linear_model
      import numpy as np

      poly15_data = polynomial_sframe(sales['sqft_living'], 15) # use equivalent of `polynomial_sframe`
      model = linear_model.Ridge(alpha=l2_small_penalty, normalize=True)
      model.fit(poly15_data, sales['price'])
"""

from sklearn import linear_model
 
poly15_data = polynomial_sframe(sales['sqft_living'], 15) # use equivalent of `polynomial_sframe`

poly15_features = poly15_data.column_names() # get the name of the features
poly15_data['price'] = sales['price']

model15 = turicreate.linear_regression.create(poly15_data, 
                                             target = 'price',
                                             features = poly15_features,
                                             l2_penalty = l2_small_penalty,
                                             validation_set = None,
                                             verbose=False)

model15.coefficients.print_rows(num_rows = 16)

"""4. **Quiz Question:** What’s the learned value for the coefficient of feature power_1?

#**Observe Overfitting**

5. Recall from Module 3 (Polynomial Regression) that the polynomial fit of degree 15 changed wildly whenever the data changed. In particular, when we split the sales data into four subsets and fit the model of degree 15, the result came out to be very different for each subset. The model had a high variance. We will see in a moment that ridge regression reduces such variance. But first, we must reproduce the experiment we did in Module 3.

*   first split sales into 2 subsets with .random_split(.5) use seed = 0!
*   next split these into 2 more subsets (4 total) using random_split(0.5) again set seed = 0!
*   you should have 4 subsets of (approximately) equal size, call them set_1, set_2, set_3, and set_4
"""

set1_1, set2_2 = sales.random_split(.5, seed=0)
set1, set2 = set1_1.random_split(.5, seed=0)
set3, set4 = set2_2.random_split(.5, seed=0)

l2_poly_penalty=1e-9

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline

set1_data = polynomial_sframe(set1['sqft_living'], 15)
set1_features = set1_data.column_names() # get the name of the features
set1_data['price'] = set1['price']
set1_model = turicreate.linear_regression.create(set1_data, 
                                             target = 'price',
                                             features = set1_features,
                                             l2_penalty = l2_poly_penalty,
                                             validation_set = None,
                                             verbose = False)
set1_model.coefficients.print_rows(num_rows=16)
plt.plot(set1_data['power_1'], set1_data['price'], '.', set1_data['power_1'], set1_model.predict(set1_data), '-')

set2_data = polynomial_sframe(set2['sqft_living'], 15)
set2_features = set2_data.column_names() # get the name of the features
set2_data['price'] = set2['price']
set2_model = turicreate.linear_regression.create(set2_data, 
                                             target = 'price',
                                             features = set2_features,
                                             l2_penalty = l2_poly_penalty,
                                             validation_set = None,
                                             verbose = False)
set2_model.coefficients.print_rows(num_rows=16)
plt.plot(set2_data['power_1'], set2_data['price'], '.', set2_data['power_1'], set2_model.predict(set2_data), '-')

set3_data = polynomial_sframe(set3['sqft_living'], 15)
set3_features = set3_data.column_names() # get the name of the features
set3_data['price'] = set3['price']
set3_model = turicreate.linear_regression.create(set3_data, 
                                             target = 'price',
                                             features = set3_features,
                                             l2_penalty = l2_poly_penalty,
                                             validation_set = None,
                                             verbose = False)
set3_model.coefficients.print_rows(num_rows=16)
plt.plot(set3_data['power_1'], set3_data['price'], '.', set3_data['power_1'], set3_model.predict(set3_data), '-')

set4_data = polynomial_sframe(set4['sqft_living'], 15)
set4_features = set4_data.column_names() # get the name of the features
set4_data['price'] = set4['price']
set4_model = turicreate.linear_regression.create(set4_data, 
                                             target = 'price',
                                             features = set4_features,
                                             l2_penalty = l2_poly_penalty,
                                             validation_set = None,
                                             verbose = False)
set4_model.coefficients.print_rows(num_rows=16)
plt.plot(set4_data['power_1'], set4_data['price'], '.', set4_data['power_1'], set4_model.predict(set4_data), '-')

"""8. **Quiz Question:** For the models learned in each of these training sets, what are the smallest and largest values you learned for the coefficient of feature power_1?

# **Ridge regression comes to rescue**

9. Generally, whenever we see weights change so much in response to change in data, we believe the variance of our estimate to be large. Ridge regression aims to address this issue by penalizing "large" weights. (The weights looked quite small, but they are not that small because 'sqft_living' input is in the order of thousands.)

10. Fit a 15th-order polynomial model on set_1, set_2, set_3, and set_4, this time with a large L2 penalty. Make sure to add "alpha=l2_large_penalty" and "normalize=True" to the parameter list, where the value of l2_large_penalty is given by
"""

l2_large_penalty=1.23e2

set1_data = polynomial_sframe(set1['sqft_living'], 15)
set1_features = set1_data.column_names() # get the name of the features
set1_data['price'] = set1['price']
set1_model = turicreate.linear_regression.create(set1_data, 
                                             target = 'price',
                                             features = set1_features,
                                             l2_penalty = l2_large_penalty,
                                             validation_set = None,
                                             verbose = False)
set1_model.coefficients.print_rows(num_rows=16)
plt.plot(set1_data['power_1'], set1_data['price'], '.', set1_data['power_1'], set1_model.predict(set1_data), '-')

set2_data = polynomial_sframe(set2['sqft_living'], 15)
set2_features = set2_data.column_names() # get the name of the features
set2_data['price'] = set2['price']
set2_model = turicreate.linear_regression.create(set2_data, 
                                             target = 'price',
                                             features = set2_features,
                                             l2_penalty = l2_large_penalty,
                                             validation_set = None,
                                             verbose = False)
set2_model.coefficients.print_rows(num_rows=16)
plt.plot(set2_data['power_1'], set2_data['price'], '.', set2_data['power_1'], set2_model.predict(set2_data), '-')

set3_data = polynomial_sframe(set3['sqft_living'], 15)
set3_features = set3_data.column_names() # get the name of the features
set3_data['price'] = set3['price']
set3_model = turicreate.linear_regression.create(set3_data, 
                                             target = 'price',
                                             features = set3_features,
                                             l2_penalty = l2_large_penalty,
                                             validation_set = None,
                                             verbose = False)
set3_model.coefficients.print_rows(num_rows=16)
plt.plot(set3_data['power_1'], set3_data['price'], '.', set3_data['power_1'], set3_model.predict(set3_data), '-')

set4_data = polynomial_sframe(set4['sqft_living'], 15)
set4_features = set4_data.column_names() # get the name of the features
set4_data['price'] = set4['price']
set4_model = turicreate.linear_regression.create(set4_data, 
                                             target = 'price',
                                             features = set4_features,
                                             l2_penalty = l2_large_penalty,
                                             validation_set = None,
                                             verbose = False)
set4_model.coefficients.print_rows(num_rows=16)
plt.plot(set4_data['power_1'], set4_data['price'], '.', set4_data['power_1'], set4_model.predict(set4_data), '-')

"""These curves are varieng a lot less, now that we applied a high degree of regularization.

11. **QUIZ QUESTION:** For the models learned with regularization in each of these training sets, what are the smallest and largest values you learned for the coefficient of feature power_1?

#**Selecting an L2 penalty via cross-validation**

12. Just like the polynomial degree, the L2 penalty is a "magic" parameter we need to select. We could use the validation set approach as we did in the last module, but that approach has a major disadvantage: it leaves fewer observations available for training. Cross-validation seeks to overcome this issue by using all of the training set in a smart way.

We will implement a kind of cross-validation called k-fold cross-validation. The method gets its name because it involves dividing the training set into k segments of roughtly equal size. Similar to the validation set method, we measure the validation error with one of the segments designated as the validation set. The major difference is that we repeat the process k times as follows:



*   Set aside segment 0 as the validation set, and fit a model on rest of data, and evalutate it on this validation set

*   Set aside segment 1 as the validation set, and fit a model on rest of data, and evalutate it on this validation set

*   ...

*   Set aside segment k-1 as the validation set, and fit a model on rest of data, and evalutate it on this validation set


After this process, we compute the average of the k validation errors, and use it as an estimate of the generalization error. Notice that all observations are used for both training and validation, as we iterate over segments of data.
"""

import pandas as pd

dtype_dict = {'bathrooms':float, 'waterfront':int, 'sqft_above':int, 'sqft_living15':float, 'grade':int, 'yr_renovated':int, 'price':float, 'bedrooms':float, 'zipcode':str, 'long':float, 'sqft_lot15':float, 'sqft_living':float, 'floors':float, 'condition':int, 'lat':float, 'date':str, 'sqft_basement':int, 'yr_built':int, 'id':str, 'sqft_lot':int, 'view':int}

train_valid_shuffled = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Machine Learning/Course 2 Machine Learning Regression/Week4/Assignment/wk3_kc_house_train_valid_shuffled.csv',dtype=dtype_dict)
test = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Machine Learning/Course 2 Machine Learning Regression/Week4/Assignment/wk3_kc_house_test_data.csv', dtype=dtype_dict)

"""14. Divide the combined training and validation set into equal segments. Each segment should receive n/k elements, where n is the number of observations in the training set and k is the number of segments. Since the segment 0 starts at index 0 and contains n/k elements, it ends at index (n/k)-1. The segment 1 starts where the segment 0 left off, at index (n/k). With n/k elements, the segment 1 ends at index (n*2/k)-1. Continuing in this fashion, we deduce that the segment i starts at index (n*i/k) and ends at (n*(i+1)/k)-1.

With this pattern in mind, we write a short loop that prints the starting and ending indices of each segment, just to make sure you are getting the splits right.
"""

n = len(train_valid_shuffled)
k = 10 # 10-fold cross-validation

for i in range(k):
    start = (n*i)/k
    end = (n*(i+1))/k-1
    print(i, (start, end))

"""Let us familiarize ourselves with array slicing with SFrame. To extract a continuous slice from an SFrame, use colon in square brackets. For instance, the following cell extracts rows 0 to 9 of `train_valid_shuffled`. Notice that the first index (0) is included in the slice but the last index (10) is omitted."""

train_valid_shuffled[0:10] # select rows 0 to 9

"""Meanwhile, to choose the remainder of the data that's not part of the segment i, we select two slices (0:start) and (end+1:n) and paste them together."""

# train_valid_shuffled[0:start].append(train_valid_shuffled[end+1:n])
validation4 = train_valid_shuffled[5818: 7758]

"""# To verify that we have the right elements extracted, run the following cell, which computes the average price of the fourth segment. When rounded to nearest whole number, the average should be $536,234."""

print(int(round(validation4['price'].mean(), 0)))

"""After designating one of the k segments as the validation set, we train a model using the rest of the data. To choose the remainder, we slice (0:start) and (end+1:n) of the data and paste them together. SFrame has `append()` method that pastes together two disjoint sets of rows originating from a common dataset. For instance, the following cell pastes together the first and last two rows of the `train_valid_shuffled` dataframe."""

n = len(train_valid_shuffled)
first_two = train_valid_shuffled[0:2]
last_two = train_valid_shuffled[n-2:n]
print(first_two.append(last_two))

"""Extract the remainder of the data after *excluding* fourth segment (segment 3) and assign the subset to `train4`."""

n = len(train_valid_shuffled)
before_third = train_valid_shuffled[0:5818]
after_third = train_valid_shuffled[7758:n]
train4 = before_third.append(after_third)

"""To verify that we have the right elements extracted, run the following cell, which computes the average price of the data with fourth segment excluded. When rounded to nearest whole number, the average should be $539,450."""

print(int(round(train4['price'].mean(), 0)))

"""Now we are ready to implement k-fold cross-validation. Write a function that computes k validation errors by designating each of the k segments as the validation set. It accepts as parameters (i) `k`, (ii) `l2_penalty`, (iii) dataframe, (iv) name of output column (e.g. `price`) and (v) list of feature names. The function returns the average validation error using k segments as validation sets.
 
* For each i in [0, 1, ..., k-1]:
* Compute starting and ending indices of segment i and call 'start' and 'end'
* Form validation set by taking a slice (start:end+1) from the data.
* Form training set by appending slice (end+1:n) to the end of slice (0:start).
* Train a linear model using training set just formed, with a given l2_penalty
* Compute validation error using validation set just formed
"""

def k_fold_cross_validation(k, l2_penalty, data, output_name, features_list):
    n = len(data)
    errors = []
    for i in range(0, k):
        start = (n*i)/k
        end = (n*(i+1)/k)-1
        validation_set = data[start:end+1]
        training_set = data[0:start].append(data[end+1:n])
        
        model = turicreate.linear_regression.create(training_set,
                                                  target = output_name, features = features_list,
                                                  l2_penalty=l2_penalty,
                                                  validation_set = None,
                                                  verbose = False)
        
        price_validation_predicted = model.predict(validation_set)
        val_errors = price_validation_predicted - validation_set['price']
        RSS = sum(val_errors * val_errors)
        errors.append(RSS)
        
    return sum(errors)/len(errors)

"""Once we have a function to compute the average validation error for a model, we can write a loop to find the model that minimizes the average validation error. Write a loop that does the following:
* We will again be aiming to fit a 15th-order polynomial model using the `sqft_living` input
* For `l2_penalty` in [10^1, 10^1.5, 10^2, 10^2.5, ..., 10^7] (to get this in Python, you can use this Numpy function: `np.logspace(1, 7, num=13)`.)
* Run 10-fold cross-validation with `l2_penalty`
* Report which L2 penalty produced the lowest average validation error.
 
Note: since the degree of the polynomial is now fixed to 15, to make things faster, you should generate polynomial features in advance and re-use them throughout the loop. Make sure to use `train_valid_shuffled` when generating polynomial features!
"""

min_error = None
best_l2_penalty = None
cross_val_error = []
l2_penalty_values = np.logspace(1, 7, num=13)

for l2_penalty in l2_penalty_values:
  # print(l2_penalty)
  avg_val_error = k_fold_cross_validation(10, l2_penalty, poly15_data, 'price', poly15_features)
  # print(avg_val_error)
  cross_val_error.append(avg_val_error)
  if min_error is None or avg_val_error < min_error:
    min_error = avg_val_error
    best_l2_penalty = l2_penalty

print("Best error : ", best_l2_penalty)

"""17. **Quiz Question:** What is the best value for the L2 penalty according to 10-fold validation?

18. Once you found the best value for the L2 penalty using cross-validation, it is important to retrain a final model on all of the training data using this value of l2_penalty. This way, your final model will be trained on the entire dataset.
"""

train_data = polynomial_sframe(sales['sqft_living'], 15)
train_features = train_data.column_names() # get the name of the features
train_data['price'] = sales['price']
train_model = turicreate.linear_regression.create(train_data, 
                                             target = 'price',
                                             features = train_features,
                                             l2_penalty = best_l2_penalty,
                                             validation_set = None,
                                             verbose = False)
train_model.coefficients.print_rows(num_rows=16)
plt.plot(train_data['power_1'], train_data['price'], '.', train_data['power_1'], train_model.predict(train_data), '-')

"""19. **Quiz Question:** Using the best L2 penalty found above, train a model using all training data. What is the RSS on the TEST data of the model you learn with this L2 penalty?"""

train_model.evaluate

test_data = polynomial_sframe(sales['sqft_living'], 15)
difference = train_model.predict(test_data) - test['price']
error_square = (difference * difference)
RSS = error_square.sum()
print(RSS)

test_data = polynomial_sframe(test['sqft_living'], 15)
predictions_test = train_model.predict(test_data)
test_errors = predictions_test - test['price']
RSS_test = (test_errors * test_errors).sum()
print(RSS_test)


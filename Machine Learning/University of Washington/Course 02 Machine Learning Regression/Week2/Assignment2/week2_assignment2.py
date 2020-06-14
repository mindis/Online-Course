# -*- coding: utf-8 -*-
"""Week2 Assignment2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nKzteYITBEeDYevGV69bseUzky8u5Qaf

#**Regression Week 2: Multiple Regression (gradient descent)**
In the first notebook we explored multiple regression using graphlab create. Now we will use graphlab along with numpy to solve for the regression weights with gradient descent.

In this notebook we will cover estimating multiple regression weights via gradient descent. You will:


*   Add a constant column of 1's to a graphlab SFrame to     account for the intercept

*   Convert an SFrame into a Numpy array

*   Write a predict_output() function using Numpy

*   Write a numpy function to compute the derivative of the regression weights with respect to a single feature


*   Write gradient descent function to compute the regression 

*   weights given an initial weight vector, step size and tolerance.

*   Use the gradient descent function to estimate regression weights for multiple features
"""

!pip install turicreate

import turicreate
from turicreate import SFrame

"""#**Load in house sales data**"""

sales = turicreate.SFrame('/content/drive/My Drive/Colab Notebooks/Machine Learning/Course 2 Machine Learning Regression/Week2/Assignment1/home_data.sframe')

"""2. If you’re using python: to do the matrix operations required to perform a gradient descent we will be using the popular python library ‘numpy’ which is a computational library specialized for operations on arrays. For students unfamiliar with numpy we have created a numpy tutorial (see useful resources). It is common to import numpy under the name ‘np’ for short, to do this execute:"""

import numpy as np

"""3. Next write a function that takes a data set, a list of features 
  
         (e.g. [‘sqft_living’, ‘bedrooms’])
  
   to be used as inputs, and a name of the output (e.g. ‘price’). This function should return a features_matrix (2D array) consisting of first a column of ones followed by columns containing the values of the input features in the data set in the same order as the input list. It should also return an output_array which is an array of the values of the output in the data set (e.g. ‘price’). e.g. if you’re using SFrames and numpy you can complete the following function:

       def get_numpy_data(data_sframe, features, output):
            data_sframe['constant'] = 1 # add a constant column to an SFrame
            # prepend variable 'constant' to the features list
            features = ['constant'] + features
            # select the columns of data_SFrame given by the ‘features’ list into the SFrame ‘features_sframe’

            # this will convert the features_sframe into a numpy matrix:
            features_matrix = features_sframe.to_numpy()
            # assign the column of data_sframe associated with the target to the variable ‘output_sarray’

            # this will convert the SArray into a numpy array:
            output_array = output_sarray.to_numpy()
            return(features_matrix, output_array)
"""

def get_numpy_data(data_sframe, features, output):

  data_sframe['constant'] = 1 # add a constant column to an SFrame
  # prepend variable 'constant' to the features list
  features = ['constant'] + features
  # select the columns of data_SFrame given by the ‘features’ list into the SFrame ‘features_sframe’
  features_sframe = data_sframe[features]
  # this will convert the features_sframe into a numpy matrix:
  features_matrix = features_sframe.to_numpy()
  # assign the column of data_sframe associated with the target to the variable ‘output_sarray’
  output_sarray = data_sframe[output]
  # this will convert the SArray into a numpy array:
  output_array = output_sarray.to_numpy()
  return(features_matrix, output_array)

"""For testing let's use the 'sqft_living' feature and a constant as our features and price as our output:"""

(example_features, example_output) = get_numpy_data(sales, ['sqft_living'], 'price') # the [] around 'sqft_living' makes it a list
print(example_features[0,:]) # this accesses the first row of the data the ':' indicates 'all columns'
print(example_output[0]) # and the corresponding output

"""4. If the features matrix (including a column of 1s for the constant) is stored as a 2D array (or matrix) and the regression weights are stored as a 1D array then the predicted output is just the dot product between the features matrix and the weights (with the weights on the right). Write a function ‘predict_output’ which accepts a 2D array ‘feature_matrix’ and a 1D array ‘weights’ and returns a 1D array ‘predictions’. e.g. in python:

        def predict_outcome(feature_matrix, weights):
           [your code here]
           return(predictions)
"""

def predict_output(feature_matrix, weights):
    # assume feature_matrix is a numpy matrix containing the features as columns 
    # and weights is a corresponding numpy array
    # create the predictions vector by using np.dot()
    predictions = np.dot(feature_matrix, weights)
    return(predictions)

"""to test our code run the following cell:"""

my_weights = np.array([1., 1.]) # the example weights
my_features = example_features[0,] # we'll use the first data point

test_predictions = predict_output(example_features, my_weights)
print(test_predictions[0]) 
print(test_predictions[1])

"""5. If we have a the values of a single input feature in an array ‘feature’ and the prediction ‘errors’ (predictions - output) then the derivative of the regression cost function with respect to the weight of ‘feature’ is just twice the dot product between ‘feature’ and ‘errors’. Write a function that accepts a ‘feature’ array and ‘error’ array and returns the ‘derivative’ (a single number). e.g. in python:

    
        def feature_derivative(errors, feature):
            [your code here]
            return(derivative)

We are now going to move to computing the derivative of the regression cost function. Recall that the cost function is the sum over the data points of the squared difference between an observed output and a predicted output.

Since the derivative of a sum is the sum of the derivatives we can compute the derivative for a single data point and then sum over data points. We can write the squared difference between the observed output and predicted output for a single point as follows:

(w[0]*[CONSTANT] + w[1]*[feature_1] + ... + w[i] *[feature_i] + ... + w[k]*[feature_k] - output)^2

Where we have k features and a constant. So the derivative with respect to weight w[i] by the chain rule is:

2*(w[0]*[CONSTANT] + w[1]*[feature_1] + ... + w[i] *[feature_i] + ... + w[k]*[feature_k] - output)* [feature_i]

The term inside the paranethesis is just the error (difference between prediction and output). So we can re-write this as:

2*error*[feature_i]

That is, the derivative for the weight for feature i is the sum (over data points) of 2 times the product of the error and the feature itself. In the case of the constant then this is just twice the sum of the errors!

Recall that twice the sum of the product of two vectors is just twice the dot product of the two vectors. Therefore the derivative for the weight for feature_i is just two times the dot product between the values of feature_i and the current errors.

With this in mind complete the following derivative function which computes the derivative of the weight given the value of the feature (over all data points) and the errors (over all data points).
"""

def feature_derivative(errors,feature):
  # Assume that errors and feature are both numpy arrays of the same length (number of data points)
  # compute twice the dot product of these vectors as 'derivative' and return the value
  derivative = 2*np.dot(errors, feature)
  return(derivative)

"""To test our feature derivartive run the following:"""

(example_features, example_output) = get_numpy_data(sales, ['sqft_living'], 'price') 
my_weights = np.array([0., 0.]) # this makes all the predictions 0
test_predictions = predict_output(example_features, my_weights) 
# just like SFrames 2 numpy arrays can be elementwise subtracted with '-': 
errors = test_predictions - example_output # prediction errors in this case is just the -example_output
feature = example_features[:,0] # let's compute the derivative with respect to 'constant', the ":" indicates "all rows"
derivative = feature_derivative(errors, feature)
print(derivative)
print(-np.sum(example_output)*2)  #should be the same as derivative

"""6. Now we will use our predict_output and feature_derivative to write a gradient descent function. Although we can compute the derivative for all the features simultaneously (the gradient) we will explicitly loop over the features individually for simplicity. Write a gradient descent function that does the following:

Accepts a numpy feature_matrix 2D array, a 1D output array, an array of initial weights, a step size and a convergence tolerance.
While not converged updates each feature weight by subtracting the step size times the derivative for that feature given the current weights
At each step computes the magnitude/length of the gradient (square root of the sum of squared components)
When the magnitude of the gradient is smaller than the input tolerance returns the final weight vector.
e.g. if you’re using SFrames and numpy you can complete the following function:

        def regression_gradient_descent(feature_matrix, output, initial_weights, step_size, tolerance):
            converged = False
            weights = np.array(initial_weights)
            while not converged:
                # compute the predictions based on feature_matrix and weights:
                # compute the errors as predictions - output:
                
                gradient_sum_squares = 0 # initialize the gradient
                # while not converged, update each weight individually:
                for i in range(len(weights)):
                    # Recall that feature_matrix[:, i] is the feature column associated with weights[i]
                    # compute the derivative for weight[i]:
                    
                    # add the squared derivative to the gradient magnitude
                    
                    # update the weight based on step size and derivative:
                    
                gradient_magnitude = sqrt(gradient_sum_squares)
                if gradient_magnitude < tolerance:
                    converged = True
            return(weights)
"""

from math import sqrt

def regression_gradient_descent(feature_matrix, output, initial_weights, step_size, tolerance):
    converged = False 
    weights = np.array(initial_weights) # make sure it's a numpy array
    while not converged:
        # compute the predictions based on feature_matrix and weights using your predict_output() function
        predictions = predict_output(feature_matrix, weights)
        # compute the errors as predictions - output
        errors = predictions - output
        gradient_sum_squares = 0 # initialize the gradient sum of squares
        # while we haven't reached the tolerance yet, update each feature's weight
        for i in range(len(weights)): # loop over each weight
            # Recall that feature_matrix[:, i] is the feature column associated with weights[i]
            # compute the derivative for weight[i]:
            feature = feature_matrix[:, i]
            derivative = feature_derivative(errors, feature)
            # add the squared value of the derivative to the gradient sum of squares (for assessing convergence)
            gradient_sum_squares += derivative**2
            # subtract the step size times the derivative from the current weight
            weights[i] -= step_size*derivative
        # compute the square-root of the gradient sum of squares to get the gradient matnigude:
        gradient_magnitude = sqrt(gradient_sum_squares)
        if gradient_magnitude < tolerance:
            converged = True
    return(weights)

#A few things to note before we run the gradient descent. 
#Since the gradient is a sum over all the data points and involves a product of an error 
#and a feature the gradient itself will be very large since the features are large (squarefeet) 
#and the output is large (prices). So while you might expect "tolerance" to be small, 
#small is only relative to the size of the features.

#For similar reasons the step size will be much smaller than you might expect 
#but this is because the gradient has such large values.

"""7. Now split the sales data into training and test data."""

train_data, test_data = sales.random_split(.8, seed=0)

"""8. Now we will run the regression_gradient_descent function on some actual data. In particular we will use the gradient descent to estimate the model from Week 1 using just an intercept and slope. Use the following parameters:

features: ‘sqft_living’

output: ‘price’

initial weights: -47000, 1 (intercept, sqft_living respectively)

step_size = 7e-12

tolerance = 2.5e7

e.g. in python with numpy and SFrames:
"""

simple_features = ['sqft_living']
my_output= 'price'
(simple_feature_matrix, output) = get_numpy_data(train_data, simple_features, my_output)
initial_weights = np.array([-47000., 1.])
step_size = 7e-12
tolerance = 2.5e7

"""Use these parameters to estimate the slope and intercept for predicting prices based only on ‘sqft_living’."""

my_sqft_weights = regression_gradient_descent(simple_feature_matrix, output, initial_weights, step_size, tolerance)
print(my_sqft_weights)

"""#9. **Quiz Question:** What is the value of the weight for sqft_living -- the second element of ‘simple_weights’ (rounded to 1 decimal place)?

10. Now build a corresponding ‘test_simple_feature_matrix’ and ‘test_output’ using test_data. Using ‘test_simple_feature_matrix’ and ‘simple_weights’ compute the predicted house prices on all the test data.
"""

test_simple_feature_matrix, test_output = get_numpy_data(test_data, simple_features, my_output)

house_price_prediction = predict_output(test_simple_feature_matrix, my_sqft_weights)
print('House price prediction : ', house_price_prediction)

"""#11. **Quiz Question:** What is the predicted price for the 1st house in the Test data set for model 1 (round to nearest dollar)?"""

print(np.rint(house_price_prediction[0]))

"""12. Now compute RSS on all test data for this model. Record the value and store it for later"""

test_errors = house_price_prediction - test_output
RSS = (test_errors*test_errors).sum()
print('RSS : ', RSS)

"""13. Now we will use the gradient descent to fit a model with more than 1 predictor variable (and an intercept). Use the following parameters:

model features = ‘sqft_living’, ‘sqft_living_15’

output = ‘price’

initial weights = [-100000, 1, 1] (intercept, sqft_living, and sqft_living_15 respectively)

step size = 4e-12

tolerance = 1e9

e.g. in python with numpy and SFrames:

      model_features = ['sqft_living', 'sqft_living15']
      my_output = 'price'
     (feature_matrix, output) = get_numpy_data(train_data, model_features,my_output)
      initial_weights = np.array([-100000., 1., 1.])
      step_size = 4e-12
      tolerance = 1e9
"""

model_features = ['sqft_living', 'sqft_living15']
my_output = 'price'
(feature_matrix, output) = get_numpy_data(train_data, model_features,my_output)
initial_model_weights = np.array([-100000., 1., 1.])
step_size = 4e-12
tolerance = 1e9

model_weights = regression_gradient_descent(feature_matrix, output, initial_model_weights, step_size, tolerance)
print(model_weights)

"""14. Use the regression weights from this second model (using sqft_living and sqft_living_15) and predict the outcome of all the house prices on the TEST data."""

(test_feature_matrix, model_output) = get_numpy_data(test_data, model_features, my_output) 
model_test_predictions = predict_output(test_feature_matrix, model_weights)

"""#15. **Quiz Question:** What is the predicted price for the 1st house in the TEST data set for model 2 (round to nearest dollar)?"""

print(np.rint(model_test_predictions[0]))

"""16. What is the actual price for the 1st house in the Test data set?"""

print(test_data[0]['price'])

"""#17. **Quiz Question:** Which estimate was closer to the true price for the 1st house on the TEST data set, model 1 or model 2?
Model 1 is nearer

18. Now compute RSS on all test data for the second model.
"""

model_errors = model_test_predictions - model_output
RSS2 = (model_errors*model_errors).sum()
print('RSS for the 2nd model : ',RSS2)

"""#19. **Quiz Question:** Which model (1 or 2) has lowest RSS on all of the TEST data?
model 2
"""

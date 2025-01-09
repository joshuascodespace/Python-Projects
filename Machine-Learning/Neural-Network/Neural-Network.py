# NN to recognize hand-written digits using the MNIST data
import numpy as np
import random

output_file_name = "NN-Output.txt"
output_file_handler = open(output_file_name, 'w')

# read the MNIST data
testx = np.loadtxt("testx.csv", delimiter=',', dtype=int)
testy = np.loadtxt("testy.csv", delimiter=',', dtype=int)
trainx = np.loadtxt("trainx.csv", delimiter=',', dtype=int)
trainy = np.loadtxt("trainy.csv", delimiter=',', dtype=int)

L = 3                 # number of layers including input and output
sizes = [784, 30, 10] # number of neurons in each layer

# the activation function
def f(z):
    return 1/(1 + np.exp(-z))      # sigmoid activation

def fprime(z):
    return f(z) * (1-f(z))

# convert a digit d to a 10-element vector
# e.g. 6 is converted to [0,0,0,0,0,0,1,0,0,0]
def digit2vector(d):
    return 1*(range(10) == d) # 1 if range digit equals d; 0 otherwise.
    

# a feedforward function that returns the activations
# from each layer and the weighted inputs to each layer
# so that they can be used during backpropagation.
# W,b contain the weights, biases in the network.
# x is the input of a single training example (a vector of length 784).
def feedforward(W, b, x):
    a = [ x, 
          np.zeros(sizes[1]),   # layer 2
          np.zeros(sizes[2]) ]   # layer 3
    z = [ x, 
          np.zeros(sizes[1]),   # layer 2
          np.zeros(sizes[2]) ]   # layer 3
    
    for i in range(1, len(a)):
        z[i] = W[i-1] @ a[i-1] + b[i-1]
        a[i] = f(z[i])
    return a, z

# given an input vector, return the predicted digit
def classify(W, b, x):
    a, z = feedforward(W, b, x)
    return np.argmax(a[L-1])


# helper function for backprop().
# this function computes the error for a single training example.
# W contains the weights in the network.
# a contains the activations.
# z contains the weighted inputs.
# y is the correct digit.
# returns δ = the error. the size of δ is [ 784, 30, 10 ]
def compute_error(W, a, z, y):
    δ = [ np.zeros(sizes[0]), np.zeros(sizes[1]), np.zeros(sizes[2]) ]
    # note that δ[1] is junk. we put it there so that the indices make sense.

    # at the output layer L
    δ[2] = -(digit2vector(y) - a[2]) * fprime(z[2])

    # for each earlier layer L-1,L-2,..,2 (for the HW, this means only layer 2)
    δ[1] = W[1].T @ δ[2] * fprime(z[1])

    return δ


# helper function for backprop(). given the errors δ and the
# activations a for a single training example, this function returns
# the gradient components ∇W and ∇b.
# this function implements teh equations BP3 and BP4.
def compute_gradients(δ, a):
    nablaW = [ np.zeros((sizes[1], sizes[0])),  # layer 1 to 2
          np.zeros((sizes[2], sizes[1])) ] # layer 2 to 3
    nablab = [ np.zeros(sizes[1]),   # layer 2
          np.zeros(sizes[2]) ]   # layer 3 
    for i in range(len(δ)-1):
        nablaW[i] = np.outer(δ[i+1], a[i].flatten())
        nablab[i] = δ[i+1]
    
    return nablaW, nablab


# backpropagation. returns ∇W and ∇b for a single training example.
def backprop(W, b, x, y):
    a, z = feedforward(W, b, x)
    δ = compute_error(W, a, z, y)
    nablaW, nablab = compute_gradients(δ, a)
    return nablaW, nablab


# gradient descent algorithm.
# W = weights in the network
# b = biases in the network
# batch = the indices of the observations in the batch, i.e. the rows of trainx
# α = step size
# λ = regularization parameter
def GD(W, b, batch, α=0.01, λ=0.01):
    m = len(batch)    # batch size

    # data structure to accumulate the sum over the batch.
    # in the lecture notes as well as Ng's article, sumW is ΔW and sumb is Δb.
    sumW = [ np.zeros((sizes[1], sizes[0])),
             np.zeros((sizes[2], sizes[1])) ]
    sumb = [ np.zeros(sizes[1]), np.zeros(sizes[2]) ]
    nablaW = [ np.zeros((sizes[1], sizes[0])),  # layer 1 to 2
          np.zeros((sizes[2], sizes[1])) ] # layer 2 to 3
    nablab = [ np.zeros(sizes[1]),   # layer 2
          np.zeros(sizes[2]) ]   # layer 3

    m = len(batch)
    for i in batch:
        nablaW_i, nablab_i = backprop(W, b, trainx[i,:], trainy[i])
        for layer in range(L-1):
            sumW[layer] += nablaW_i[layer]
            sumb[layer] += nablab_i[layer]

    for layer in range(L-1):
        nablaW[layer] = ((1/m) * sumW[layer] + λ * W[layer])
        nablab[layer] = (1/m) * sumb[layer]
        W[layer] -= α * nablaW[layer]
        b[layer] -= α * nablab[layer]
    # for each training example in the batch, use backprop
    # to compute the gradients and add them to the sum


    # make the update to the weights and biases and take a step
    # of gradient descent. note that we use the average gradient.

    # return the updated weights and biases. we also return the gradients
    return W, b, nablaW, nablab


# classify the test data and compute the classification accuracy
def accuracy(W, b):
    ntest = len(testy)
    yhat = np.zeros(ntest, dtype=int)
    for i in range(ntest):
        yhat[i] = classify(W, b, testx[i,:])
    return sum(testy == yhat)/ntest # hit rate

# train the neural network using batch gradient descent.
# this is a driver function to repeatedly call GD().
# N = number of observations in the training data.
# m = batch size
# α = learning rate (i.e. step size)
# λ = regularization parameter
def BGD(N, m, epochs, α=0.01, λ=0.01):
    # random initialization of the weights and biases
    W = [ np.random.normal(0, 1, (sizes[1], sizes[0])), 
          np.random.normal(0, 1, (sizes[2], sizes[1])) ]
    b = [ np.random.normal(0, 1, sizes[1]),
          np.random.normal(0, 1, sizes[2]) ]
    nablaW = [ np.zeros((sizes[1], sizes[0])),  # layer 1 to 2
          np.zeros((sizes[2], sizes[1])) ] # layer 2 to 3
    nablab = [ np.zeros(sizes[1]),   # layer 2
          np.zeros(sizes[2]) ]   # layer 3

    for j in range(epochs):
        batch_options = list(range(N))
        random.shuffle(batch_options)
        # List contains all numbers between 0 and N exactly once in random order
        for index in range(0, N, m):
            batch = batch_options[index:index+m]
            W, b, nablaW, nablab = GD(W, b, batch)
        print("epoch", j + 1, "is done. Accuracy =", accuracy(W, b), file=output_file_handler)
    # print out messages to monitor the progress of the
    # training. for example, you could print the epoch number and the
    # accuracy after completion of each epoch.
    
    return W, b, nablaW, nablab

# some tuning parameters
N = len(trainy)
m = 25       # batch size
epochs = 30 # Set to 30 after testing # number of complete passes through the training data
α = 0.01     # learning rate / step size
λ = 0.01     # regularization parameter
W, b, nablaW, nablab = BGD(N, m, epochs, α=α, λ=λ)



















# Finite-difference gradient approximation. NOTE! Be sure
# to source the functions for problem 3 before running this code!

# unroll the weights and biases into a single vector.
# note this function will also work for unrolling the gradient.
# note that this is hard-coded for a 3-layer NN.
def unroll(W, b):
    return np.concatenate((W[0].flatten(order='C'), W[1].flatten(order='C'), b[0], b[1]))

# given a single vector θ, reshape the parameters into the data
# structures that are used for backpropagation, that is, W and b, or
# ∇w and ∇b.  note that this is hard-coded for a 3-layer NN.
def reshape_params(θ):
    n1 = sizes[0]  # number of nodes in layer 1
    n2 = sizes[1]  # number of nodes in layer 2
    n3 = sizes[2]
    W1 = θ[0:(n2*n1)].reshape((n2, n1))
    W2 = θ[(n2*n1):(n2*n1 + n2*n3)].reshape((n3, n2))
    b1 = θ[(n2*n1 + n2*n3):(n2*n1 + n2*n3 + n2)]
    b2 = θ[(n2*n1 + n2*n3 + n2):len(θ)]
    W = [ W1, W2 ]
    b = [ b1, b2 ]
    return W, b

# evaluate the cost function for a batch of training examples
# θ is the unrolled vector of weights and biases.
# batch is the set of indices of the batch of training examples.
def J(θ, batch, λ):

    # THIS FUNCTION IS INCOMPLETE.
    
    m = len(batch)
    sumJ = 0.0  # to accumulate the sum for the batch.
    # we need to pass W, b to feedforward, so we re-create W, b from θ
    W, b = reshape_params(θ)
    for i in batch:

        # grab training example i
        x_i = trainx[i,:]
        y_i = trainy[i]

        # feedforward to obtain a, z
        a, z = feedforward(W, b, x_i)
        # accumulate the cost function 
        sumJ += sum((a[2] - digit2vector(y_i))**2)
    

    # return the cost. note that the regularization term only
    # applies to the weights, not the biases
    sum_over_all_W = sum([np.sum(w_matrix**2) for w_matrix in W])
    
    return sumJ / (2 * m) + λ * sum_over_all_W / 2
    


# create the ith basis vector
def e(i):
    e = np.zeros(sizes[1]*sizes[0] + sizes[2]*sizes[1] + sizes[1] + sizes[2])
    e[i] = 1
    return e

def θplus(v, i, ϵ=1e-4):
    return v + ϵ*e(i)

def θminus(v, i, ϵ=1e-4): 
    return v - ϵ*e(i)

# compute the difference between the ith element of the gradient as
# computed from backpropagation (this is ∇θ[i]) and the approximation of
# the ith element of the gradient as obtained from finite differencing.
# the idea is to see if the backpropagation code is correctly computing
# the gradient of the cost function.
def compare1(i, θ, nablaθ, batch, λ, ϵ=1e-4):
    # i is the index for the ith element of the unrolled gradient θ,
    return nablaθ[i] - ( J(θplus(θ, i, ϵ=ϵ), batch, λ) - J(θminus(θ, i, ϵ=ϵ), batch, λ) )/(2*ϵ)

# compare each element of the gradient as computed from
# backpropagation to its estimate as obtained from finite
# differencing.
def compare(W, b, nablaW, nablab, λ):
    θ = unroll(W, b)
    nablaθ = unroll(nablaW, nablab)
    m = len(trainy)

    # create a batch of 5000 training examples to evaluate the cost function.
    # we really just need the indices of the batch.
    batch = list(range(m))
    random.shuffle(batch)
    batch = batch[0:5000] 

    W, b, nablaW, nablab = GD(W, b, batch)
    nablaθ = unroll(nablaW, nablab)
    θ = unroll(W, b)

    # random sample of 200 gradient components to check
    grad_component = list(range(sizes[0]*sizes[1]+sizes[1]*sizes[2]+sizes[1]+sizes[2]))
    random.shuffle(grad_component)
    grad_component = grad_component[0:200]

    count = 0
    for component in grad_component:
        finite_difference = compare1(component, θ, nablaθ, batch, λ)
        if np.abs(finite_difference) > 0.001:
            count += 1
            print("Oh No! Your gradient component's finite differencing exceeding the threshhold!!", finite_difference, ">", 0.001, file=output_file_handler)
    print("Your weights failed the finite differencing", count, "times.", file=output_file_handler)
        

# Note: W, b, ∇W, ∇b have been already been
# computed. Use your code from earlier to do this.
# λ should be same as the λ that was used for problem 3.
compare(W, b, nablaW, nablab, λ)

output_file_handler.close()
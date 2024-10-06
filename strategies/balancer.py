import numpy as np
import pandas as pd
from scipy.optimize import minimize

def optimize_scipy(Q, m, x0):
    # Q is the cov matrix
    # m is the vector of mean returns
    # x0 is the weights in array
    def objective(x):
        return x.T @ Q @ x

    # m.dot(x) = 1
    def constraint_return(x):
        return np.dot(m, x) - 1

    # weights sum to 1
    def constraint_sum(x):
        return np.sum(x) - 1

    # Constraints in the form {'type': 'eq', 'fun': constraint_function}
    constraints = [{'type': 'eq', 'fun': constraint_return},
                   {'type': 'eq', 'fun': constraint_sum}]

    bounds = [(0, 1), (0, 1)]

    # Perform the optimization
    result = minimize(objective, x0, bounds=bounds, constraints=constraints, method='SLSQP')

    return result.x

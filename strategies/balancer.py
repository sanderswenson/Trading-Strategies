import numpy as np
import pandas as pd
from scipy.optimize import minimize, Bounds

class Balancer:
    def __init__(self):
        pass

    def minimize_sharpe(date, portfolio, data):
        # input portfolio as value
        # data must have dates in first column
        # TODO: implement for pandas dataframes

        p = portfolio
        x0 = np.array([(xi / np.sum(p)) for xi in p])
        data_matrix = data.loc[:date].to_numpy()
        Q = np.cov(data_matrix.T)
        m = np.array([np.mean(np.diff(data_matrix,axis=0), axis=0)])

        # TODO: change fixed r_f to variable over period

        m_car = m - np.array([.02, .02, .02])

        def objective_sharpe(x):
            # function to minimize
            return (x.dot(Q)).dot(x.T)

        # Constraints (if any)
        # TODO: Add constraint matrix and jac if possible
        eq_cons   = {'type': 'eq',
                     'fun' : lambda w: np.array([m_car.dot(w) - 1,
                                                 np.sum(w) - 1]),
                     'jac' : lambda w: np.array([np.sum(m_car),
                                                 3.0])}
        
        ineq_cons = {'type': 'ineq',
                     'fun' : lambda w: np.sum(w),
                     'jac' : lambda w: np.array([3.0])}

        # Bounds for variables (if any)
        bounds = Bounds([0,0,0], [1,1,1])  # Example: variables between 0 and 1

        # Perform the minimization
        result = minimize(
            objective_sharpe,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=[eq_cons, ineq_cons]
        )

        return result.x

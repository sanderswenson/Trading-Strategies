import numpy as np
from scipy.optimize import minimize, Bounds

class Balancer:
    def __init__(self):
        pass

    def minimize_sharpe(self, data_matrix):
        # data_matrix must have portfolio in column 1, and assets in 2-4
        # TODO: implement for pandas dataframes
        # Define the objective sharpe to minimize

        p = data_matrix[:,1]
        x0 = np.array([(xi / np.sum(p)) for xi in p[i]]
                     for i in range(0,p.shape[0]))
        Q = np.cov([data_matrix[:,2], data_matrix[:,3], data_matrix[:,4]])
        m = np.array([np.average(data_matrix[i,j] - data_matrix[i-1]
                                 for i in range(1,data_matrix.shape[0]))
                      for j in [2,3,4]])
        
        # TODO: change fixed r_f to variable over period

        m_car = m - np.array([.02, .02, .02])

        def objective_sharpe(x):
            # function to minimize
            return x.T.dot(Q).dot(x)

        # Constraints (if any)
        # TODO: Add constraint matrix and jac if possible
        eq_cons   = {'type': 'eq',
                     'fun' : lambda w: m_car.dot(w) - 1}
        
        ineq_cons = {'type': 'ineq',
                     'fun' : lambda w: np.sum(w)}

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

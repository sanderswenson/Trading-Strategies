import numpy as np
from scipy.optimize import minimize

class Balancer:
    def __init__(self):
        pass

    def minimize_sharpe(self, initial_guess, data_matrix):
        # data_matrix must have portfolio in column 1, and assets in 2-4
        # TODO: implement for pandas dataframes
        # Define the objective sharpe to minimize
        def objective_sharpe(data_matrix):
            p = data_matrix[:,1]
            x = np.array([(xi / np.sum(p)) for xi in p])
            Q = np.cov([data_matrix[:,2], data_matrix[:,3], data_matrix[:,4]])
            # function to minimize
            return x.T.dot(Q).dot(x)

        # Constraints (if any)
        constraints = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Example: weights sum to 1
        )

        # Bounds for variables (if any)
        bounds = ((0, 1), (0, 1), (0, 1))  # Example: variables between 0 and 1

        # Perform the minimization
        result = minimize(
            objective_sharpe,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        return result.x

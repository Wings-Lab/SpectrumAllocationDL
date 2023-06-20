function J = linearCostFunction(X, y, theta, fp_penalty_coef, fn_penalty_coef)
%COMPUTECOSTMULTI Compute cost for linear regression with multiple variables
%   J = COMPUTECOSTMULTI(X, y, theta) computes the cost of using theta as the
%   parameter for linear regression to fit the data points in X and y

% Initialize some useful values
m = length(y); % number of training examples
fp_fn_vec = ones(size(y)) * fn_penalty_coef;

y_pred = X * theta;
fp_fn_vec(y_pred > y) = fp_penalty_coef;
J = 1 / (2 * m) * (y_pred - y)' * ((y_pred - y).*fp_fn_vec);

% =========================================================================

end

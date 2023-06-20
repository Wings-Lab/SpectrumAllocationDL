function [J, grad] = costFunction(X, y, theta, lambda, fp_coef, fn_coef)
%COSTFUNCTION Compute cost and gradient for logistic regression
%   J = COSTFUNCTION(theta, X, y) computes the cost of using theta as the
%   parameter for logistic regression and the gradient of the cost
%   w.r.t. to the parameters.

% Initialize some useful values
m = length(y); % number of training examples
n = length(theta);
fp_fn_vec = ones(size(y))*fn_coef;

% You need to return the following variables correctly 
J = 0; 
grad = zeros(size(theta));

% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta
%
% Note: grad should have the same dimensions as theta
%
y_pred = sigmoid(X * theta);
lg_y_pred = log(y_pred);
lg_y_pred(lg_y_pred == -inf) = realmin;
one_minus_lg = log(1 - y_pred);
one_minus_lg(one_minus_lg == -inf) = realmin;
J = sum(-fn_coef*y.*lg_y_pred - fp_coef*(1 - y).*one_minus_lg)/m + ...
    lambda * sum(theta(2:n).^2)/(2*m);

fp_fn_vec(y_pred>y) = fp_coef;
grad(1) = sum((y_pred - y).*X(:,1).*fp_fn_vec)/m;

for i = 2 : n
  grad(i) = sum((y_pred - y).*X(:,i).*fp_fn_vec)/m + lambda * theta(i)/m;
end







% =============================================================

end

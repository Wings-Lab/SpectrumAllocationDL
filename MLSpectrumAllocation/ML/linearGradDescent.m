function [theta, J_history] = linearGradDescent(X, y, theta, alpha, num_iters, fp_penalty_coef, fn_penalty_coef)
%GRADIENTDESCENTMULTI Performs gradient descent to learn theta
%   theta = GRADIENTDESCENTMULTI(x, y, theta, alpha, num_iters) updates theta by
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
m = length(y); % number of training examples
J_history = zeros(num_iters, 1);
n = length(theta);
temp = zeros(size(theta));

for iter = 1:num_iters
    fp_fn_vec = ones(size(y)) * fn_penalty_coef;
    fp_fn_vec(X * theta > y) = fp_penalty_coef;
    for j = 1 : n
      temp(j) = theta(j) - alpha/m * sum((X * theta - y).*X(:,j).*fp_fn_vec);
    end 
    theta = temp;




    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = linearCostFunction(X, y, theta, fp_penalty_coef, fn_penalty_coef);

end

end

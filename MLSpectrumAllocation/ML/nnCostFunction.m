function [J, grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda, fp_penalty_coef, fn_penalty_coef)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
dim = [hidden_layer_size(1) * (input_layer_size + 1), ...
    hidden_layer_size(2) * (hidden_layer_size(1) + 1)];
Theta1 = reshape(nn_params(1:dim(1)), ...
                 hidden_layer_size(1), (input_layer_size + 1));

Theta2 = reshape(nn_params(1 + dim(1): dim(1) + dim(2)), ...
                 hidden_layer_size(2), (hidden_layer_size(1) + 1));

Theta3 = reshape(nn_params(1 + dim(1) + dim(2):end), ...
                 num_labels, (hidden_layer_size(2) + 1));

% Setup some useful variables
m = size(X, 1); 
         
% You need to return the following variables correctly 
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));
Theta3_grad = zeros(size(Theta3));

X =  [ones(m,1) X];


%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. 
Z2 = X * Theta1';
A2 = sigmoid(Z2);
m2 = size(A2, 1);
A2 = [ones(m2,1) A2];

Z3 = A2 * Theta2';
A3 = sigmoid(Z3);
m3 = size(A3, 1);
A3 = [ones(m3, 1) A3];

HX = sigmoid(A3*Theta3');
J = 0;
%for i=1:m 
%  J = J - sum(log(HX(i,:)) .* y_eye(y(i), :) + ...
%  (1 - y_eye(y(i), :)) .* log(1 - HX(i,:)));
%endfor
J = -sum(sum(log(HX) .* y * fn_penalty_coef + ...
  (1 - y) .* log(1 - HX)*fp_penalty_coef));
J = J + (sum(sum(Theta1(:, 2:end).^2))...
  + sum(sum(Theta2(:, 2:end).^2)) + sum(sum(Theta3(:, 2:end).^2)))*lambda/2;
J = J / m; 

%
% Part 2: Implement the backpropagation algorithm to compute the gradients
%         Theta1_grad and Theta2_grad and Theta3_grad. You should return the partial derivatives of
%         the cost function with respect to Theta1 and Theta2 in Theta1_grad and
%         Theta2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a 
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the 
%               first time.
fp_fn_vec = ones(size(y))*fn_penalty_coef;  % This is a vector for having differnet penalty for fp and fn
fp_fn_vec(HX>y) = fp_penalty_coef;
Delta4 = (HX - y).*fp_fn_vec;

% for i=1:m
%   delta4 = Delta4(i,:);
%   a3 = A3(i,:);
%   Theta3_grad = Theta3_grad + delta4' * a3;
% end
Theta3_grad = Delta4' * A3;
Theta3_grad = Theta3_grad/m;
Delta3 = Delta4 * Theta3 ;
Delta3 = Delta3(:, 2:end) .* sigmoidGradient(Z3);

% for i=1:m
%   delta3 = Delta3(i,:);
%   a2 = A2(i,:);
%   Theta2_grad = Theta2_grad + delta3' * a2;
% end
Theta2_grad = Delta3' * A2;
Theta2_grad = Theta2_grad/m;
Delta2 = Delta3 * Theta2 ;
Delta2 = Delta2(:, 2:end) .* sigmoidGradient(Z2);

% for i=1:m
%   delta2 = Delta2(i,:);
%   a1 = X(i,:);
%   Theta1_grad = Theta1_grad + delta2' * a1;
% end
Theta1_grad = Delta2' * X;
Theta1_grad = Theta1_grad / m;

%
% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to Theta1_grad
%               and Theta2_grad from Part 2.
%
  
LAMBDA = ones(size(Theta1_grad))*lambda/m;
LAMBDA(:,1) = 0;
Theta1_grad = Theta1_grad + Theta1.*LAMBDA;

LAMBDA = ones(size(Theta2_grad))*lambda/m;
LAMBDA(:,1) = 0;
Theta2_grad = Theta2_grad + Theta2.*LAMBDA;

LAMBDA = ones(size(Theta3_grad))*lambda/m;
LAMBDA(:,1) = 0;
Theta3_grad = Theta3_grad + Theta3.*LAMBDA;







% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:); Theta3_grad(:)];


end

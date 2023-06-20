function [error_train, error_val, mvec] = ...
    learningCurve(X, y, Xval, yval, lambda)
%LEARNINGCURVE Generates the train and cross validation set errors needed 
%to plot a learning curve
%   [error_train, error_val] = ...
%       LEARNINGCURVE(X, y, Xval, yval, lambda) returns the train and
%       cross validation set errors for a learning curve. In particular, 
%       it returns two vectors of the same length - error_train and 
%       error_val. Then, error_train(i) contains the training error for
%       i examples (and similarly for error_val(i)).
%
%   In this function, you will compute the train and test errors for
%   dataset sizes from 1 up to m. In practice, when working with larger
%   datasets, you might want to do this in larger intervals.
%

% Number of training examples
m = size(X, 1);
mvec = 1:2000:m;

% You need to return these values correctly
error_train = zeros(length(mvec), 1);
error_val   = zeros(length(mvec), 1);

% Note: You should evaluate the training error on the first i training
%       examples (i.e., X(1:i, :) and y(1:i)).
%
%       For the cross-validation error, you should instead evaluate on
%       the _entire_ cross validation set (Xval and yval).
%
% Note: If you are using your cost function (linearRegCostFunction)
%       to compute the training and cross validation error, you should 
%       call the function with the lambda argument set to 0. 
%       Do note that you will still need to use lambda when running
%       the training to obtain the theta parameters.
%

% ---------------------- Sample Solution ----------------------
for i = 1:length(mvec)
    theta = trainLogisticReg(X(1:mvec(i), :), y(1:mvec(i)), 0); 
    error_train(i) = logisticCostFunction(X(1:mvec(i), :), y(1:mvec(i)), ...
        theta, lambda);
    error_val(i) = logisticCostFunction(Xval, yval, theta, 0);
end






% -------------------------------------------------------------

% =========================================================================

end

function [Xtrain, ytrain, Xval, yval, Xtest, ytest, test_idx] = splittingData(X, y)
  [m n] = size(X);
%   train_size = 0.6;
%   val_size = 0.2;
  train_size = 0.1064;
  val_size = 0.0425;
  
  Xtrain = X(1:round(m*train_size), :);
  ytrain = y(1:round(m*train_size));
  
  Xval = X(round(m*train_size)+1:round(m*train_size) + round(m*val_size), :);
  yval = y(round(m*train_size)+1:round(m*train_size) + round(m*val_size));
  
  Xtest = X(round(m*train_size) + round(m*val_size) + 1:end, :);
  ytest = y(round(m*train_size) + round(m*val_size) + 1:end);
  test_idx = round(m*train_size) + round(m*val_size) + 1;
end

function d = choosePoly(Xtrain, ytrain, Xval, yval)
  n = size(Xtrain, 2);
  error_train = zeros(n-4, 1);
  error_val   = zeros(n-4, 1);
  accuracy_val = zeros(n-4, 1);
  fscore_val = zeros(n-4, 1);
  for i = 5:n
    theta = trainLogisticReg(Xtrain(:,1:i), ytrain, 0); 
    error_train(i-4) = logisticCostFunction(Xtrain(:,1:i), ytrain, theta, 0);
    error_val(i-4) = logisticCostFunction(Xval(:, 1:i), yval, theta, 0);
    ypred_val = predict(theta, Xval(:, 1:i), 0.5); 
    [accuracy_val(i-4), fscore_val(i-4)] = errorAnalysis(yval, ypred_val);
  end
  [~, d] = min(error_val);
  d = d + 4;
end

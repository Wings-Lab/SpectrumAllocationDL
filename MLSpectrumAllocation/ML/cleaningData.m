function [X_norm, mu, sigma] = cleaningData(X)
%  # normalizing data
%  # [m n] = size(X);
%  # for i = 1 : n
%  #   X(:, i) = (X(:, i) - mean(X(:, i))) / std(X(:, i));
%  # endfor
  
  mu = mean(X);
  X_norm = bsxfun(@minus, X, mu);

  sigma = std(X_norm);
  X_norm = bsxfun(@rdivide, X_norm, sigma);

end

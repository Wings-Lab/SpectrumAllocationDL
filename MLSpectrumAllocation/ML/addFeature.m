function X = addFeature(X)
  % creating more polynomial features
  [m, n] = size(X);
  if n <= 3
      d = 2; % maximum number; should be written automatically
      X = [X(:,1:end-1), X(:,1).^2, X(:,2).^2, X(:,1).*X(:,2),X(:,1).*X(:,2).^2,...
          X(:,2).*X(:,1).^2, X(:,end)];
      X = [X(:,1:end-1), (X(:,1).^2).*(X(:,2).^2), (X(:,1).^3).*(X(:,2)),...
          (X(:,1).^3).*(X(:,2).^2), (X(:,1).^3).*(X(:,2).^3),...
          (X(:,1).^2).*(X(:,2).^3),  X(:,1).*X(:,2).^3, X(:,end)];
  end
end

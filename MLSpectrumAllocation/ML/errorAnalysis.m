function [accuracy, f_score, tp, fp, fn, tn] = errorAnalysis(y, y_pred)
  accuracy = 1 - sum(abs(y - y_pred))/size(y, 1);
  p_ind = y==1;
  tp = sum(y_pred(p_ind));
  fp = sum(y_pred) - tp; 
  fn = sum(y) - tp;
  tn = length(y) - tp - fn - fp;
  p = tp/(tp + fp); % precision
  r = tp/(tp + fn); % recall
  f_score = 2 * p * r / (p + r);
end

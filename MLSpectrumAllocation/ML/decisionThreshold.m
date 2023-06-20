function thr = decisionThreshold(Xval, yval, theta, metric)
  thresholdVec = [0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9];
  l = size(thresholdVec, 2);
  accuracy = zeros(l ,1);
  fscore = zeros(l, 1);
  tp = zeros(l, 1);
  fp = zeros(l, 1);
  for i = 1:l
    ypred = predict(theta, Xval, thresholdVec(i));
    [accuracy(i), fscore(i), tp(i), fp(i)] = errorAnalysis(yval, ypred);
  end
  if metric == "accuracy" 
      [best_metric, ind] = max(accuracy); % best accuracy to choose threshold
  elseif metric == "min_fp"
      [best_metric, ind] = min(fp); % best accuracy to choose threshold
  end
  
  thr = thresholdVec(ind);
  threshold_dyn_vec = max(0, thr - 0.05):0.01:min(1, thr + 0.05);
        for j = 1:length(threshold_dyn_vec)
            threshold = threshold_dyn_vec(j);
            pred = predict(theta, Xval, threshold);
            [accuracy, ~, ~, fp] = errorAnalysis(yval, pred);
            if metric == "accuracy"
                if accuracy > best_metric
                    best_metric = accuracy;
                    thr = threshold;
                end
            elseif metric == "min_fp"
                if fp < best_metric
                    best_metric = fp;
                    thr = threshold;
                end
            end
        end
  end

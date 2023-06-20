
%% Initialization
clear ; close all; clc

%% Load Data
%  The first two columns contains the exam scores and the third column
%  contains the label.
data = load('data\dynamic_pus_using_pus50000_15PUs_201910_2616_25.txt');
[m, n] = size(data);

 % splitting data
number_of_samples = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150,...
    200, 250, 300, 400, 500, 700 1000:1000:4001];
% number_of_samples = [5000];
metric = "min_fp";  %{'min_fp', 'accuarcy'}
fp_coef = 1000;
fn_coef = 1;
% metric = "min_fp";

MAX_POWER = true;
if MAX_POWER
    data_max = load('data\dynamic_pus_max_power50000_15PUs_201910_2616_25.txt');
    new_data = [data data_max];
    new_data(new_data(:, end)==-Inf, :) = [];
    data = new_data(:, 1:n);
    data_max = new_data(:, n+1:end);
    average_diff_power = zeros(1, length(number_of_samples));
    max_diff_power = zeros(1, length(number_of_samples));
    fp_num = zeros(1, length(number_of_samples));
    fp_mean = zeros(1, length(number_of_samples));
end

X = data(:, 1:n-1); y = data(:, n);
accuracy_test = zeros(1, length(number_of_samples));
fscore_test = zeros(1, length(number_of_samples));
tp = zeros(1, length(number_of_samples));
fp = zeros(1, length(number_of_samples));
fn = zeros(1, length(number_of_samples));
tn = zeros(1, length(number_of_samples));
test_samples = 1300;
for j = 1:length(number_of_samples)
    fprintf("\n ****** Samples: %d **********", number_of_samples(j));
    [Xtrain, ytrain, Xval, yval, Xtest, ytest, test_start_idx] = splittingData(X, y);
    Xtrain = Xtrain(1:number_of_samples(j), :);
    ytrain = ytrain(1:number_of_samples(j));
    
    Xval = Xval(1:max(2, round(number_of_samples(j)/3)), :);
    yval = yval(1:max(2, round(number_of_samples(j)/3)), :);
    
    % Training data, add feature and normalize
    Xtrain_p = addFeature(Xtrain);                          % add poly feature
    [Xtrain_pn, mu, sigma] = cleaningData(Xtrain_p);        % normalize
    Xtrain_pn = [ones(size(Xtrain_pn, 1), 1), Xtrain_pn];  % Add Ones

    % validation data, add feature and normalize
    Xval_p = addFeature(Xval);
    Xval_pn = bsxfun(@minus, Xval_p, mu);
    Xval_pn = bsxfun(@rdivide, Xval_pn, sigma);
    Xval_pn = [ones(size(Xval_pn, 1), 1), Xval_pn];           % Add Ones

    % test data, add feature and normalize
    Xtest_p = addFeature(Xtest);
    Xtest_pn = bsxfun(@minus, Xtest_p, mu);
    Xtest_pn = bsxfun(@rdivide, Xtest_pn, sigma);
    Xtest_pn = [ones(size(Xtest_pn, 1), 1), Xtest_pn];           % Add Ones

    % Initialize fitting parameters
    % initial_theta = zeros(n + 1, 1);

    %% ============= Part 2: Optimizing using fminunc  =============
    %  In this exercise, you will use a built-in function (fminunc) to find the
    %  optimal parameters theta.

    %  Set options for fminunc
%     d = choosePoly(Xtrain_pn, ytrain, Xval_pn, yval);

    % Xtrain_pn = Xtrain_pn(:, 1:d);
    % Xval_pn = Xval_pn(:, 1:d);
    % Xtest_pn = Xtest_pn(:, 1:d);

    %%%% choose best lambda
    [lambda_vec, error_train, error_val, best_theta] = ...
        validationCurve(Xtrain_pn, ytrain, Xval_pn, yval, fp_coef, fn_coef);

    % decide what threshold is better
    threshold = decisionThreshold(Xval_pn, yval, best_theta, metric);


    %% ============= Part 3: Predicting Test =============
    % Compute accuracy on our test set 
    yp_test = predict(best_theta, Xtest_pn, threshold);
    [accuracy_test(j), fscore_test(j), tp(j), fp(j), fn(j), tn(j)] = ...
        errorAnalysis(ytest, yp_test);
    
    if MAX_POWER
        ypower_test_gt = data_max(test_start_idx:end, size(data_max, 2));
        ypower_test_predicted = zeros(size(ypower_test_gt));
        max_power = max(ypower_test_gt) + 10;  % 50 is added to increase higher bound
        min_power = min(ypower_test_gt) - 10;  % 50 is subtracted to decrease lower bound
        for p=1:length(ytest)
            h = max_power;
            l = min_power;
            while h - l > 0.5
               mid = l + (h - l)/2;
               mid_norm = bsxfun(@minus, mid, mu(end));
               mid_norm = bsxfun(@rdivide, mid_norm, sigma(end));
               res_tmp = predict(best_theta, [Xtest_pn(p, 1:end-1), mid_norm], threshold);  % replace su real power with mid
               if res_tmp
                   l = mid;
               else
                   h = mid;
               end
            end
            ypower_test_predicted(p) = l + (h - l)/2;
        end
        average_diff_power(j) = round(mean(abs(ypower_test_gt - ypower_test_predicted)), 3);
        max_diff_power(j) = round(max(abs(ypower_test_gt - ypower_test_predicted)), 3);
        fp_num(j) = sum(ypower_test_predicted > ypower_test_gt);
        fp_mean(j) = round(mean((ypower_test_predicted - ypower_test_gt).*(ypower_test_predicted>ypower_test_gt)), 3);
    end
end




%% Initialization
clear ; close all; clc

%% Load Data
% TODO: regularization not being implemented
data = load('data\dynamic_pus_using_pus50000_15PUs_201910_2616_25.txt');
data_max = load('data\dynamic_pus_max_power50000_15PUs_201910_2616_25.txt');
[m, n] = size(data);
% 
data = [data(:, 1:end-2) data_max(:, end)];
data(data(:, end)==-Inf, :) = [];


  % bumber of training samples as the outer loop
number_of_samples = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150,...
    200, 250, 300, 400, 500, 700 1000:1000:4001];
% number_of_samples = [10];


X = data(:, 1:size(data,2)-1); y = data(:, size(data,2));
clear data data_max
% load('tmp_var.mat')

average_diff_power = zeros(1, length(number_of_samples));
fp_mean = zeros(1, length(number_of_samples));
max_diff_power = zeros(1, length(number_of_samples));
J_training = zeros(1, length(number_of_samples));
J_test = zeros(1, length(number_of_samples));
J_val = zeros(1, length(number_of_samples));

alpha = 0.01;
num_iters = 400;   % number of iterations for training theta
fp_penalty_coef = 10;
fn_penalty_coef = 1;

for j = 1:length(number_of_samples)
    fprintf("\n ****** Samples: %d **********", number_of_samples(j));
    [Xtrain, ytrain, Xval, yval, Xtest, ytest, test_start_idx] = splittingData(X, y);
    Xtrain = Xtrain(1:number_of_samples(j), :);
    ytrain = ytrain(1:number_of_samples(j));
    
    Xval = Xval(1:max(2, round(number_of_samples(j)/3)), :);
    yval = yval(1:max(2, round(number_of_samples(j)/3)), :);
    
    % Training data, add feature and normalize
    Xtrain = addFeature(Xtrain);                          % add poly feature
    [Xtrain, mu, sigma] = cleaningData(Xtrain);        % normalize
    Xtrain = [ones(size(Xtrain, 1), 1), Xtrain];  % Add Ones

    % validation data, add feature and normalize
    Xval = addFeature(Xval);
    Xval = bsxfun(@minus, Xval, mu);
    Xval = bsxfun(@rdivide, Xval, sigma);
    Xval = [ones(size(Xval, 1), 1), Xval];           % Add Ones

    % test data, add feature and normalize
    Xtest = addFeature(Xtest);
    Xtest = bsxfun(@minus, Xtest, mu);
    Xtest = bsxfun(@rdivide, Xtest, sigma);
    Xtest = [ones(size(Xtest, 1), 1), Xtest];           % Add Ones

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
    theta = ones(size(Xtrain, 2), 1);
    [theta, J_history] = linearGradDescent(Xtrain, ytrain, theta, alpha, num_iters, fp_penalty_coef, fn_penalty_coef);
    
    J_training(j) = J_history(end);
    J_val(j) = linearCostFunction(Xval, yval, theta, fp_penalty_coef, fn_penalty_coef);
    
%     figure;
    plot(1:numel(J_history), J_history, '-b', 'LineWidth', 2);
    xlabel('Number of iterations');
    ylabel('Cost J');
    title('trainig samples: ' + string(number_of_samples(j)));

    %% ============= Part 3: Predicting Test =============
    % Compute accuracy on our test set 
    yp_test = predictLinear(theta, Xtest);
    average_diff_power(j) = round(mean(abs(ytest - yp_test)), 3);
    max_diff_power(j) = round(max(abs(ytest - yp_test)), 3);
    fp_mean(j) = round(mean((yp_test - ytest).*(yp_test > ytest)), 3);
    J_test(j) = linearCostFunction(Xtest, ytest, theta, fp_penalty_coef, fn_penalty_coef);
end

figure;
plot(number_of_samples, J_training, '-', 'LineWidth', 2);
hold on
plot(number_of_samples, J_val, '-', 'LineWidth', 2);
plot(number_of_samples, J_test, '-.', 'LineWidth', 2);
xlabel('Number of training samples');
ylabel('Cost J');
title('Cost function' );
legend('training', 'validation', 'test');
hold off



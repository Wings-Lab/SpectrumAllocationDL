
%% Initialization
clear ; close all; clc

hidden_layer_size = [20, 20];   % two hidden layers each
hidden_layer_size = [7, 7];   % for static pus
num_labels = 1;          % yes/no 
normalize = 1;
%% Load Data
%  The first two columns contains the exam scores and the third column
%  contains the label.
number_of_samples = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 150,...
    200, 250, 300, 400, 500, 700 1000:1000:4001];
% number_of_samples = [5000];
data = load('data\dynamic_pus_using_pus50000_15PUs_201910_2616_25.txt');
[m, n] = size(data);
MAX_POWER = true;
metric = "fp_min";  %{"accuracy", "fp_min"}
fp_penalty_coef = 1000;
fn_penalty_coef = 1;
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
input_layer_size  = n-1;  % 3 inputs for static PUs

lambda_vec = [0 0.001 0.003 0.01 0.03 0.1 0.3 1 3 10 20];
    % lambda_vec = [20 60 200];
    % lambda_vec = 1;
threshold_vec = 0.1:0.1:0.9;
    % threshold_vec = 0.5;

borders = [hidden_layer_size(1) * (input_layer_size + 1), ...
    hidden_layer_size(2) * (hidden_layer_size(1) + 1)];

accuracy_test = zeros(1, length(number_of_samples));
fscore_test = zeros(1, length(number_of_samples));
tp_test = zeros(1, length(number_of_samples));
fp_test = zeros(1, length(number_of_samples));
fn_test = zeros(1, length(number_of_samples));
tn_test = zeros(1, length(number_of_samples));

options = optimset('MaxIter', 150);

for jj = 1:length(number_of_samples)
    [Xtrain, ytrain, Xval, yval, Xtest, ytest, test_start_idx] = ...
        splittingData(X, y);
    Xtrain = Xtrain(1:number_of_samples(jj), :);
    if normalize == 1
        [Xtrain, mu, sigma] = cleaningData(Xtrain);        % normalize
    end
    ytrain = ytrain(1:number_of_samples(jj));
    
    fprintf("\n number of trainig samples: %d", number_of_samples(jj));
    fprintf("\n number of samples equal to 1: %d", sum(ytrain));
    Xval = Xval(1:max(2, round(number_of_samples(jj)/3)), :);
    if normalize == 1
        Xval = bsxfun(@minus, Xval, mu);
        Xval = bsxfun(@rdivide, Xval, sigma);
    end
    yval = yval(1:max(2, round(number_of_samples(jj)/3)), :);
    

    %% ================ Part 2: Initializing Parameters ================
    %  Weights should be randomly intialized to avoid Symmetry breaking

    initial_Theta1 = randInitializeWeights(input_layer_size, ...
        hidden_layer_size(1));
    initial_Theta2 = randInitializeWeights(hidden_layer_size(1), ...
        hidden_layer_size(2));
    initial_Theta3 = randInitializeWeights(hidden_layer_size(2), num_labels);

    % Unroll parameters
    initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:); initial_Theta3(:)];
    %% =================== Part 8: Training NN ===================
    %  Training our NN with Train set and finding the optimum value for lambda
    %  and threshold(decision) by checking error on Validation set
    %
    fprintf('\nTraining Neural Network... \n');
    
    best_accuracy = -Inf;
    best_fp = Inf;
    % choosing best lambda over Validation set
    for i = 1:length(lambda_vec)
        lambda = lambda_vec(i);

    % Create "short hand" for the cost function to be minimized
        costFunction = @(p) nnCostFunction(p, ...
                                           input_layer_size, ...
                                           hidden_layer_size, ...
                                           num_labels, Xtrain, ytrain, lambda, fp_penalty_coef, fn_penalty_coef);

    % Now, costFunction is a function that takes in only one argument (the
    % neural network parameters)
        [nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

        % Obtain Theta1 and Theta2 back from nn_params
        Theta1 = reshape(nn_params(1:borders(1)), ...
                     hidden_layer_size(1), (input_layer_size + 1));

        Theta2 = reshape(nn_params(1 + borders(1): borders(1) + borders(2)), ...
                     hidden_layer_size(2), (hidden_layer_size(1) + 1));

        Theta3 = reshape(nn_params(1 + borders(1) + borders(2): end), ...
                     num_labels, (hidden_layer_size(2) + 1));

        % predic on Validation set to get the best lambda; choosing best
        % threshold
        for j = 1:length(threshold_vec)
            threshold = threshold_vec(j);
            pred = predictNN(Theta1, Theta2, Theta3, Xval, threshold);
            [accuracy, f_score, tp, fp, fn, tn] = errorAnalysis(yval, pred);
            if metric == "accuracy"
                if accuracy > best_accuracy
                    best_accuracy = accuracy;
                    best_lambda = lambda;
                    best_threshold = threshold;
                    Theta1_b = Theta1;
                    Theta2_b = Theta2;
                    Theta3_b = Theta3;
                end
            elseif metric == "fp_min"
                if fp < best_fp
                    best_fp = fp;
                    best_lambda = lambda;
                    best_threshold = threshold;
                    Theta1_b = Theta1;
                    Theta2_b = Theta2;
                    Theta3_b = Theta3;
                end
            end
        end
    end
    
    % finer granuality for threshold
    threshold_dyn_vec = max(0, best_threshold - 0.05):0.01:min(1, best_threshold + 0.05);
    for j = 1:length(threshold_dyn_vec)
        threshold = threshold_dyn_vec(j);
        pred = predictNN(Theta1, Theta2, Theta3, Xval, threshold);
        [accuracy, f_score, tp, fp, fn, tn] = errorAnalysis(yval, pred);
        if metric == "accuracy"
            if accuracy > best_accuracy
                best_accuracy = accuracy;
                best_lambda = lambda;
                best_threshold = threshold;
                Theta1_b = Theta1;
                Theta2_b = Theta2;
                Theta3_b = Theta3;
            end
        elseif metric == "fp_min"
            if fp < best_fp
                best_fp = fp;
                best_lambda = lambda;
                best_threshold = threshold;
                Theta1_b = Theta1;
                Theta2_b = Theta2;
                Theta3_b = Theta3;
            end
        end
    end
    % Compute accuracy on our test set
    fprintf("\n Best lambda: %f", best_lambda);
    fprintf("\n Best Threshold: %f", best_threshold);
    fprintf("\n***********************");
    
    if normalize == 1
        Xtest = bsxfun(@minus, Xtest, mu);
        Xtest = bsxfun(@rdivide, Xtest, sigma);
    end
    yp_test = predictNN(Theta1_b, Theta2_b, Theta3_b, Xtest, best_threshold);
    [accuracy_test(jj), fscore_test(jj), tp_test(jj), fp_test(jj),...
        fn_test(jj), tn_test(jj)] = errorAnalysis(ytest, yp_test);
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
               if normalize
                   mid_norm = bsxfun(@minus, mid, mu(end));
                   mid_norm = bsxfun(@rdivide, mid_norm, sigma(end));
               end
               res_tmp = predictNN(Theta1_b, Theta2_b, Theta3_b, ...
                   [Xtest(p, 1:end-1), mid_norm], best_threshold);  % replace su real power with mid
               if res_tmp
                   l = mid;
               else
                   h = mid;
               end
            end
            ypower_test_predicted(p) = l + (h - l)/2;
        end
        average_diff_power(jj) = round(mean(abs(ypower_test_gt - ypower_test_predicted)), 3);
        max_diff_power(jj) = round(max(abs(ypower_test_gt - ypower_test_predicted)), 3);
        fp_num(jj) = sum(ypower_test_predicted > ypower_test_gt);
        fp_mean(jj) = round(mean((ypower_test_predicted - ypower_test_gt).*(ypower_test_predicted>ypower_test_gt)), 3);
    end
end



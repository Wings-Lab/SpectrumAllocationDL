function W = randInitializeWeights(L_in, L_out)
%RANDINITIALIZEWEIGHTS Randomly initialize the weights of a layer with L_in
%incoming connections and L_out outgoing connections
%   W = RANDINITIALIZEWEIGHTS(L_in, L_out) randomly initializes the weights 
%   of a layer with L_in incoming connections and L_out outgoing 
%   connections. 



INIT_EPSILON = 0.20;
W = rand(L_out,1 + L_in) * (2 * INIT_EPSILON) - INIT_EPSILON;



% =========================================================================

end

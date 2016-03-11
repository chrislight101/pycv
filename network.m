% training data
x = [0 0;0 1;1 0;1 1]; % XOR 4 training examples of 2 inputs each
x = [ones(size(x,1),1),x]; % add +1 bias to each example
y = [0;1;1;0]; % XOR 4 training outputs
m = size(x,1); % number of examples
k = size(y,1); % number of classes

% random weight initialization bounded by epsilon
epsilon = 0.1;
w1 = rand(2,3)*(2*epsilon)-epsilon; % (n_hidden * num_input+1)
w2 = rand(1,3)*(2*epsilon)-epsilon;

% forward propagation
a1 = x;
z2 = a1*w1';
a2 = sigmoid(z2); % activation outputs of hidden layer
a2 = [ones(size(a2,1),1),a2];
z3 = a2*w2';
a3 = sigmoid(z3); % hx, activation output of output layer

% cost computation
d3 = a3 - y;
d2 = 



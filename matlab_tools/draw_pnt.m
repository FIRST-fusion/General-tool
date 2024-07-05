% This code is to calculate the relation between P, N, T and their gradient for bootsp.f
% Lin Shih
% 2024/6/14

%% EPFL thesis 
% p = 1.086*[0.9210 -0.6105 -0.6105 0.6105 0.0 0.0 0.0 0.0 0.0 0.0 -0.621 ...
%        0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.3105]
% % pprime
% pprime = 1.086*[-0.6105 -2*0.6105 3*0.6105 0.0 0.0 0.0 0.0 0.0 0.0 -6.21 ...
%         0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 20*0.3105]
% % DENSITY OF EPFL_BSJ
% n      = [ 0.9438 -0.3105 -0.3105 0.3105 0.0 0.0 0.0 0.0 0.0 0.0 -2*0.6333 ...
%           0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.6333]
% nprime = [ -0.3105 -2*0.3105 3*0.3105 0.0 0.0 0.0 0.0 0.0 0.0 -20*0.6333 ...
%           0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 20*0.6333 ]

%% Modified 0614 
% p = [1 -0.3667 -0.3667 0.3667 0.0 0.0 0.0 0.0 0.0 0.0 -2*0.6333 ...
%     0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.6333]
% % pprime
% pprime = [-0.3667 -2*0.3667 3*0.3667 0.0 0.0 0.0 0.0 0.0 0.0 -2*10*0.6333 ...
%         0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 20*0.6333]
% % DENSITY OF EPFL_BSJ
% n      = [ 0.9438 -0.3105 -0.3105 0.3105 0.0 0.0 0.0 0.0 0.0 0.0 -2*0.6333 ...
%           0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.6333]
% nprime = [ -0.3105 -2*0.3105 3*0.3105 0.0 0.0 0.0 0.0 0.0 0.0 -20*0.6333 ...
%           0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 20*0.6333 ]
%% Miller 
% p = [1-0.9813 -0.025 0.0 0.0 -0.975/4 1/5 ]
c = -0.0687
p = [1 0.025/c 0.0 0.0 0.975/4/c -1/5/c ]
pprime = [0.025/c 0.0 0.0 0.975/c -1/c]
n = [1 0.025/c 0.0 0.0 0.975/4/c -1/5/c ]
nprime = [0.025/c 0.0 0.0 0.975/c -1/c]

% Define the range of x values
x = linspace(0, 1, 100);  % Adjust the number of points for smoother plotting

% Initialize the power series
Press = zeros(size(x));
Press_prime = zeros(size(x));
Density = zeros(size(x));
Density_prime = zeros(size(x));
Temp = zeros(size(x));
Temp_prime = zeros(size(x));


% Generate the power series
for i = 1:length(p)
    Press = Press + p(i) * x.^(i-1);
end

for i = 1:length(pprime)
    Press_prime = Press_prime + pprime(i) * x.^(i-1);
end
for i = 1:length(n)
    Density = Density + n(i) * x.^(i-1);
end
for i = 1:length(nprime)
    Density_prime = Density_prime + nprime(i) * x.^(i-1);
end

Temp = Press ./ Density
% Temp_prime = (Press_prime .* Density - Press .* Density_prime) ./ (Density .^ 2);

% Normalize the power series
Press = Press / max(abs(Press))
Press_prime = Press_prime / max(abs(Press_prime))
Density = Density / max(abs(Density))
Density_prime = Density_prime / max(abs(Density_prime))
% Temp = Temp / max(abs(Temp));

%% Plot the power series
figure;
hold on;
plot(x, Press, 'r', 'LineWidth', 2, 'DisplayName', 'p');
plot(x, Density, 'b', 'LineWidth', 2, 'DisplayName', 'n');
% plot(x, Temp, 'k', 'LineWidth', 2, 'DisplayName', 'temp');
plot(x, Press_prime, '--r', 'LineWidth', 2, 'DisplayName','p-prime');
plot(x, Density_prime, '--b', 'LineWidth', 2, 'DisplayName','n-prime');
% plot(x, Temp_prime, '--k', 'LineWidth', 2, 'DisplayName', 'temp-prime');
% xlabel('x');
% ylabel('p');
legend('show','Fontsize',14);
grid on;

% saveas(gcf, [input, '.png']);


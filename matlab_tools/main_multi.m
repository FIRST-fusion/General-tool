% Specify the directory containing the data files
<<<<<<< HEAD
directory = 'mast_240918';
profile = 'mast_snake_950kA_ns129';
fileList = dir(fullfile(directory, '*snake*.nc'));
=======
directory = '240712_tony/';
% directory = 'snake/tcv/axisym/662kA';

profile = 'tcv_snake_662kA';
fileList = dir(fullfile(directory, 'wout*.nc'));
>>>>>>> 234912dd1648afc86525f55af395f00c23eec555
n_loop = length(fileList);
% n_loop = 2 
R0 = 0.47
aspect_ratio = 1.46875

% R0 = 0.45
% aspect_ratio = 1.4

a = R0/aspect_ratio

% Get a list of all files with a specific extension (e.g., '.txt')
filename = cell(n_loop, 1);
iter     = cell(n_loop, 1);
jcuru    = cell(n_loop, 1);
jcurv    = cell(n_loop, 1);
jdotb    = cell(n_loop, 1);
ns       = cell(n_loop, 1);
s        = cell(n_loop, 1);
q_factor = cell(n_loop, 1);
b0       = cell(n_loop, 1);
p_avg    = cell(n_loop, 1);
ctor     = cell(n_loop, 1);

% beta     = cell(n_loop, 1);
% beta_N   = cell(n_loop, 1);
beta = [];
beta_N = [];

for i = 1:n_loop
    filename{i} = fullfile(directory, fileList(i).name);
    jcuru{i}    = ncread(filename{i}, 'jcuru');
    jcurv{i}    = ncread(filename{i}, 'jcurv');
    jdotb{i}    = ncread(filename{i}, 'jdotb');
    ns{i}       = ncread(filename{i}, 'ns');
    q_factor{i} = ncread(filename{i}, 'q_factor');
    b0{i}       = ncread(filename{i}, 'b0');
    p_avg{i}    = ncread(filename{i}, 'p_avg');
    ctor{i}     = ncread(filename{i}, 'ctor');
    betatotal{i}     = ncread(filename{i}, 'betaxis');


    npoint      = cast(ns{i}, 'double');
    s{i}        = 0:1 / (npoint - 1): 1;
    strNumber = num2str(i);
    % iter{i}     = ['j_',strNumber];
    % iter{i}     =['iteration_',strNumber];

    [q_min,min_index] = min(q_factor{i});
    [q_max,max_index] = max(q_factor{i});
    % fprintf('The qmax is: %d, at index: %d\n', q_max, max_index);
    % fprintf('The qmin is: %d, at index: %d\n', q_min, min_index);

    %% calculate beta and beta_N
    beta(i) = 2*(4*pi*10^(-7))* p_avg{i}/b0{i}^2;
    beta_N(i) = beta(i) * 100 / ( -ctor{i} * 10^(-6)/( b0{i} * a));
    % beta_N(i) = -ctor{i} * 10^(-6)/( b0{i} *(R0/aspect_ratio));

end

disp(betatotal')
disp("B0  ")
disp(b0)
disp("< p >")
disp(p_avg)
disp("beta: ")
disp(beta')
disp("beta_N: ")
disp(beta_N')
% iter{1} = "without bsc"
iter{1} = "iteration 1"
iter{2} = "iteration 2"
iter{3} = "iteration 3"

%% Draw jcurv
figure;
hold on;
for i = 1:n_loop
    % plot(s{i},jcurv{i},'LineWidth',2);
    plot(s{i},jcurv{i},'LineWidth',2,'DisplayName', iter{i});
end
legend('show')
grid on;
title('toroidal current density profile','FontSize',18);
ylabel('jcurv','FontSize',14);
xlabel('\rho','FontSize',14);
set(gcf, 'Position', [100, 100, 500, 500]);
set(gca, 'FontSize', 14);
hold off;
plotname = ['jcurv_',profile,'.png'];
saveas(gcf,plotname);

%% Draw jdotB
figure;
hold on;
for i = 1:n_loop
   % plot(s{i},jdotb{i},'LineWidth',2);
     plot(s{i},jdotb{i},'LineWidth',2,'DisplayName', iter{i});
end
legend('show')
grid on;
title('\langle J \cdot B \rangle ','FontSize',18);
ylabel('\langle J \cdot B \rangle','FontSize',18);
xlabel('\rho','FontSize',18);
hold off;
plotname = ['jdotb_',profile,'.png'];
saveas(gcf,plotname);

%% Draw q_factor
figure;
hold on;
for i = 1:n_loop
    % plot(s{i},q_factor{i},'LineWidth',2);
    plot(s{i},q_factor{i},'LineWidth',2,'DisplayName', iter{i});
end
legend('show')
grid on;
title('q profile','FontSize',14);
ylabel('q','FontSize',14);
xlabel('\rho','FontSize',14);
set(gcf, 'Position', [100, 100, 500, 500]);
set(gca, 'FontSize', 14);
hold off;
plotname = ['q_factor_',profile,'.png'];
saveas(gcf,plotname);

% %% Draw jcuru
% figure;
% hold on;
% for i = 1:n_loop
%     plot(s{i},jcuru{i},'LineWidth',2);
%     % plot(s{i},jcuru{i},'LineWidth',2','DisplayName', iter{i});
% end
% grid on;
% % legend('show')
% title('poloidal current density profile','FontSize',18);
% ylabel('jcuru','FontSize',18);
% xlabel('\rho','FontSize',18);
% hold off;
% plotname = ['jcuru_',profile,'.png'];
% saveas(gcf,plotname);
%% Draw Beta trend 
% figure;
% set(gca, 'FontSize', 14,'FontUnits','points')
% elong=[2.0, 2.2, 2.4, 2.6, 2.8];
% % plot(elong, beta,'-s','LineWidth',2,'MarkerSize',10);
% % ylabel('\beta','FontSize',18,'FontUnits','points');
% % ylim([0.0, 0.8]);
% plot(elong, beta_N,'-s','LineWidth',2,'MarkerSize',10);
% ylabel('\beta_N','FontSize',18,'FontUnits','points');
% ylim([5, 10]);
% xlabel('\kappa','FontSize',24,'FontUnits','points'); % Enlarge x-axis label font size
% xlim([1.9,2.9]); % elong

% delta = [0.4, 0.5, 0.6];
% plot(delta, beta,'-s','LineWidth',2,'MarkerSize',10);
% ylabel('\beta','FontSize',18,'FontUnits','points');
% ylim([0.0, 0.8]);
% plot(delta, beta_N,'-s','LineWidth',2,'MarkerSize',10);
% ylabel('\beta_N','FontSize',18,'FontUnits','points');
% ylim([5,10]);
% xlabel('\delta','FontSize',24,'FontUnits','points'); % Enlarge x-axis label font size
% xlim([0.35,0.65]);

% %% beta vs beta N
% yyaxis left;
% plot(elong, beta,'--o','LineWidth',2,'MarkerFaceColor','b','MarkerSize',10);
% ylabel('\beta','FontSize',18,'FontUnits','points');
% ylim([0.0, 0.6]);

% yyaxis right;
% plot(elong, beta_N,'-s','LineWidth',2,'MarkerFaceColor','r','MarkerSize',10);
% ylabel('\beta_N','FontSize',18,'FontUnits','points');
% ylim([0, 10]);

% grid on;
% xlabel('\kappa','FontSize',24,'FontUnits','points'); % Enlarge x-axis label font size
% xlim([1.9,2.9]);
% plotname = ['beta_elongation_',profile,'.png'];
% saveas(gcf,plotname);

% 
% iter{1} = "Total toroidal current profile"
% iter{2} = "Bootstrap current profile"

% iter{1} = "\kappa = 2.0";
% iter{2} = "\kappa = 2.2";
% iter{3} = "\kappa = 2.4";
% iter{4} = "\kappa = 2.6";
% iter{5} = "\kappa = 2.8";



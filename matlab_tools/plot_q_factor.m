function draw_q_factor(inputfile)

filename = truncateString(inputfile);

% read from NCfile
q_factor=ncread(inputfile,'q_factor');
ns=ncread(inputfile,'ns');

npoint = cast(ns,'double');
s = 0:1/(npoint-1.):1;

plot(s,q_factor,'LineWidth',2);
grid on;
xlabel('\rho','FontSize',18);
ylabel('q','FontSize',18);
fontsize(15.5,"points");

plotname = [filename,'_q_factor.png'];
saveas(gcf,plotname);

end

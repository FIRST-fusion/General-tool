function draw_pressure(inputfile)

filename=truncateString(inputfile);
% read from NCfile
presf=ncread(inputfile,'presf');
ns=ncread(inputfile,'ns');

npoint = cast(ns,'double');
s = 0:1/(npoint-1.):1;

plot(s,presf,'LineWidth',2);
grid on;
xlabel('\rho','FontSize',18);
ylabel('P [Pa]','FontSize',18);
fontsize(13.5,"points");


plotname = [filename,'_presf.png'];
saveas(gcf,plotname);

end

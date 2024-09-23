function draw_jcuru(inputfile)

filename=truncateString(inputfile);

% read from NCfile
jcuru=ncread(inputfile,'jcuru');
ns=ncread(inputfile,'ns');

npoint = cast(ns,'double');
s = 0:1/(npoint-1.):1;

plot(s,jcuru,'LineWidth',2);
grid on;
xlabel('\rho','FontSize',18);
ylabel('poloidal current density','FontSize',18);
fontsize(13.5,"points");

plotname = [filename,'_jcuru.png'];
saveas(gcf,plotname);


end

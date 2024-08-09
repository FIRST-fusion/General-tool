function draw_jcurv(inputfile)

% draw_jcurv('wout_filename.nc)
% Created by Lin 2023
% uploaded in 2024 July 4th

filename = truncateString(inputfile);

% read from NCfile
jcurv=ncread(inputfile,'jcurv');
ns=ncread(inputfile,'ns');

npoint = cast(ns,'double');
s = 0:1/(npoint-1.):1;

% normalized_profile =  (jcurv - min(jcurv)) / (max(jcurv) - min(jcurv));

plot(s,jcurv,'LineWidth',2);
% plot(s,normalized_profile,'LineWidth',2);
grid on;
xlabel('\rho','FontSize',20);
ylabel('toroidal current density','FontSize',20);
fontsize(13.5,"points");


plotname = [filename,'_jcurv.png'];
saveas(gcf,plotname);

end

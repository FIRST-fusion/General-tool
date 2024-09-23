function draw_jdotb(inputfile)


filename=truncateString(inputfile);

% read from NCfile
jdotb=ncread(inputfile,'jdotb');
ns=ncread(inputfile,'ns');

npoint = cast(ns,'double');
s = 0:1/(npoint-1.):1;

plot(s,jdotb,'LineWidth',2);
grid on;
ylabel('\langle J \cdot B \rangle','FontSize',18);
xlabel('\rho','FontSize',18);
fontsize(13.5,"points");

plotname = [filename,'_jdotb.png'];
saveas(gcf,plotname);

end

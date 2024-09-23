
function main_2D(inputfile,coilfile) %varargin coils

R0 = 0.45
a=0.32
aspect_ratio =R0/a
% coil_data=read_coils('coils.*')

% fprintf('Draw plots from wout type: %s\n ',inputfile);
% inputfile = 'wout_tcv_301123a_s225_j2.nc'
% inputfile = ['wout/wout_',inputfile,'.vmec.nc'];
filename=truncateString(inputfile)
numdefargs=1;   %Number of default arguments
if nargin >numdefargs
    coil_data=read_coils(coilfile)
end
phidex=180;   % Index at which to plot the flux surfaces
% read from wout
rmin_surf=ncread(inputfile,'rmin_surf');
rmax_surf=ncread(inputfile,'rmax_surf');
rmnc=ncread(inputfile,'rmnc');
zmns=ncread(inputfile,'zmns');
bmnc=ncread(inputfile,'bmnc'); 
xn=ncread(inputfile,'xn');
xm=ncread(inputfile,'xm');
xn_nyq=ncread(inputfile,'xn_nyq');
xm_nyq=ncread(inputfile,'xm_nyq');
ns=ncread(inputfile,'ns');
nfp=ncread(inputfile,'nfp');
ntor=ncread(inputfile,'ntor');
mpol=ncread(inputfile,'mpol');
presf=ncread(inputfile,'presf');
b0=ncread(inputfile,'b0');
ctor=ncread(inputfile,'ctor');

theta=0:2*pi/(359):2*pi;   
phi=0:2*pi/(359):2*pi;      
% phi=0:2*pi/(359):2*pi;      

r=cfunct(theta,phi,rmnc,xm,xn);  % Cos transform
z=sfunct(theta,phi,zmns,xm,xn);  % Sin transform
modb=cfunct(theta,phi,bmnc,xm_nyq,xn_nyq);
presf_=presfunct(theta,phi,presf);



%%  2D flux surface
% Here we only note that r and z are indexed (s,theta,phi)
 figure;
 % plot_wall();
 % hold on;
 % plot_pvi();
 plot(r(ns,:,phidex),z(ns,:,phidex),'r');  % Boundary
 hold on;
 for i=2:ns-1
     plot(r(i,:,phidex),z(i,:,phidex),'k');          % Inner flux
 end
 plot(r(1,1,phidex),z(1,1,phidex),'+k');             % Magnetic Axis
 % hold off
 axis equal
 grid on;
 xlabel('R [m]');
 ylabel('Z [m]');
 fontsize(13.5,"points");
 title(['Flux Surfaces at \phi = ', num2str((phidex), '%4.2f'),'\circ' ...
        ', n = ', num2str(ntor * nfp), ...
        ', m = ', num2str(mpol-2)]);
 % hold on
 savefilename0 = [filename,'_fluxsurf.png'];
 saveas(gcf,savefilename0);
 % if nargin >numdefargs
 %     plot_coils(coil_data,'plane')
 %     savefilename10 = [filename,'_fluxsurf_coilplane.png'];
 %     saveas(gcf,savefilename10);
 % end
 %% 2D Contour plots (modB)
 figure;
 torocont(r,z,modb,phidex);
 colormap(jet)
 colorbar;
 xlabel('R [m]');
 ylabel('Z [m]');
 fontsize(13.5,"points");
 title(['|B| at phi=' num2str(phi(phidex),'%4.2f'),...
        ', n = ', num2str(ntor * nfp), ...
        ', m = ', num2str(mpol-2)]);
 savefilename1 = [filename,'_ContB.png'];
 saveas(gcf,savefilename1);
 if nargin >numdefargs
     plot_coils(coil_data,'plane')
     savefilename20 = [filename,'_ContB_coilplane.png'];
     saveas(gcf,savefilename20);
 end

%% 2D Contour plots (pressure)
 figure;
 torocont(r,z,presf_,phidex);
 colormap(jet)
 xlabel('R [m]');
 ylabel('Z [m]');
 fontsize(13.5,"points");
 title(['Pressure at phi=' num2str(phi(phidex),'%4.2f'),...
        ', n = ', num2str(ntor * nfp), ...
        ', m = ', num2str(mpol-2)]);
 savefilename1 = [filename,'_Contpres.png'];
 saveas(gcf,savefilename1);
 if nargin >numdefargs
     plot_coils(coil_data,'plane')
     savefilename30 = [filename,'_Contpres_coilplane.png'];
     saveas(gcf,savefilename30);
 end

%  3D Flux surface plots (isotoro)

% figure;
% isotoro(r,z,phi,ns,modb);
% colormap(jet)
% colorbar;
% grid on;
% xlabel('x [m]');
% ylabel('y [m]');
% zlabel('z [m]');
% fontsize(13.5,"points");
% title(['Flux Surface (ns=' num2str(ns,'%3d'),...
%        ', n = ', num2str(ntor * nfp), ...
%        ', m = ', num2str(mpol-2),')']);
% savefilename2 = [filename,'_3DFluxSurf.png'];
% saveas(gcf,savefilename2);
% if nargin >numdefargs
%     % plot_coils(coil_data,'field_period')
%     plot_coils(coil_data);
%     % plot_coils(coil_data,'tube','nedges',20,'tubewidth',0.2);
%     colormap(jet)
%     savefilename30 = [filename,'_3D_coil.png'];
%     saveas(gcf,savefilename30);
% end



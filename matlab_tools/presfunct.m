function f=presfunct(theta,zeta,presf)
% SFUNCT(theta,zeta,zmns,xm,xn) Sine Fourier Transform


% ns=size(presf)
ns = size(presf, 1);
lt=length(theta);
lz=length(zeta);
f = zeros(ns, lt, lz);

for k=1:ns

    % f(k,:,:)= repmat(presf,[1,lt]);
    f(k, :, :) = repmat(presf(k, :), [lt, lz]);
end
return
end    
% zmn=repmat(zmns(:,k),[1 lt]);
    % f(k,:,:)=(zmn.*sinmt)'*cosnz+(zmn.*cosmt)'*sinnz;

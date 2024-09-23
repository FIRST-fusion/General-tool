function main(inputfile,R0,a)
    if nargin < 2
        R0 = 0.45;  % Default value for R0
    end
    if nargin < 3
        a = 0.32;   % Default value for a
    end
    
    % Now you can use inputfile, R0, and a in your function
    % Example usage:
    fprintf('Input file: %s\n', inputfile);
    fprintf('R0: %.2f\n', R0);
    fprintf('a: %.2f\n', a);
    aspect_ratio =R0/a
    filename=truncateString(inputfile)
    b0=ncread(inputfile,'b0');
    p_avg=ncread(inputfile,'p_avg');
    ctor=ncread(inputfile,'ctor');
    
    
    % Physical parameters
    grid on;
    plot_pressure(inputfile);
    % plot_jcuru(inputfile);
    plot_jcurv(inputfile);
    % plot_jdotb(inputfile);    
    plot_q_factor(inputfile);

    
    disp('B on axis:')
    disp(b0)
    beta = 2*(4*pi*10^(-7))*p_avg/b0^2
    beta_N = beta* 100 / ( -ctor * 10^(-6)/( b0 * a))

end

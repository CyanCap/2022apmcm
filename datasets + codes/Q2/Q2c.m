% Grey relation analysis
clear all
close all
clc
    
zongshouru = [3439, 4002, 4519, 4995, 5566];
daxuesheng = [341, 409, 556, 719, 903];
congyerenyuan = [183, 196, 564, 598, 613];
xingjifandian = [3248, 3856, 6029, 7358, 8880];

filename='./total (c).xlsx';
dt=xlsread(filename,'Sheet2','A2:I32');

yr=reshape(dt(:,1),1,31)
fr=reshape(dt(:,2),1,31)
c2=reshape(dt(:,3),1,31)
mi=reshape(dt(:,4),1,31)
pl=reshape(dt(:,5),1,31)
pd=reshape(dt(:,6),1,31)
td=reshape(dt(:,7),1,31)
al=reshape(dt(:,8),1,31)
tp=reshape(dt(:,9),1,31)



% %     define comparative and reference
% x0 = zongshouru;
% x1 = daxuesheng;
% x2 = congyerenyuan;
% x3 = xingjifandian;

x0=tp
x1=fr
x2=c2
x3=mi
x4=pl
x5=pd
x6=td
x7=al

%     % normalization
x0 = x0 ./ x0(1);
x1 = x1 ./ x1(1);
x2 = x2 ./ x2(1);
x3 = x3 ./ x3(1);
x4 = x4 ./ x4(1);
x5 = x5 ./ x5(1);
x6 = x6 ./ x6(1);
x7 = x7 ./ x7(1);


%     
%     % global min and max
global_min = min(min(abs([x1; x2; x3;x4;x5;x6;x7] - repmat(x0, [7, 1]))));
global_max = max(max(abs([x1; x2; x3;x4;x5;x6;x7] - repmat(x0, [7, 1]))));
%     
%     % set rho
rho = 0.5;
   


    % calculate zeta relation coefficients
zeta_1 = (global_min + rho * global_max) ./ (abs(x0 - x1) + rho * global_max);
zeta_2 = (global_min + rho * global_max) ./ (abs(x0 - x2) + rho * global_max);
zeta_3 = (global_min + rho * global_max) ./ (abs(x0 - x3) + rho * global_max);
zeta_4 = (global_min + rho * global_max) ./ (abs(x0 - x4) + rho * global_max);
zeta_5 = (global_min + rho * global_max) ./ (abs(x0 - x5) + rho * global_max);
zeta_6 = (global_min + rho * global_max) ./ (abs(x0 - x6) + rho * global_max);
zeta_7 = (global_min + rho * global_max) ./ (abs(x0 - x7) + rho * global_max);

%     % show
figure;
plot(x0, 'ro-' )
hold on
plot(x1, 'b*-')
hold on
plot(x2, 'g*-')
hold on
plot(x3, 'c*-')
hold on
plot(x4, 'm*-')
hold on
plot(x5, 'y*-')
hold on
plot(x6, 'k*-')
hold on
plot(x7, 'r*-')
legend('temperature', 'forest', 'CO2', 'marco ind', 'population', 'products', 'trade', 'agricultral land')
    
figure;
plot(zeta_1, 'b*-' )
hold on
plot(zeta_2, 'g*-')
hold on
plot(zeta_3, 'c*-')
hold on
plot(zeta_4, 'm*-')
hold on
plot(zeta_5, 'y*-')
hold on
plot(zeta_6, 'k*-')
hold on
plot(zeta_7, 'r*-')
hold on
legend('forest', 'CO2', 'marco ind', 'population', 'products', 'trade', 'agricultral land')
    

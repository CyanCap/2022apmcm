clear,clc
covid=xlsread('COVID-19',1,'H3:H48');
tem=xlsread('COVID-19',1,'E3:E48');
date=xlsread('COVID-19',1,'D3:D48');

plot(date,tem,'b','LineWidth',1);
hold on;
plot(date,covid,'r','LineWidth',1);

xlabel('month starts from 2020 Jan');
ylabel('temperature and population(*100000)');
legend('temperature','infected population');
title('picture of COVID-19 and temperature');

sum(tem(1:15))/15
sum(tem(16:46))/31
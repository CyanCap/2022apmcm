clear all
clc
date=1751:2021;
rawdata=xlsread('land year std data.xls');
data=rawdata';
%rawdata=xlsread('land avg monthly.xlsx');
%data=rawdata([1800:3274],13)';
subplot(131)
plot(data,'b-','LineWidth',2)
xlabel('time')
ylabel('data')
set(gca,'fontsize',15)
subplot(132)
ddata = diff(data);
plot(ddata,'b-','LineWidth',2)
xlabel('time')
ylabel('first order difference of data')
set(gca,'fontsize',15)
subplot(133)
dddata = diff(data,2);
plot(dddata,'b-','LineWidth',2)
xlabel('time')
ylabel('second order difference of data')

set(gca,'fontsize',15)

% Stationarity Test of the raw data
d_adf=adftest(data)
d_kpss=kpsstest(data)

%if adftest=0 or kpsstest=1 that means the data is not stationary
ddata = diff(data);
d1_adf = adftest(ddata)
d1_kpss = kpsstest(ddata)

%if adftest=1 or kpsstest=0 that means the data is stationary
%ddata=data;

% draw the ACF graph and PACF graph
figure
subplot(211)
autocorr(ddata,40)
ylabel('ACF')
set(gca,'fontsize',15)

subplot(212)
parcorr(ddata,40)
ylabel('PACF')
set(gca,'fontsize',15)

%% calculate the value of q and p
pmax = 4;
qmax = 4;
d = 1;
[p, q ]=findPQ(data,pmax,qmax,d);

%% bulit model
%p = 3;q = 2;
Mdl = arima(p, 1, q);  %first order difference
EstMdl = estimate(Mdl,data');
%% predict model
step = 2000;
[forData,YMSE] = forecast(EstMdl,step,'Y0',data');  
lower = forData - 1.96*sqrt(YMSE); %the lower bound of the 95% confident interval
upper = forData + 1.96*sqrt(YMSE); %the upper bound of the 95% confident interval

figure
plot(1:length(data),data)
hold on
plot((length(data)+1):length(data)+step,forData)
hold on
plot((length(data)+1):length(data)+step,lower)
plot((length(data)+1):length(data)+step,upper)

function [p q] = findPQ(data,pmax,qmax,d)
data = reshape(data,length(data),1);
LOGL=zeros(pmax+1,qmax+1);
PQ=zeros(pmax+1,qmax+1);
for p=0:pmax
    for q=0:qmax
        model=arima(p,d,q);
        [fit,~,logL]=estimate(model,data);  %strcture
        LOGL(p+1,q+1)=logL;
        PQ(p+1,q+1)=p+q;  %number of parameters
    end
end
LOGL=reshape(LOGL,(pmax+1)*(qmax+1),1);
PQ=reshape(PQ,(pmax+1)*(qmax+1),1);
m2 = length(data);
[aic,bic]=aicbic(LOGL,PQ+1,m2);
aic0 = reshape(aic,(pmax+1),(qmax+1));
bic0= reshape(bic,(pmax+1),(qmax+1));

aic1 = min(aic0(:));
index = aic1==aic0;
[pp qq] = meshgrid(0:pmax,0:qmax);
p0 = pp(index);
q0 = qq(index);

aic2 = min(bic0(:));
index = aic2==bic0;
[pp qq] = meshgrid(0:pmax,0:qmax);
p1 = pp(index);
q1 = qq(index);

if p0^2+q0^2> p1^2+q1^2
    p = p1;
    q = q1;
else
    p = p0;
    q = q0;
end

end
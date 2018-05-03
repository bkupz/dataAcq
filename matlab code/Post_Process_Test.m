clc, clear all, close all,

% The Bkups_fullspeed.RAW Method
fn = 'logs_70f_100r.RAW';
fileID = fopen(fn,'r');
bytes = fread(fileID);
fsize = size(bytes);
actSize = dir(fn);
actSize = actSize.bytes;
[A,B] = parsemsgpack(bytes,1);
A = transpose(A);
while B < actSize
    [C,B] = parsemsgpack(bytes,B);
    C = transpose(C);
    A = vertcat(A,C);
end
for i=1:length(A)
    temp=A{i};
    DATA(i,:)=cell2mat(temp(1,:));   
end

% %csv method
% filename='2018_04_11@02_06_16.RAW.csv';
% DATA=csvread(filename);%data read

SIZE=size(DATA,1);%data length count
A=zeros(SIZE,1);B=zeros(SIZE,1);C=zeros(SIZE,1);D=zeros(SIZE,1);
E=zeros(SIZE,1);F=zeros(SIZE,1);G=zeros(SIZE,1);H=zeros(SIZE,1);
I=zeros(SIZE,1);J=zeros(SIZE,1);K=zeros(SIZE,1);L=zeros(SIZE,1);
M=zeros(SIZE,1);N=zeros(SIZE,1);O=zeros(SIZE,1);P=zeros(SIZE,1);
Q=zeros(SIZE,1);R=zeros(SIZE,1);S=zeros(SIZE,1);T=zeros(SIZE,1);
U=zeros(SIZE,1);V=zeros(SIZE,1);W=zeros(SIZE,1);X=zeros(SIZE,1);
Y=zeros(SIZE,1);Z=zeros(SIZE,1);AA=zeros(SIZE,1);AB=zeros(SIZE,1);
AC=zeros(SIZE,1);AD=zeros(SIZE,1);AE=zeros(SIZE,1);AF=zeros(SIZE,1);
AG=zeros(SIZE,1);AH=zeros(SIZE,1);AI=zeros(SIZE,1);AJ=zeros(SIZE,1);
AK=zeros(SIZE,1);AL=zeros(SIZE,1);AM=zeros(SIZE,1);AN=zeros(SIZE,1);
AO=zeros(SIZE,1);AP=zeros(SIZE,1);AQ=zeros(SIZE,1);AR=zeros(SIZE,1);

i=1;
while i<=SIZE
     B(i,1)= DATA(i,1);                                     %Converter Voltage
     C(i,1)= DATA(i,2);                                     %Battery Voltage
     D(i,1)= DATA(i,3);
     AR(i,1)= DATA(i,4);
     E(i,1)= DATA(i,5);
     F(i,1)= Temperature(DATA(i,6));                        %CVT Temp
     G(i,1)= Temperature(DATA(i,7));                        %Engine Oil Temp
     H(i,1)= Temperature(DATA(i,8));                        %Gearbox Oil Temp
     I(i,1)= RR_Shock_Pot(DATA(i,9),C(i,1));                %RR Shock Distance
     J(i,1)= RL_Shock_Pot(DATA(i,10),C(i,1));               %RL Shock Distance
     K(i,1)= DATA(i,11);
     L(i,1)= FR_Shock_Pot(DATA(i,12),C(i,1));               %FR Shock Distance
     M(i,1)= FL_Shock_Pot(DATA(i,13),C(i,1));               %FL Shock Distance
     N(i,1)= Rack_Position(DATA(i,14),C(i,1));              %Rack Position
     O(i,1)= DATA(i,15);
     P(i,1)= DATA(i,16);
     Q(i,1)= Pressure(Pi_Plate_Adj(DATA(i,17)));            %RR Shock Pressure
     R(i,1)= Pressure(Pi_Plate_Adj(DATA(i,18)));            %RL Shock Pressure
     S(i,1)= Pi_Plate_Adj(DATA(i,19));
     T(i,1)= Pressure(Pi_Plate_Adj(DATA(i,20)));            %FR Shock Pressure
     U(i,1)= Pressure(Pi_Plate_Adj(DATA(i,21)));            %FL Shock Pressure
     V(i,1)= Pi_Plate_Adj(DATA(i,22));
     W(i,1)= Pressure(Pi_Plate_Adj(DATA(i,23)));            %F Brake Pressure
     X(i,1)= Pressure(Pi_Plate_Adj(DATA(i,24)));            %R Brake Pressure
     Y(i,1)= Strain_Gauge((DATA(i,25)),(2.165),(.07));      %RL Arm Strain Gauge
     Z(i,1)= Strain_Gauge((DATA(i,26)),(2.165),(.001));     %RU Arm Strain Gauge
    AA(i,1)= Strain_Gauge((DATA(i,27)),(2.175),(.086));     %R Tab Strain Gauge
    AB(i,1)= Strain_Gauge((DATA(i,28)),(2.165),(.105));     %FL Arm Strain Gauge
    AC(i,1)= Strain_Gauge((DATA(i,29)),(2.165),(.008));     %FU Arm Strain Gauge
    AD(i,1)= Strain_Gauge((DATA(i,30)),(2.164),(.195));     %Tie Rod Strain Gauge
    AE(i,1)= Strain_Gauge((DATA(i,31)),(2.175),(-.117));    %F Tab Strain Gauge
    AF(i,1)= DATA(i,32);
    AG(i,1)= DATA(i,33);                                    %X Axis Linear Accel
    AH(i,1)= DATA(i,34);                                    %Y Axis Linear Accel
    AI(i,1)= DATA(i,35);                                    %Z Axis Linear Accel
         x = DATA(i,36);
         y = DATA(i,37);
         z = DATA(i,38);
         w = DATA(i,39);
    AN(i,1)= Tachometer(DATA(i,40),1);                  %Engine RPM
    AO(i,1)= Tachometer(DATA(i,41),(1/2.71));               %Itermediate Shaft RPM
    AP(i,1)= Tachometer(DATA(i,42),4);                      %R Half Shaft RPM
    AQ(i,1)= Tachometer(DATA(i,43),4);                      %L Half Shaft RPM
    A(i,1)= DATA(i,44);                                     %Time
    
    % Quaternion Converstion                  
    % Note matlab must have the Aerospace Toolbox installed
    [x, z, y] = quat2angle([x y z w]);
    AJ(i,1)=rad2deg(x);                                     %X Axis Orientation
    AK(i,1)=rad2deg(y);                                     %Y Axis Orientation
    AL(i,:)=rad2deg(z);                                     %Z Axis Orientation

    i=i+1;
end

%Plotting Data

figure %voltage
hold on
plot(A,B),plot(A,C),
legend('Converter Voltage','Battery Voltage'),
xlabel('Time'),ylabel('Volts'),
title('Voltage'),


figure %rpm
subplot(2,1,1)
hold on
plot(A,AN),plot(A,AO),plot(A,AP),plot(A,AQ),
legend('Engine RPM','CVT Secondary','R Half Shaft','L Half Shaft'),
xlabel('Time'),ylabel('RPM'),
title('RPM'),

subplot(2,1,2)
hold on
Ratio=(AN./AO);
plot(A,Ratio),
xlabel('Time'),ylabel('Ratio'),
title('CVT Ratio'),

figure
hold on
CIR=23*pi/12/5280;
MPH=((AP+AQ)/2)*CIR*60;
plot(A,MPH),
xlabel('Time'),ylabel('MPH'),
title('Car Speed'),

figure %pots
subplot(2,1,1)
hold on
plot(A,I),plot(A,J),plot(A,L),plot(A,M),
legend('RR Shock','RL Shock','FR Shock','FL Shock'),
xlabel('Time'),ylabel('Inches'),
title('Shock Distance'),

subplot(2,1,2)
plot(A,N),
xlabel('Time'),ylabel('Inches'),
title('Rack Position'),

figure %temp
hold on
plot(A,F),plot(A,G),plot(A,H),
legend('CVT','Engine','Gearbox'),
xlabel('Time'),ylabel('Celsius'),
title('Temperature'),

figure %shock p
hold on
plot(A,Q),plot(A,R),plot(A,T),plot(A,U),
legend('RR Shock','RL Shock','FR Shock','FL Shock'),
xlabel('Time'),ylabel('PSI'),
title('Shock Pressure'),

figure %brake p
hold on
plot(A,W),plot(A,X),
legend('F Brake','R Brake'),
xlabel('Time'),ylabel('PSI'),
title('Brake Pressure'),

figure %strain gauge
subplot(3,1,1)
hold on
plot(A,Y),plot(A,Z),plot(A,AB),plot(A,AC),
legend('RL Arm','RU Arm','FL Arm','FU Arm'),
xlabel('Time'),ylabel('Strain'),
title('Arm Strain Gauges'),

subplot(3,1,2)
hold on
plot(A,AA),plot(A,AE),
legend('R Tab','F Tab'),
xlabel('Time'),ylabel('Strain'),
title('Tab Strain Gauges'),

subplot(3,1,3)
hold on
plot(A,AD),
xlabel('Time'),ylabel('Strain'),
title('Tie Rod Strain Gauge'),

figure %stress strain
ModE=29700;
Yield=106;
i=1;
TheoStrain=-.01:.02/100:.01;
TheoStrain(:);
TheoStress=-.01:.02/100:.01;
TheoStress(:);
while i<=101
    if TheoStrain(1,i)< (-Yield/ModE)
        TheoStress(1,i)=-1*Yield;
    end
    if TheoStrain(1,i)>= (Yield/ModE)
        TheoStress(1,i)=1*Yield;
    end
    if TheoStrain(1,i)> (-Yield/ModE) && TheoStrain(1,i)< (Yield/ModE)
        TheoStress(1,i)=TheoStrain(1,i)*ModE;
    end
    i=i+1;
end

hold on
plot(TheoStrain,TheoStress,':'),plot(Y,Y*ModE),plot(Z,Z*ModE),plot(AB,AB*ModE),plot(AC,AC*ModE),
legend('Material','RL Arm','RU Arm','FL Arm','FU Arm'),
xlabel('Strain (ksi)'),ylabel('Stress (in/in)'),
title('Arm Strain Gauges'),


figure %linear accel
hold on
plot(A,AH),plot(A,AG),plot(A,AI),
legend('X','Y','Z'),
xlabel('Time'),ylabel('M/S^2'),
title('Linear Acceleration'),

figure %orientation
hold on
plot(A,AJ),plot(A,AK),plot(A,AL),
legend('Pitch','Roll','Yaw'),
xlabel('Time'),ylabel('Degrees'),
title('Orientation'),

%Excel Export
filename = 'logs_70f_100r.xlsx'; % <-- generates new file with indicated name
%Headers
a={'Time','Converter Voltage','Battery Voltage','Engine RPM',...
    'CVT Secondary RPM','R Half Shaft RPM','L Half Shaft RPM',...
    'CVT Ratio','Car MPH','RR Shock Distance','RL Shock Distance',...
    'FR Shock Distance','FL Shock Distance','Rack Position',...
    'CVT Temperature','Engine Temperature','Gearbox Temperature',...
    'RR Shock Pressure','RL Shock Pressure','FR Shock Pressure',...
    'FL Shock Pressure','F Brake Pressure','R Brake Pressure',...
    'RL Arm Strain','RU Arm Strain','FL Arm Strain','FU Arm Strain',...
    'R Tab Strain','F Tab Strain','Tie Rod Strain',...
    'X Axis Linear Acceleration','Y Axis Linear Acceleration',...
    'Z Axis Linear Acceleration','Pitch Orientation',...
    'Roll Orientation','Yaw Orientation'};
%Data Orginization
POST=[A,B,C,AN,AO,AP,AQ,Ratio,MPH,I,J,L,M,N,F,G,H,Q,R,T,U,W,X,Y,Z,AB,...
    AC,AA,AE,AD,AH,AG,AI,AJ,AK,AL];
xlswrite(filename,a,1,'A1')
xlswrite(filename,POST,1,'A2')
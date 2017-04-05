clc
close all
clear all

fileName='MatlabData.mat';

%Importing the data from Python
DataIn = load('-mat', fileName);
XP=DataIn.dataPAll(:,1:3);
YP=DataIn.dataPAll(:,4);



Mdl = TreeBagger(1000,XP,YP,'Method','regression');

HMaster=10;TMaster=1;
H=(75/50)*HMaster/100;T=(300/50)*TMaster/100;

TestData=importdata('../pv-H75T300.txt');
XPredict=zeros(200,3);
XPredict(:,1)=linspace(0,1200,200)*0+H;
XPredict(:,2)=linspace(0,1200,200)*0+T;
XPredict(:,3)=linspace(0,1200,200);

YPredict=predict(Mdl,XPredict);

plot(TestData(:,1),TestData(:,2))
plot(XPredict(:,3),YPredict)


% https://www.mathworks.com/help/stats/treebagger.html

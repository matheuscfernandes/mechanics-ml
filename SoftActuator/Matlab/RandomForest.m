%Reference: https://www.mathworks.com/help/stats/treebagger.html

% clc
close all
% clear all


%% Importing data and learning algorithm
fileName='MatlabData.mat';

%Importing the data from Python
DataIn = load('-mat', fileName);
XP=DataIn.dataPAll(:,1:3);
YP=DataIn.dataPAll(:,4);


% Mdl = TreeBagger(1000,XP,YP,'Method','regression');

%% Testing with training data to evaluate method


%% Testing with never seen data

HMaster=10;TMaster=1;

H=(75/50)*HMaster/100;T=(300/50)*TMaster/100;

TestData=importdata('../pv-H75T300.txt');

XPredict=zeros(200,3);
XPredict(:,1)=linspace(0,12000,200)*0+H;
XPredict(:,2)=linspace(0,12000,200)*0+T;
XPredict(:,3)=linspace(0,12000,200);

YPredict=predict(Mdl,XPredict);
hold on
plot(XPredict(:,3),YPredict,'b','linewidth',4)
plot(TestData(:,1),TestData(:,2),'--r','linewidth',4)
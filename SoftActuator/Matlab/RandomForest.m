%Reference: https://www.mathworks.com/help/stats/treebagger.html

% clc
close all
% clear all


%% Importing data and learning algorithmm
fileName='MatlabData.mat';

%Importing the data from Python
DataIn = load('-mat', fileName);
XP=DataIn.dataPAll(:,1:3);
YP=DataIn.dataPAll(:,4);

% Mdl = TreeBagger(700,XP,YP,'method','regression','OOBPredictorImportance','on',... 
%                  'MinLeafSize',0.001,'NumPrint',100,'NumPredictorsToSample','all');
% save('TrainedRandomForestObject.mat','Mdl','-v7.3')
%% Testing with training data to evaluate method
VNorm=1256.66662598;

H=(77/50);T=(86/50);

TestData=importdata('../Data2/H77/W100H77T86-PV.out');
TestData(:,1)=(TestData(:,1)-min(TestData(:,1)))/VNorm;


XPredict=zeros(200,3);
XPredict(:,1)=linspace(0,13000/VNorm,200)*0+H;
XPredict(:,2)=linspace(0,13000/VNorm,200)*0+T;
XPredict(:,3)=linspace(0,20000/VNorm,200);

figure()
YPredict=predict(Mdl,XPredict);
hold on
plot(XPredict(:,3),YPredict,'b','linewidth',4)
plot(TestData(:,1),TestData(:,2),'--r','linewidth',4)
legend('Prediction','Data','location','southeast')


%% Testing with never seen data

% H=(75/50);T=(300/50);
% 
% TestData=importdata('../pv-H75T300.txt');
% TestData(:,1)=(TestData(:,1)-min(TestData(:,1)))/VNorm;
% 
% XPredict=zeros(200,3);
% XPredict(:,1)=linspace(0,12000/VNorm,200)*0+H;
% XPredict(:,2)=linspace(0,12000/VNorm,200)*0+T;
% XPredict(:,3)=linspace(0,12000/VNorm,200);
% 
% figure()
% YPredict=predict(Mdl,XPredict);
% hold on
% plot(XPredict(:,3),YPredict,'b','linewidth',4)
% plot(TestData(:,1),TestData(:,2)./(0.027711),'--r','linewidth',4)
% legend('Prediction','Data','location','southeast')

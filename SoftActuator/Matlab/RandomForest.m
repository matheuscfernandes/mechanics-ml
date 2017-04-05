clc
close all
clear all

fileName='MatlabData.mat';

%Importing the data from Python
DataIn = load('-mat', fileName);
XP=DataIn.dataPAll(:,1:3);
YP=DataIn.dataPAll(:,4);



Mdl = TreeBagger(100,XP,YP,'Method','regression');



% https://www.mathworks.com/help/stats/treebagger.html

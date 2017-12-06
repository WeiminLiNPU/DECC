clear
clc

load('test.mat');
I = IH_old;
figure(1), imshow(I, []);

% 1. get the high frequency signal for "vessel" + "artery"
m = 1; n = 66;
h = ones(m,n)/(m*n);
I_LF1 = imfilter(I, h, 'replicate'); figure(2), imshow(I_LF1, []);
I_HF1 = I - I_LF1; figure(3), imshow(I_HF1, []);

% 2. get the overall profile of "heart"
m = 60; n = 60; h = ones(m,n)/(m*n);
I_LF2 = imfilter(I, h, 'replicate');
m = 55; n = 2; h = ones(m,n)/(m*n);
I_LF2 = imfilter(I_LF2, h, 'replicate'); figure(4), imshow(I_LF2, []);
I_supp = I_HF1 + I_LF2; figure(5), imshow(I_supp, []);


%% Correct the global boundary intensity difference using v4 interpolation
I_diff = I - I_supp;
l_row=size(I_diff,1); l_col=size(I_diff,2);
x=[1:l_col, 1:l_col];
y=[repmat([1],1,l_col), repmat([l_row],1,l_col)];

z = [];
for i = 1:length(x)
    z = [z,I_diff(y(i),x(i))];
end

[Y,X] = meshgrid(1:l_col,1:l_row);
Z=griddata(y,x,z,X,Y,'v4');

I_supp_fin = I_supp + Z;

figure(6),imshow(I_supp_fin,[]);

figure(7),imshow(I - I_supp_fin, [])
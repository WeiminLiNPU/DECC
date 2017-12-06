close all
clear
clc

%% Read in data
IH=log(double(dicomread('data_case20/IH')));
IL=log(double(dicomread('data_case20/IL')));
IB=1000.*exp(0.73.*imgaussfilt(IL,0.01)-imgaussfilt(IH,0.01));


for iii=1:14
    Rib_Cen=imread(sprintf('data_case20/CenterRib%d.tif',iii));
    
    %% Select out the ROI from images -> Suppress the rib
    [I_row_set,I_col_set]=find(Rib_Cen==1);
    
    IH_patch = []; IL_patch = []; IB_patch = [];
    h = 50;
    for i=1:numel(I_row_set)
        
        IH_patch = [IH_patch, IH(I_row_set(i)-h:I_row_set(i)+h, I_col_set(i))];
        IL_patch = [IL_patch, IL(I_row_set(i)-h:I_row_set(i)+h, I_col_set(i))];
        IB_patch = [IB_patch, IB(I_row_set(i)-h:I_row_set(i)+h, I_col_set(i))];
        
    end
    
    IH_patch_supp = Supp_Rib(IH_patch);
    IL_patch_supp = Supp_Rib(IL_patch);
    IB_patch_supp = Supp_Rib(IB_patch);
    
    %% Give the suppressed result back to images
    h = 50;
    for i=1:numel(I_row_set)
        
        c = round(size(IH_patch_supp,1)/2);
%         knit = 1; gau_knit = 1;
        
        IH(I_row_set(i)-h:I_row_set(i)+h, I_col_set(i)) = IH_patch_supp(c-h:c+h,i);
%         IH(I_row_set(i)-h-knit:I_row_set(i)-h+knit, I_col_set(i)-knit:I_col_set(i)+knit) = imgaussfilt(IH(I_row_set(i)-h-knit:I_row_set(i)-h+knit, I_col_set(i)-knit:I_col_set(i)+knit), gau_knit);
%         IH(I_row_set(i)+h-knit:I_row_set(i)+h+knit, I_col_set(i)-knit:I_col_set(i)+knit) = imgaussfilt(IH(I_row_set(i)+h-knit:I_row_set(i)+h+knit, I_col_set(i)-knit:I_col_set(i)+knit), gau_knit);
        
        IL(I_row_set(i)-h:I_row_set(i)+h, I_col_set(i)) = IL_patch_supp(c-h:c+h,i);
%         IL(I_row_set(i)-h-knit:I_row_set(i)-h+knit, I_col_set(i)-knit:I_col_set(i)+knit) = imgaussfilt(IL(I_row_set(i)-h-knit:I_row_set(i)-h+knit, I_col_set(i)-knit:I_col_set(i)+knit), gau_knit);
%         IL(I_row_set(i)+h-knit:I_row_set(i)+h+knit, I_col_set(i)-knit:I_col_set(i)+knit) = imgaussfilt(IL(I_row_set(i)+h-knit:I_row_set(i)+h+knit, I_col_set(i)-knit:I_col_set(i)+knit), gau_knit);
         
        IB(I_row_set(i)-h:I_row_set(i)+h, I_col_set(i)) = IB_patch_supp(c-h:c+h,i);
%         IB(I_row_set(i)-h-knit:I_row_set(i)-h+knit, I_col_set(i)-knit:I_col_set(i)+knit) = imgaussfilt(IB(I_row_set(i)-h-knit:I_row_set(i)-h+knit, I_col_set(i)-knit:I_col_set(i)+knit), gau_knit);
%         IB(I_row_set(i)+h-knit:I_row_set(i)+h+knit, I_col_set(i)-knit:I_col_set(i)+knit) = imgaussfilt(IB(I_row_set(i)+h-knit:I_row_set(i)+h+knit, I_col_set(i)-knit:I_col_set(i)+knit), gau_knit);
        
    end
    
    
    %% Show results
    figure(1),imshow(IH,[]);
    figure(2),imshow(IL,[]);
%     figure(3),imshow(IB,[0 225]);
    
end

% figure,imshow(-log(IH(493:1639,575:1600)),[]);
% figure,imshow(-log(IL(493:1639,575:1600)),[]);
% IB=1000.*exp(0.73.*imgaussfilt(IL,0.01)-imgaussfilt(IH,0.01));
% figure,imshow(IB(493:1639,575:1600),[]);

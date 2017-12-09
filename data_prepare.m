imgpaths=textread('imglist','%s','delimiter','\n');

n=length(imgpaths);
counter=0;
for i=1:n
    path=imgpaths{i};
    ptspath=strrep(path,'IB.dcm','Point.mat');
    if exist(ptspath,'file')
        img=imadjust(dicomread(path));
        img=mat2gray(img);
        imwrite(img,sprintf('./data/%d.jpg',counter));
        copyfile(ptspath,sprintf('./data/%d.mat',counter)); 
        counter=counter+1;
    end
   
end
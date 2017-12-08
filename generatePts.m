load('./data/10.mat');
file=fopen('./data/10.pts','w');


fprintf(file,sprintf('version: 1\n'));
fprintf(file,sprintf('n_points: 196\n'));
fprintf(file,sprintf('{\n'));
p=P16;
p=round(p);
for i=1:196
    fprintf(file,'%d %d\n',p(i,1),p(i,2));
end
fprintf(file,sprintf('}\n'));




% This code generates a Voronoi-Poisson tessellation for 2d system 
% obtained from LADIA or CalAtom
% usage:rename the position file of atoms to "exp.txt", then run this
%       script and the area information will be output to "area.txt" and
%       print a colored voronoi map
% author: ponychen
% 20200702

clearvars; close all; clc;

%basic parameters you should set
scale = 0.01061 ; %how much nanometer one pixel represent
thershould = 0.08 ; %thershould to judge whether an atom belongs to boundary08
edge = 1 %distance between boundary and edge of ribbon

% read xx yy coordination from exp.txt
fid = fopen('exp.txt','r');
data = fscanf(fid,'%g %g',[2 inf]);
data = data';
fclose(fid);

xx = data(:,1)*scale;
yy = data(:,2)*scale;
%Perform Voronoi tesseslation using built-in function
[v,c] = voronoin([xx(:),yy(:)]);

%%%START -- Plotting section -- START%%%
figure; hold on;

%create voronoi diagram on the point pattern
voronoi(xx,yy);
A = zeros(length(c),2) ;
tot = 0;
num = 0;
for i = 1:length(c)
    v1 = v(c{i},1) ; 
    v2 = v(c{i},2) ;
    s = polyarea(v1,v2) ;
    if s < thershould
        tot = tot+s;
        num = num+1;
        patch(v1,v2,s);
    end
    A(i,1) = i ;
    A(i,2) = s ;
end

%output area of each polygon to area.txt
fid2 = fopen('area.txt','w');
fprintf(fid2,'%d %12.8f\n',A');
fclose(fid2);

%plot underlying point pattern (ie a realization of a Poisson point process)
plot(xx,yy,'r.','MarkerSize',20);
xlabel('Distance (nm)','Fontsize',12,'Fontname','Arial')
ylabel('Distance (nm)','Fontsize',12,'Fontname','Arial')
ylabel(colorbar,'Atomic area (nm^2)','Fontsize',12,'Fontname','Arial');
colormap(cool);
%number/label the points/cells
numPoints = length(c);
labels=cellstr(num2str((1:numPoints)'));%labels correspond to their order
text(xx, yy, labels, 'VerticalAlignment','bottom', ...
    'HorizontalAlignment','right');
% set boundary
if min(xx) < min(yy)
    boundmin = min(xx)-edge;
else
    boundmin = min(yy)-edge;
end
if max(xx) < max(yy)
    boundmax = max(yy)+edge;
else
    boundmax = max(xx)+edge;
end
    
xlim([boundmin boundmax]);
ylim([boundmin boundmax]);

fprintf('the mean atomic area is %12.8f nm^2\n',tot/num);
%%%END -- Plotting section -- END%%%
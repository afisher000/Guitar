% playground for testing code
close all;
clearvars;
rgb     = .9 * ones(1,3);

figure(); 
hold on;
xvec    = [1 2];
yvec    = [1 2];
for j=-.1:.002:.1
    plot(xvec,yvec+j);
end
plot([1 2],[1.5 1.5],'k-')

% annotation('rectangle',[0 0 1 1],'Color',rgb,'FaceColor',rgb,'FaceAlpha',0.5);
text(1.5,1.5,'    ','Margin',0.1,'BackgroundColor',ones(1,3),'FontSize',10);
text(1.5,1.5,num2str(5),'Margin',0.1,'FontSize',10);




















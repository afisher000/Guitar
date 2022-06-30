% Create fretboard

title(['Note number ',num2str(j)]);

% If capo is non-zero, add to figure
if capo>=1
    plot([capo-.2,capo-.2],[0.5,6.5],'k','LineWidth',10);
end
%Loop over strings lines
for istr=1:6
    plot([.5,12.5],[istr,istr],'k');
end

%Loop over fret lines
for ifret= 0.5 : 1 : 12.5
    plot([ifret,ifret],[1,6],'k');
end

% Add fret markers
scatter([3,5,7,9,12,3,5,7,9,12],[.5,.5,.5,.5,.5,6.5,6.5,6.5,6.5,6.5],100,'k');

% Modify Display
xlim([-0.1,13]); ylim([0,7]); xticks(1:12); yticks(1:6);
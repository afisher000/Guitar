% Called by select_notes. This creates the fretboard background for
% selecting notes.

xlabel('Soprano -> red, Alto->magenta, Tenor->green, Bass->blue');
title(['Note number ',num2str(j),' lyric: ',lyrics{j}]);

% If capo is non-zero, add to figure
plot([0.3,0.3],[0.5,6.5],'k','LineWidth',5);

%Loop over strings lines
for istr=1:6
    plot([-.5,12.5],[istr,istr],'k');
end

%Loop over fret lines
for ifret= 0.5 : 1 : 12.5
    plot([ifret,ifret],[1,6],'k');
end

% Add fret markers
scatter([3,5,7,9,12,3,5,7,9,12],[.5,.5,.5,.5,.5,6.5,6.5,6.5,6.5,6.5],100,'k');

% Modify Display
xlim([-0.2,13]); ylim([0,7]); xticks(1:12); yticks(1:6);
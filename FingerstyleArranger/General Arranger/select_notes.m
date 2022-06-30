close all;
clearvars;
% read in specific song
songname='On';
load(['Songs/',songname,'.mat']);
capo=0;

% Loop over song notes
figure(); fig=gcf; set(gcf,'Position',[300,300,900,600]);
ax=axes('Parent',fig);
j=1;
while j<=numnotes
    clf; hold on; 
    create_fretboard;
    add_notes;
    
    hold off;
    
    keypress=0;
    while keypress==0
        keypress=waitforbuttonpress;
    end
    curkey=get(fig,'CurrentKey');
    switch get(fig,'CurrentKey')
        case 'leftarrow'
            j=max(1,j-1);
        case 'rightarrow'
            j=min(j+1,numnotes);
        case 'p'
            jinput=input('Enter note number: ');
            j=min(numnotes,round(jinput));
            j=max(1,j);
        case 'm'
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case 'b'
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case 'escape'
            j=numnotes+1;
        otherwise
    end
end
close all;

save(['Songs/',songname,'.mat'],'melody','bass','capo','numnotes');
clearvars;
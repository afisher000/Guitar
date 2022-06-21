% Called by select_notes. rapid_input allows the user to quickly click
% notes to include in arrangement. (Usually the soprano part). 

maxjj=min(j+rapid_len-1,numnotes);
for jj=j:maxjj
    j=jj;
    clf; hold on;
    create_fretboard;
    add_notes;
    [x,y]=ginput(1);
    qfret=round(x); qstr=round(y);
    update_notes;
end
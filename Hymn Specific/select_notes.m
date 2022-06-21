% Main script for selecting notes that will be included in guitar
% arrangement.
% e,e2,ed,...etc are extra notes that only happen in certain parts. 
% d suffixes represent delays, 2 suffix allows multiple notes at given
% time.

close all;
clearvars;
%% Read in song, transpose using capo
songname='were you there';
load(['Songs/',songname,'.mat']);
capo=6;


% Transpose without changing 12 elements (indicates silence)
flag    = (s.int==12); s.int   = mod(s.int - capo,12); s.int(flag)=12; 
flag    = (a.int==12); a.int   = mod(a.int - capo,12); a.int(flag)=12;
flag    = (t.int==12); t.int   = mod(t.int - capo,12); t.int(flag)=12;
flag    = (b.int==12); b.int   = mod(b.int - capo,12); b.int(flag)=12;

% Where bass notes occur most
[GC,GR] = groupcounts(b.int',-0.5:12.5,'IncludeEmptyGroups',1);
capo_suggestions(GC);




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
        
    
    % Save data to matfile
    flag    = (s.int==12); s.int   = mod(s.int + capo,12); s.int(flag)=12; 
    flag    = (a.int==12); a.int   = mod(a.int + capo,12); a.int(flag)=12;
    flag    = (t.int==12); t.int   = mod(t.int + capo,12); t.int(flag)=12;
    flag    = (b.int==12); b.int   = mod(b.int + capo,12); b.int(flag)=12;
    save(['Songs/',songname,'.mat'],'s','a','t','b','e','e2','ed','ed2','edd','edd2','eddd','eddd2','lyrics','numnotes','capo');
    flag    = (s.int==12); s.int   = mod(s.int - capo,12); s.int(flag)=12; 
    flag    = (a.int==12); a.int   = mod(a.int - capo,12); a.int(flag)=12;
    flag    = (t.int==12); t.int   = mod(t.int - capo,12); t.int(flag)=12;
    flag    = (b.int==12); b.int   = mod(b.int - capo,12); b.int(flag)=12;

    
    switch get(fig,'CurrentKey')
        case 'leftarrow'
            j=max(1,j-1);
        case 'rightarrow'
            j=min(j+1,numnotes);
        case 'p'
            jinput=input('Enter note number: ');
            j=min(numnotes,round(jinput));
            j=max(1,j);
        case 's'
            part = 'soprano';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case 'a'
            part = 'alto';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case 't'
            part = 'tenor';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes;
        case 'b'
            part = 'bass';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case 'r'
            rapidpart=input('Which part for rapid enter? (soprano, alto, tenor, or bass):\n','s');
            if find(contains({'soprano','alto','tenor','bass'},rapidpart))
                part     = rapidpart;
                rapid_len=input('How many notes do you want to input? ');
                rapid_input;
            else
                fprintf('Input wasn"t a part name (soprano, alto, tenor, or bass)\n');
            end
        case '1'
            part = 'e';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case '2'
            part = 'e2';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case '3'
            part = 'ed';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case '4'
            part = 'ed2';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case '5'
            part = 'edd';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case '6'
            part = 'edd2';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case '7'
            part = 'eddd';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case '8'
            part = 'eddd2';
            [x,y]=ginput(1);
            qfret=round(x); qstr=round(y);
            update_notes; 
        case 'backspace' 
            partcell = {'s' 'a' 't' 'b' 'e' 'ed' 'edd' 'eddd' 'e2' 'ed2' 'edd2' 'eddd2'};
            for jj=1:length(partcell)
                eval( strcat(partcell{jj},'.str(j) = 0;') );
            end
        case 'delete'
            userconfirm = input('Do you really want to clear the entire song? If yes, press "y"...\n','s');
            if strcmp(userconfirm,'y')
                partcell = {'s' 'a' 't' 'b' 'e' 'ed' 'edd' 'eddd' 'e2' 'ed2' 'edd2' 'eddd2'};
                for jj=1:length(partcell)
                    eval( strcat(partcell{jj},'.str = zeros(1,',num2str(numnotes),');') );
                end
                fprintf('Song deleted\n');
            else
                fprintf('Song not deleted\n');
            end
        case 'escape'
            j=numnotes+1;
        otherwise
    end
    
end
close all;

% Return .int to original before saving
flag    = (s.int==12); s.int   = mod(s.int + capo,12); s.int(flag)=12; 
flag    = (a.int==12); a.int   = mod(a.int + capo,12); a.int(flag)=12;
flag    = (t.int==12); t.int   = mod(t.int + capo,12); t.int(flag)=12;
flag    = (b.int==12); b.int   = mod(b.int + capo,12); b.int(flag)=12;

save(['Songs/',songname,'.mat'],'s','a','t','b','e','e2','ed','ed2','edd','edd2','eddd','eddd2','lyrics','numnotes','capo');
clearvars;
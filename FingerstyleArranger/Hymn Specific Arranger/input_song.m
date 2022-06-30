%%% Input Song
% Main script for inputting new song notes. Calls "enter_notes.m".
% Enter lyrics and notes. You get opportunity to fix errors. 
% Creates vectors for played_flag, note int, and note name.

clearvars;
close all;


%% Define note2int
noteset={'c' 'cs' 'db' 'd' 'ds' 'eb' 'e' 'f' 'fs' 'gb' 'g' 'gs' 'ab' 'a' 'as' 'bb' 'b'};
intset=[0 1 1 2 3 3 4 5 6 6 7 8 8 9 10 10 11];
note2int=containers.Map(noteset,intset);

%% Enter title and key signature
songname=input('What is the song name?\n','s');
keyint=input('If key has more sharps enter a number. Otherwise hit return... \n');
if isempty(keyint)
    key='flat';
else
    key='sharp';
end

%% Enter lyrics
fprintf('Enter the lyrics for each note\n');
lyrics={};
j=0;
while 1==1
    j=j+1;
    str=input('','s');
    if strcmp(str,'stop')
        break;
    else
        lyrics{j}=str;
    end
end
numnotes=length(lyrics);

%% Enter notes
clc;
fprintf('Enter soprano notes\n');
s=enter_notes(lyrics,key);

clc;
fprintf('Enter alto notes\n');
a=enter_notes(lyrics,key);

clc;
fprintf('Enter tenor notes\n');
t=enter_notes(lyrics,key);

clc;
fprintf('Enter bass notes\n');
b=enter_notes(lyrics,key);

%% Give opportunity to fix errors
notesperline=20;
numpages=ceil( length(lyrics)/notesperline );
ipage=1;

figure(); fig=gcf; set(gcf,'Position',[100,100,1500,600]);
while 1==1
    clf;
    title(['Page ',num2str(ipage),' of ',num2str(numpages)]);
    xlim([0,notesperline+1]); ylim([0,7]); 
    % Plot song and options
    for i=1:min(notesperline,numnotes-(ipage-1)*notesperline)
        text(i,5, lyrics{i+(ipage-1)*notesperline} );
        text(i,4, s.note{i+(ipage-1)*notesperline} );
        text(i,3, a.note{i+(ipage-1)*notesperline} );
        text(i,2, t.note{i+(ipage-1)*notesperline} );
        text(i,1, b.note{i+(ipage-1)*notesperline} );
    end
    text(1,6,'Previous page');
    text(notesperline-2,6,'Next page');
    text(round(notesperline/2-1),6,'Save Song');

    % Automatically go to qinput
    [x,y]=ginput(1);
    x=round(x); y=round(y);
    if y<0
        y=1;
    end
    if x<0
        x=1;
    elseif x>notesperline
        x=notesperline;
    end
    
    if y>=6 %option clicked
        if x<notesperline/4
            ipage=max(1,ipage-1);
        elseif x>3/4*notesperline
            ipage=min(ipage+1,numpages);
        else
            break;
        end
    else
        switch y
            case 5
                newlyric=input('New lyric: ','s');
                lyrics{x+(ipage-1)*notesperline}=newlyric;
            case 4
                breakvar=0;
                while breakvar==0
                    str=input('New note: ','s');
                    if any(strcmp(noteset,str))
                        s.note(x+(ipage-1)*notesperline)={str};
                        breakvar=1;            
                    else
                        fprintf('Not valid note, try again\n');
                    end
                end
            case 3
                breakvar=0;
                while breakvar==0
                    str=input('New note: ','s');
                    if any(strcmp(noteset,str))
                        a.note(x+(ipage-1)*notesperline)={str};
                        breakvar=1;            
                    else
                        fprintf('Not valid note, try again\n');
                    end
                end
            case 2
                breakvar=0;
                while breakvar==0
                    str=input('New note: ','s');
                    if any(strcmp(noteset,str))
                        t.note(x+(ipage-1)*notesperline)={str};
                        breakvar=1;            
                    else
                        fprintf('Not valid note, try again\n');
                    end
                end
            case 1
                breakvar=0;
                while breakvar==0
                    str=input('New note: ','s');
                    if any(strcmp(noteset,str))
                        b.note(x+(ipage-1)*notesperline)={str};
                        breakvar=1;            
                    else
                        fprintf('Not valid note, try again\n');
                    end
                end
        end
    end
end

%add int, played, and str structures.
for j=1:numnotes
    s.int(j)=note2int(s.note{j});
    a.int(j)=note2int(a.note{j});
    t.int(j)=note2int(t.note{j});
    b.int(j)=note2int(b.note{j});
end 
[s.played, s.str, a.played, a.str, t.played, t.str, b.played, b.str, e.played, e.str, e.fret, ed.played, ed.str, ed.fret, ...
    e2.played, e2.str, e2.fret, ed2.played, ed2.str, ed2.fret, edd.played, edd.str, edd.fret, ...
    edd2.played, edd2.str, edd2.fret, eddd.played, eddd.str, eddd.fret,eddd2.played, eddd2.str, eddd2.fret]=deal(zeros(1,numnotes));

save(['Songs/',songname,'.mat'],'s','a','t','b','e','ed','edd','eddd','e2','ed2','edd2','eddd2','lyrics','numnotes');
clearvars;
close('all');
clc;
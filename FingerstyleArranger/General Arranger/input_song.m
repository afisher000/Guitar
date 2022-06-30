%% Input Song
clearvars;
close all;


% map notes to ints
noteset={'c' 'cs' 'db' 'd' 'ds' 'eb' 'e' 'f' 'fs' 'gb' 'g' 'gs' 'ab' 'a' 'as' 'bb' 'b'};
intset=[0 1 1 2 3 3 4 5 6 6 7 8 8 9 10 10 11];
note2int=containers.Map(noteset,intset);


songname=input('What is the song name?\n','s');
keyint=input('If key has more sharps enter a number. Otherwise hit return? (s/f) \n');
if isempty(keyint)
    key='flat';
else
    key='sharp';
end

clc;
fprintf('Enter notes\n');
[melody bass]=enter_notes(key);
numnotes=size(bass.note,1);

%add int, played, and str structures.
for j=1:size(bass.note,1)
    if isempty(melody.note{j})
        melody.int(j)=-1;
    else
        melody.int(j)=note2int(melody.note{j});
    end
    for jj=1:size(bass.note,2)
        if isempty(bass.note{j,jj})
            bass.int{j,jj}=-1;
        else
            bass.int{j,jj}=note2int(bass.note{j,jj});
        end
    end
end 
melody.played=zeros(1,numnotes);
melody.str=zeros(1,numnotes);
bass.played=zeros(numnotes,size(bass.note,2));
bass.str=zeros(numnotes,size(bass.note,2));

save(['Songs/',songname,'.mat'],'melody','bass','numnotes');
% clearvars;
% close('all');
% clc;

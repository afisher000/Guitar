% Combine songs to one large song

clearvars;
close all;

songcell={'song1' 'song2' '...'};

basscell=cell(1,length(songcell));
melodycell=cell(1,length(songcell));
largestchord=0;

for j=1:length(songcell)
    load(['Songs\',songcell{j},'mat']);
    basscell{j}=bass;
    melodycell{j}=melody;
    largestchord=max(largestchord,size(bass.note,2));
end

bass.note={};   bass.int={};    bass.played=[];     bass.str=[];
melody.note={}; melody.int=[];  melody.played=[];   melody.str=[];

% Need to make sure all size(basscell{j},2) are the same. 
for j=1:length(songcell)
    
    try
        bass.note{1,largestchord};
    catch
        bass.note{ size(bass.note,1) , largestchord } =[];
    end
    
    try
        bass.int{1,largestchord};
    catch
        bass.int{ size(bass.int,1) , largestchord } =[];
    end
    try
        bass.played(1,largestchord);
    catch
        bass.played( size(bass.played,1) , largestchord ) =0;
    end
    try
        bass.str(1,largestchord);
    catch
        bass.str( size(bass.str,1) , largestchord ) =0;
    end
    
    bass.note       = [bass.note    ; basscell{j}.note];
    bass.int        = [bass.int     ; basscell{j}.int];
    bass.played     = [bass.played  ; basscell{j}.played];
    bass.str        = [bass.str     ; basscell{j}.str];
    
    melody.note     = [melody.note  , melodycell{j}.note];
    melody.int      = [melody.int   , melodycell{j}.int];
    melody.played   = [melody.played, melodycell{j}.played];
    melody.str      = [melody.str   , melodycell{j}.str];
end

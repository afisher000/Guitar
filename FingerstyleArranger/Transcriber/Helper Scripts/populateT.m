%% Populates T table with measure, beat, string and fret.
params(); 

%% Compute estimate measure/beat from anchortimes
for j=1:height(T)
    [~,idx] = min(abs(T.Time(j) - anchortimes));
    idx         = idx-1; %math easier when counting index from 0
    stripmeas   = mod(idx,4*bpm);
    T.Measure(j)= (idx-stripmeas)/(4*bpm);
    T.Beat(j)   = (stripmeas)*.25;
end

%% Compute string/fret from notenum
strnotes    = [24 19 15 10 5 0];
for j=1:height(T)
    fretvec = T.NoteNum(j)-strnotes;
    T.String(j) = find( fretvec>=capo , 1 , 'first'); %use lowest string possible
    T.Fret(j)   = fretvec(T.String(j));
end

%% Make sure fret>=capo
scn     = (T.Fret<capo);
if sum(scn)>0
    idxs     = find(scn);
    for j=1:length(idxs)
        idx     = idxs(j);
        try
            fret    = notestr2fret(T.NoteNum(idx),T.String(idx)+1);
        catch %error thrown
            errormsg('Capo value is not possible with current fret constraints');
        end
        T.String(idx)   = T.String(idx)+1;
        T.Fret(idx)     = fret;
    end
end

%% Resolve any overlapping notes
for iterate = 1:6 %overlaps can be created, need to iterate
    score       = (T.Measure*bpm + T.Beat)*1000 + T.String; %fretboard location maps uniquely to score
    [sortedscore,I] = sort(score,'ascend');

    Tidxvec      = I( find(~diff(sortedscore)) ); %location of duplicated values in T
    for j=1:length(Tidxvec) %find scores are identical
       Tidx  = Tidxvec(j);
       scn  = logical( (T.Measure==T.Measure(Tidx)) .* (T.Beat==T.Beat(Tidx)) .* (T.String==T.String(Tidx)) );
       Tidx_duplicates = find(scn);
       [~,idx]  = min(T.Fret(Tidx_duplicates)); %move smaller fret value
       Tidx      = Tidx_duplicates(idx);
       try 
           fret = notestr2fret(T.NoteNum(Tidx),T.String(Tidx)+1);
       catch
           errormsg('Can not reassign overlapping notes...');
       end
       T.String(Tidx)    = T.String(Tidx)+1;
       T.Fret(Tidx)      = fret;
    end
end
%Manual Entry of Note
T( logical((T.Measure==curmeas) .* (T.Beat==curbeat) .* (T.String==curstr)) , : ) = [];

if curfret>=0 %negative curfret deletes note
    T.Measure(end+1)    = curmeas;
    T.Beat(end)         = curbeat;
    T.String(end)       = curstr;
    T.Fret(end)         = curfret+capo;
    openstrings = [24 19 15 10 5 0];
    T.NoteNum(end)      = openstrings(curstr) + curfret + capo + tuning(curstr);
    playtone(T.NoteNum(end));
end
save([matfolder, songname,'.mat'],'T','-append');

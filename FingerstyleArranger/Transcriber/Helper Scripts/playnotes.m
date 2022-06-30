% Play notes at current location
scn     = logical((T.Measure==curmeas) .* (T.Beat==curbeat));
notenums= T.NoteNum(scn);
for j=1:length(notenums)
    playtone(notenums(j));
end




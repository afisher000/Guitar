function fret = notestr2fret(note,str)
if ~ismember(str,1:6)
    errormsg('String number is not valid\n');
end

openstrings     = [24 19 15 10 5 0];
fret            = note - openstrings(str);
if fret<0 || fret>16
    errormsg('Fret<0 or Fret>16\n');
end
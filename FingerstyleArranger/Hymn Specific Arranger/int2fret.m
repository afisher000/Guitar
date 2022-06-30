function fret=int2fret(str,int,part)
if int==12 %note not played, silence
    fret = -1;
    return;
end

switch str
    case 1
        fret=int-4;
    case 2
        fret=int-9;
    case 3
        fret=int-2;
    case 4
        fret=int-7;
    case 5
        fret=int-11;
    case 6
        fret=int-4;
    otherwise
        errormsg('Non-valid string value\n');
end
fret=mod(fret,12);

%Add shift so parts don't overlap
switch part
    case 's'
        dfret=+0.08;
    case 'a'
        dfret=+0.02;
    case 't'
        dfret=-0.02;
    case 'b'
        dfret=-0.08;
    otherwise
        errormsg('Non-valid part char identifier\n');
end

fret=fret+dfret;
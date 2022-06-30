function playchord(T,curtime)
%% Play notes on cursor line
[y,Fs]=audioread('guitarnote_A#.wav');

%% Loop through table
tvec    = (1:Fs)/Fs;
Y       = zeros(1,Fs);
taper   = 3;
scn     = (T.Time==curtime);
notevec = T.NoteNum(scn);
for j=1:length(notevec)
    notenum = notevec(j);
    Fsnew   = round(Fs*(2^((notenum-18)/12)));
    % Sum 1 second clips of frequency shifted notes
    Y       = Y + interp1((1:Fsnew)/Fsnew , y(1:Fsnew)' .* exp(-taper*(1:Fsnew)/Fsnew) , tvec,'linear',0);
end
sound(Y,Fs);

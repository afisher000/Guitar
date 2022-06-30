%% Write guitar string audio files
[y,Fs]  = audioread('guitarnote_A#.wav');

for notenum = 0
    taper   = 3;
    Fsnew   = round(Fs*(2^((notenum-18)/12)));
    Y       = interp1( (1:Fsnew)/Fsnew , y(1:Fsnew)' .* exp(-taper*(1:Fsnew)/Fsnew) , (1:Fs)/Fs ,'linear',0);

    sound(Y,Fs);
    audiowrite(['Guitar Notes/Note',num2str(notenum),'.wav'],Y,Fs)
end
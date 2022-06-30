function playsection(T,tmin,tmax)
%% Play song section
[y,Fs]=audioread('guitarnote_A#.wav');

%% Loop through table
tvec    = tmin + (1:(tmax-tmin)*Fs)/Fs;
Y       = zeros(1,(tmax-tmin)*Fs);
taper   = 3;
for j=1:height(T)
    Fsnew   = round(Fs*(2^((T.NoteNum(j)-18)/12)));
    % Sum 1 second clips of frequency shifted notes
    Y       = Y + interp1( T.Time(j) + (1:Fsnew)/Fsnew , y(1:Fsnew)' .* exp(-taper*(1:Fsnew)/Fsnew) , tvec,'linear',0);
end

sound(Y,Fs);

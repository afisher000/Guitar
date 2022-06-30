function playtone(notenum)
%% Notenum = 0 for low E.

%% Recorder guitar A note
[y,Fs]=audioread('guitarnote_A#.wav');

% Scale Fs to play different notes
Fs          = round(Fs*(2^((notenum-18)/12))); %18 is notenum of A# file

% Taper signal to 1 sec
taper       = 3; %manually adjusted
sound( y(1:Fs)' .* exp(-taper*(1:Fs)/Fs) , Fs); 

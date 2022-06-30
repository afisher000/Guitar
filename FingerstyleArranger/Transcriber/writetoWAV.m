% Create WAV file for completed song
songname = 'Annies Song';
params(); 
[y,Fs]  = audioread('guitarnote_A#.wav');
taper       = 3;
BPM         = 120;
songbuffer  = 2; %2 seconds at beginning at end
%% Loop through notes
TMAX    = max(T.Measure+1) * bpm * (60/BPM); %convert total beats to seconds
time    = 0:1/Fs:TMAX;
Y       = zeros(1,length(time));

%% Add NoteNum and Time categories
openstrings = [24 19 15 10 5 0];
T.NoteNum   = openstrings(T.String)' + T.Fret + capo + tuning(T.String)';
T.Time      = (T.Measure * bpm + T.Beat) * (60/BPM);
    
%% Add notes to WAV file
for j=1:height(T)
    Fsnew   = round(Fs*(2^((T.NoteNum(j)-18)/12)));
    % Sum 1 second clips of frequency shifted notes
    Y       = Y + interp1( T.Time(j) + (1:Fsnew)/Fsnew , y(1:Fsnew)' .* exp(-taper*(1:Fsnew)/Fsnew) , time ,'linear',0);
    
    clc;
    fprintf('Creating WAV: %d%%\n',round(j/height(T)*100));
end

%% Add buffer, write to file
Y   = [zeros(1,songbuffer*Fs),Y,zeros(1,songbuffer*Fs)];
audiowrite([transcribedwavfolder,songname,'.wav'],Y,Fs);



% Resource for midi byte encoding
% http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html
clearvars;

% Analyze WAV
addpath('F:\Personal Projects\FingerstyleArranger\Transcriber\Helper Scripts');

%% Read songfile
songname = 'Jesus Walked This Lonesome Valley';
% Check if song exists
% if isfile(['F:\Personal Projects\FingerstyleArranger\Transcriber\Song Matfiles\',songname,'.mat'])
%     error('This song already exists. Is this another arrangement?')
% end
% initializesong;
params;
[data, byteCount] = fread(fopen([MIDIfolder,songname,'.mid']));

%%
formattype  = data(10);
numtracks   = data(12);
ticksPerQNote = polyval(data(13:14),256); %ticks per 1/4 note encoded as bytes 13+14

% Initialize values
chunkIndex = 14;     % Header chunk is always 14 bytes
ts = 0;              % Timestamp - Starts at zero                 
notevec = [];
timevec = [];

% Parse track chunks in outer loop
while chunkIndex < byteCount
    % Read header of track chunk, find chunk length   
    % Add 8 to chunk length to account for track chunk header length
    chunkLength = polyval(data(chunkIndex+(5:8)),256)+8;
    
    ptr = 8+chunkIndex;             % Determine start for MIDI event parsing
    statusByte = -1;                % Initialize statusByte. Used for running status support
    
    % Parse MIDI track events in inner loop
    while ptr < chunkIndex+chunkLength
        % Read delta-time
        [deltaTime,deltaLen] = findVariableLength(ptr,data);  
        % Push pointer to beginning of MIDI message
        ptr = ptr+deltaLen;
        
        % Read MIDI message
        [statusByte,messageLen,message] = interpretMessage(statusByte,ptr,data);
        % Extract relevant data - Create midimsg object
        [ts,msg] = createMessage(message,ts,deltaTime,ticksPerQNote);
        
        %% If note pressed:
        try
            if message(1)==144 && message(3)>0 %Velocity must be >0
                notevec(end+1)  = message(2);
                timevec(end+1)  = ts;
            end
        catch
        end
        
        % Push pointer to next MIDI message
        ptr = ptr+messageLen;
    end
    
    % Push chunkIndex to next track chunk
    chunkIndex = chunkIndex+chunkLength;
end

%% Find approximate beats
timevec     = timevec-min(timevec);
[Ncounts,edges]   = histcounts(diff(timevec),linspace(500,2000,length(timevec)/10));
ctr         = edges(1:end-1)/2 + edges(2:end)/2;
[~, idx]    = max(Ncounts);
beatvec     = timevec/ctr(idx);
figure(); plot(ctr,Ncounts);
figure();
scatter(beatvec,notevec)

%% Save to Matfile
BPM         = 120; %arbitrary
anchortimes = 0 : 0.25*(60/BPM) : max(beatvec)*(60/BPM);
for j=1:length(notevec)
    T.NoteNum(j)   = notevec(j) - 40; %Low E on guitar is midinote 40
    T.Time(j)      = beatvec(j) * (60/BPM); 
end
save([matfolder,songname,'.mat'],'T','bpm','anchortimes','-append');

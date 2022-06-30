% Initialize Matfile
clearvars;
fprintf('Song needs to be initialized\n');
songname    = input('Type the song name...\n','s');
bpm     = str2num( input('How many beats in a measure? ','s') );

if ~ismember(bpm,1:8)
    errormsg('Incorrect input for beats per measure.');
end

folder  = 'F:\Personal Projects\FingerstyleArranger\Transcriber\Song Matfiles\';
T       = table('Size',[0 6],'VariableTypes',repmat({'double'},1,6));
T.Properties.VariableNames = {'Time','NoteNum','Measure','Beat','String','Fret'};
capo    = 0;
tuning  = [0 0 0 0 0 0];
BPM     = 110; %Beats per minute

save([folder,songname,'.mat'],'T','BPM','bpm','capo','tuning');
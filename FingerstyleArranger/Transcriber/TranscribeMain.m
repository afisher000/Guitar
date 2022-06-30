% TranscribeMain
addpath('F:\Personal Projects\FingerstyleArranger\Transcriber\Helper Scripts');
format long;
songname = 'Annies Song';
try
    params;
    if ~sum(T.Beat) %Populate from AnalyzeWAV
        populateT; %fill in Measure,Beat,String, and Fret
        save([matfolder,songname,'.mat'],'T','-append');
    end
catch
    initializesong;
    params;
end
capo = 0;
exitflag = 1;
figure(1); fig=gcf; set(gcf,'Position',[100,100,1600,900]);
ax=axes('Parent',fig);
while exitflag
    clf; 
    hold on; 
    plottab();
    hold off;

    %% Wait for button
    keypress=0;
    while keypress==0
        keypress=waitforbuttonpress;
    end

    switch get(fig,'CurrentKey') 
        case 'pageup'
            curmeas = max(0,curmeas-meas_line);
        case 'pagedown'
            curmeas = curmeas+meas_line;
        case 'comma'
            idx         = find(stepsize==stepsizevec);
            stepsize    = stepsizevec( max(1,idx-1) );
        case 'period'
            idx         = find(stepsize==stepsizevec);
            stepsize    = stepsizevec( min(length(stepsizevec),idx+1) );
        case 'leftarrow'
            curpos  = curmeas*bpm + curbeat;
            curpos  = max(0,curpos-stepsize);
            curmeas = floor(curpos/bpm);
            curbeat = mod(curpos,bpm);
            curbeat = round(curbeat*minstepfac)/minstepfac;
            if playmode
                playnotes;
            end

        case 'rightarrow' %forward 1/8 beat
            curpos  = curmeas*bpm + curbeat;
            curpos  = curpos+stepsize;
            curmeas = floor(curpos/bpm);
            curbeat = mod(curpos,bpm);
            curbeat = round(curbeat*minstepfac)/minstepfac;
            if playmode
                playnotes;
            end
        
        case 'uparrow' %go to higher string
            curstr = max(curstr-1,1);
        case 'downarrow' %go to lower string
            curstr = min(curstr+1,6);
            
        %% Shift all later notes
        case 's'
            curpos  = curmeas*bpm + curbeat;
            Tpos    = T.Measure*bpm + T.Beat;
            scn     = (Tpos>=curpos);
            Tpos(scn) = Tpos(scn) + stepsize;
            T.Measure = floor(Tpos/bpm);
            T.Beat  = mod(Tpos,bpm);
            save([matfolder, songname,'.mat'],'T','-append');
        case 'a'
            curpos  = curmeas*bpm + curbeat;
            Tpos    = T.Measure*bpm + T.Beat;
            scn     = (Tpos>=curpos);
            Tpos(scn) = max(0, Tpos(scn) - stepsize);
            T.Measure = floor(Tpos/bpm);
            T.Beat  = mod(Tpos,bpm);
            save([matfolder, songname,'.mat'],'T','-append');
        
        %% Enter note manually
        case '0'
            curfret = 0;
            manualentry();
        case '1'
            curfret = 1;
            manualentry();
        case '2'
            curfret = 2;
            manualentry();
        case '3'
            curfret = 3;
            manualentry();
        case '4'
            curfret = 4;
            manualentry();
        case '5'
            curfret = 5;
            manualentry();
        case '6'
            curfret = 6;
            manualentry();
        case '7'
            curfret = 7;
            manualentry();
        case '8'
            curfret = 8;
            manualentry();
        case '9'
            curfret = 9;
            manualentry();
        case 'o'
            curfret = 10;
            manualentry();
        case 'q'
            curfret = 11;
            manualentry();
        case 'w'
            curfret = 12;
            manualentry();
        case 'e'
            curfret = 13;
            manualentry();
        case 'r'
            curfret = 14;
            manualentry();
            
        %% Copy measure to clipboard
        case 'c'
            num_meas   = input('How many measures to copy? ');
            if ~ismember(num_meas,1:8)
                fprintf('Input must be integer from 1 to 8\n');
                continue;
            end
            scn     = ismember(T.Measure, curmeas:(curmeas+num_meas-1));
            clipboard = T(scn,:);
            clipboard.Measure = clipboard.Measure - curmeas*ones(height(clipboard),1); % reference clipboard.measure to 0
            
        case 'v'
            clipboard.Measure = clipboard.Measure + curmeas*ones(height(clipboard),1);
            scn     = ismember(T.Measure, curmeas:(curmeas+num_meas-1)); % clear previous notes
            T(scn,:)=[];
            T = [T; clipboard];
            clipboard = [];
            save([matfolder, songname,'.mat'],'T','-append');
            
        %% Remove notes
        case 'backspace' %single note
            curfret = -1;
            manualentry();
        case 'delete' %delete measures
            num_meas    = input('How many measures to delete? ');
            if ~ismember(num_meas,1:8)
                fprintf('Input must be integer from 1 to 8\n');
                continue;
            end
            userinput = input('Confirm deleting measures by typing "yes": ','s');
            if strcmp(userinput,'yes')
                scn     = ismember(T.Measure, curmeas:(curmeas+num_meas-1));
                T(scn,:)=[];
            end
            save([matfolder, songname,'.mat'],'T','-append');
            
        %% Toggle play mode
        case 'p'
            playmode = ~playmode;
            if playmode
                playnotes;
            end
            
        %% Toggle fast mode
        case 'f'
            fastmode = ~fastmode;
            
        %% Exit loop
        case 'escape'
            exitflag=0;
            save([matfolder, songname,'.mat'],'T','-append');
            close all;
    end
end
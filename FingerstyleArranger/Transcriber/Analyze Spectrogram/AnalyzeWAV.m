% Analyze WAV
addpath('F:\Personal Projects\FingerstyleArranger\Transcriber\Helper Scripts');

%% Read songfile
songname = 'Test';
try
    params;
catch
    initializesong;
    params;
    definebeats;
end
[song,Fs] = audioread([origwavfolder,songname,'.wav']);

%% While loop
exitflag    = 1;
fig = figure('units','normalized','outerposition',[0 0 1 1]);

while exitflag
    y           = song(1+floor(Fs*tmin) : floor(Fs*tmax) );
    L           = length(y);

    %% Plot
    clf;
    hold on;
    plotfreqdomain;
    plot(T.NoteNum,T.Time,'r*'); 
    hold off;
    
    %% Wait for button
    % 1 for keyboard, 0 for mouseclick
    event_type   = waitforbuttonpress;
    
    %% Keyboard
    if event_type
        
        switch get(fig,'CurrentKey') 
        case 'j' %jump to specific time
            usertime   = input('Where to jump in song?');
            if usertime>TMAX-tspan
                tmin = TMAX-tspan;
                tmax = TMAX;
            elseif usertime<0
                tmin = 0;
                tmax = tspan;
            else
                tmin = usertime;
                tmax = usertime+tspan;
            end

        case 'uparrow' %move up 1 second
            if tmax<TMAX
                tmin=tmin+1;
                tmax=tmax+1;
            end

        case 'downarrow' %move down 1 second
            if tmin<1
                tmin=0;
                tmax=tspan;
            else
                tmin=tmin-1;
                tmax=tmax-1;
            end

        case 'p' %playback entered notes
            playsection(T,tmin,tmax);

        case 'l' %listen to song
            sound(y,Fs);

        case 'escape' %Exit loop
            exitflag=0;
            close all;
        end
    end
    
    %% Mouseclick
    if ~event_type
        
        %get cursor location
        C   = get(gca, 'CurrentPoint');
        xclick = C(1,1); yclick = C(1,2); 
        
        %check figure bounds
        if xclick<Nmin || xclick>Nmax || yclick>tmax || yclick<tmin
            disp('Bad Click Location');
            continue;
        end
        
        %get nearest note/anchortime
        clicknote   = round(xclick); 
        [~,idx]     = min(abs(yclick-anchortimes));
        clicktime   = anchortimes(idx);
        
        % get scns
        note_scn    = (T.NoteNum == clicknote);
        time_scn    = (T.Time == clicktime);
        
        switch get(fig,'SelectionType')
        case 'normal' %leftclick, add note
            
             %if no intersection with table
            if ~sum(note_scn.*time_scn)
                T.Time(end+1)   = clicktime;
                T.NoteNum(end)  = clicknote;
                playtone(clicknote);
                save([matfolder,songname,'.mat'],'T','-append');
            end
                
        case 'alt' %rightclick, remove note
            
            %if intersection with table
            if sum(note_scn.*time_scn) 
                idx     = logical( note_scn.*time_scn );
                T(idx,:)=[];
                save([matfolder,songname,'.mat'],'T','-append');
            end

        case 'extend' % middleclick, hear note pitch
            playtone(clicknote);
        end
    end
end


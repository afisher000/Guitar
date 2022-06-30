% DefineStrings
clearvars;
addpath('F:\Personal Projects\FingerstyleArranger\Transcriber\Helper Scripts');
songname = 'Godfather Theme';
params();

%%
if ~sum(T.Beat)
    populateT; %fill in Measure,Beat,String, and Fret
    save([matfolder,songname,'.mat'],'T','-append');
end

exitflag = 1;
figure(); fig=gcf; 
set(gcf,'Position',[100,100,1600,900]);

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
        %% Move Forward/Backward
        case 'pageup' %previous line on tab
            curmeas = max(0,curmeas-meas_line);
        case 'pagedown' %next line on tab
            curmeas = curmeas+meas_line;
        case 'comma' %backward full measure
            curmeas = max(0,curmeas-1);
        case 'period' %forward full measure
            curmeas = curmeas+1;
        case 'leftarrow' %back 1/8 beat
            % Already at beginning
            if curmeas==0 && curbeat<0.5
                curbeat = 0;
                continue;
            end
            % At start of measure
            if curbeat<0.5 && curmeas>0
                curmeas=curmeas-1;
            end
            curbeat = mod(curbeat-0.5,bpm);
            
        case 'rightarrow' %forward 1/8 beat
            if curbeat>=bpm-0.5
                curmeas=curmeas+1;
            end
            curbeat = mod(curbeat+0.5,bpm);
            
        case 'n' %back 1/16 beat
            % Already at beginning
            if curmeas==0 && curbeat==0
                continue;
            end
            % At start of measure
            if curbeat<0.25 && curmeas>0
                curmeas=curmeas-1;
            end
            curbeat = mod(curbeat-0.25,bpm);

        case 'm' %forward 1/16 beat
            if curbeat>=bpm-0.25
                curmeas=curmeas+1;
            end
            curbeat = mod(curbeat+0.25,bpm);

        case 'uparrow' % move up one string
            curstr = max(curstr-1,1);
            
        case 'downarrow' % move down one string
            curstr = min(curstr+1,6);
           
        case 'u' % play note on higher string
            scn     = logical( (curstr==T.String).* (curmeas==T.Measure) .* (curbeat==T.Beat) ); 
            if sum(scn)>0
                idx     = find(scn,1);
                try
                    fret    = notestr2fret(T.NoteNum(idx),T.String(idx)-1);
                catch %error thrown
                    continue;
                end
                T.String(idx)   = T.String(idx)-1;
                T.Fret(idx)     = fret;
            end
            save([matfolder, songname,'.mat'],'T','-append');
            
        case 'd' % play note on lower string
            scn     = logical( (curstr==T.String).* (curmeas==T.Measure) .* (curbeat==T.Beat) ); 
            if sum(scn)>0
                idx     = find(scn,1);
                try
                    fret    = notestr2fret(T.NoteNum(idx),T.String(idx)+1);
                catch %error thrown
                    continue;
                end
                T.String(idx)   = T.String(idx)+1;
                T.Fret(idx)     = fret;
            end
            save([matfolder, songname,'.mat'],'T','-append');
        
        case 'f' %toggle fastmode
            fastmode = ~fastmode;
            
        case 'escape' % Exit loop
            exitflag=0;
            close all;
    end
    
end




% plotTab


lines_page      = 8;
measure_line    = 12;
xmax            = 100*measure_line;
ymax            = 0;
staffspacing    = 4;
dx              = .25; %Length of beat shift to avoid numbers on lines

%% Plot Staff (comment out j loop to plot only one line (faster))
title(songname);
cury    = 1;
for j=1:lines_page 
    %% Option to only plot current line (skip others)
    if fastmode
        jquick = floor(curmeas/measure_line+1);
        if j~=jquick
            cury = cury + 6 + staffspacing;
            continue;
        end
    end
    
    %% Thick Vertical Lines
    plot([0 0],-[cury cury+5],'k');
    for jj=1:measure_line
       plot(jj*[100 100], -[cury cury+5],'k');
    end
    
    % Faint Vertical lines
    if ~fastmode
        for xval = round(100*.25/bpm:100/bpm:xmax)
            plot([xval xval], -[cury cury+5],'color',.9*[1 1 1]);
        end
    end
    
    %% Horizontal Lines
    for jj=1:6 
        plot([0 xmax],-[cury cury],'k');
        cury    = cury+1;
    end
    
    %% Staff Spacing
    if j<lines_page
        cury    = cury + staffspacing;
    end
end

%% Add notes
if fastmode
    leftmeas    = curmeas-mod(curmeas,measure_line);
    scn     = ismember(T.Measure, leftmeas:leftmeas+measure_line-1); %.plot notes for one line
else
    scn     = (T.Measure>-100); %plot all notes
end
Tscn    = T(scn,:);
for j=1:height(Tscn)
    jmeas   = Tscn.Measure(j);
    jbeat   = Tscn.Beat(j);
    jstr    = Tscn.String(j);
    jfret   = Tscn.Fret(j);
    xval    = 100*( mod(jmeas,measure_line) + jbeat/bpm) + 100*dx/bpm; %Notes should be offset
    yval    = jstr + floor(jmeas/measure_line) * (6+staffspacing);
    if jfret<10
        text(xval-2,-yval,num2str(jfret),'FontSize',13);
    else
        text(xval-5,-yval,num2str(jfret),'FontSize',13);
    end
end

%% Add location carat
jmeas   = curmeas;
jbeat   = curbeat;
xval    = 100*( mod(jmeas,measure_line) + jbeat/bpm) + 100*dx/bpm; %Notes should be offset
yval    = 7 + floor(jmeas/measure_line) * (6+staffspacing);
text(xval,-yval,'^','Color','blue','FontSize',10);

%% Add location *
jmeas   = curmeas;
jbeat   = curbeat;
xval    = 100*( mod(jmeas,measure_line) + jbeat/bpm) + 100*dx/bpm; %Notes should be offset
yval    = curstr + floor(jmeas/measure_line) * (6+staffspacing);
text(xval,-yval,'*','Color','blue','FontSize',13);

%% Adjust Figure Properties
set(gca,'XTick',[],'YTick',[],'XColor','none','YColor','none');
xlim([0 xmax]); ylim(-[lines_page*(6+staffspacing) 0]);


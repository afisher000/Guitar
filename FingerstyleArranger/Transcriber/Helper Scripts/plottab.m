% plotTab2
meas_page       = meas_line*lines_page;
measurewidth    = measurebuffer + 100;
xmax            = measurewidth * meas_line;
ymax            = 1 + lines_page * 6 + (lines_page-1)*staffbuffer;
curpage         = floor(curmeas/meas_page);
curline         = mod(floor(curmeas/meas_line),lines_page);
curblock        = mod(curmeas,meas_line);
staffstart      = 1 + (0:lines_page-1)*(6+staffbuffer);


%% Define Figure Properties
set(gca,'XTick',[],'YTick',[],'XColor','none','YColor','none');
xlim([0 xmax]); ylim([-ymax 0]);
title(songname);

%% Parameter/Options readout
readout     = sprintf('curmeas=%i    curbeat=%.2f    stepsize=%.2f    capo=%i    fastmode=%i    playmode=%i',curmeas,curbeat,stepsize,capo,fastmode,playmode);
options     = sprintf(strcat('Change String\nup/down\n\n',...
    'Change Position:\nleft/right\n\n',...
    'Change Stepsize:\n</>\n\n',...
    'Change Line:\npageup/pagedown\n\n',...
    'Enter Note:\n0-14 = 0-9,O,Q,W,E,R\n\n',...
    'Shift Notes:\na/s\n\n',...
    'Copy/Paste Measures:\nc/v\n\n',...
    'Delete Note:\nbackspace\n\n',...
    'Delete Measures:\ndelete\n\n',...
    'Toggle Fastmode:\nf\n\n',...
    'Toggle Playmode:\np\n\n',...
    'Exit:\nescape\n\n'));
    
if ~plotPDF
    text(xmax/2,-(ymax+2),readout,'FontSize',13,'HorizontalAlignment','Center');
    text(-xmax/10,-(ymax/2),options,'FontSize',10,'HorizontalAlignment','Center');
end

%% Plot beats in curmeas
if ~plotPDF
    x0              = measurebuffer + curblock*measurewidth;
    y0              = staffstart(curline+1);
    xtemp           = reshape(repmat(0:100/bpm:100,3,1),1,[]);
    ytemp           = repmat([0 5 0],1,bpm+1);
    plot(x0+xtemp,-(y0+ytemp),'color',.9*[1 1 1]);
end

%% Plot staff
xtemp           = [ repmat([0 xmax 0],1,6) , reshape(repmat(0:measurewidth:xmax,3,1),1,[]) ];
ytemp           = [ reshape(repmat(0:5,3,1),1,[]) , repmat([0 5 0],1,meas_line+1) ];
for j=1:length(staffstart)
    plot(xtemp,-(ytemp+staffstart(j)),'color',rgb);
end

%% Add notes
% use scn to control what notes are plotted
N.page  = floor(T.Measure/meas_page);
N.line  = mod(floor(T.Measure/meas_line),lines_page);
N.block = mod(T.Measure,meas_line);
N.x     = (measurebuffer + N.block*measurewidth) + (T.Beat/bpm*100); %x varies with block,beat
N.y     = (staffstart(N.line+1)') + (T.String-1) - dy; %y varies with line,string

if plotPDF
    curpage     = PDFpage;
    scn     = logical( N.page == curpage );
elseif fastmode
    scn     = logical( (N.page == curpage).*(N.line == curline) );
else
    scn     = logical( N.page == curpage );
end

if plotPDF % put white background behind note when printing
    scn_1digit  = logical( ((T.Fret-capo)<10) .* scn );
    scn_2digit  = logical( ((T.Fret-capo)>=10) .* scn );
    % Plot single digit notes
    text(N.x(scn_1digit),-N.y(scn_1digit)-dy,'  ','FontSize',8,'HorizontalAlignment','Center','BackgroundColor',ones(1,3),'Margin',.01);
    text(N.x(scn_1digit),-N.y(scn_1digit),num2str(T.Fret(scn_1digit)-capo),'FontSize',10,'HorizontalAlignment','Center');
    % Plot double digit notes
    text(N.x(scn_2digit),-N.y(scn_2digit)-dy,'    ','FontSize',8,'HorizontalAlignment','Center','BackgroundColor',ones(1,3),'Margin',.01);
    text(N.x(scn_2digit),-N.y(scn_2digit),num2str(T.Fret(scn_2digit)-capo),'FontSize',10,'HorizontalAlignment','Center');
else
    text(N.x(scn),-N.y(scn),num2str(T.Fret(scn)-capo),'FontSize',10,'HorizontalAlignment','Center');
end


if ~plotPDF
    %% Add location carat
    xtemp   = (measurebuffer + curblock*measurewidth) + (curbeat/bpm*100);
    ytemp   = staffstart(curline+1) + 6;
    text(xtemp,-ytemp,'^','Color','blue','FontSize',10,'HorizontalAlignment','Center');

    %% Add location star
    xtemp   = (measurebuffer + curblock*measurewidth) + (curbeat/bpm*100);
    ytemp   = staffstart(curline+1) + (curstr-1);
    text(xtemp,-ytemp,'*','Color','blue','FontSize',15,'HorizontalAlignment','Center');
end


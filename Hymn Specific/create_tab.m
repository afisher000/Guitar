%create tab
close all;
% Formatting parameters
linebuffer=2;
lyricbuffer=1;
notesperline=14;
linesperpage=4;
notesperpage=notesperline*linesperpage;


songname='Father lead me day by day'
load(['Songs/',songname,'.mat']);
%Capo is saved in mat file.

% Transpose without changing 12 elements (indicates silence)
flag    = (s.int==12); s.int   = mod(s.int - capo,12); s.int(flag)=12; 
flag    = (a.int==12); a.int   = mod(a.int - capo,12); a.int(flag)=12;
flag    = (t.int==12); t.int   = mod(t.int - capo,12); t.int(flag)=12;
flag    = (b.int==12); b.int   = mod(b.int - capo,12); b.int(flag)=12;

numpages=ceil(numnotes/notesperpage);
for ipage=1:numpages
    
    figure(); movegui('center'); hold on;
    % plot tab lines for page
    for i=1:linesperpage
        shift=(i-1)*(6+linebuffer+lyricbuffer);
        for istr=1:6 
            plot([0,notesperline+1],[-istr-shift,-istr-shift],'k');
        end
        plot([0,0],[-1-shift,-6-shift],'k');
        plot([notesperline+1,notesperline+1],[-1-shift,-6-shift],'k');
    end

    %Loop over notes for ipage
    jstart=1+(ipage-1)*notesperpage;
    jend=jstart+notesperpage-1;
    jend=min(jend,numnotes);
    for j=jstart:jend
        q=floor( (j-1) /notesperline);
        r=round( (j) - q*notesperline);
        q=q-(ipage-1)*linesperpage;
        x=r;

        for istr=1:6
            %note 7-istr because the lines are mirrored over y=0
            y=-1*( (7-istr) +q*(6+linebuffer+lyricbuffer) );
            if b.str(j)==istr
                text(x,y,num2str( round(int2fret(istr,b.int(j),'b')) ),'FontSize',13);
            elseif t.str(j)==istr
                text(x,y,num2str( round(int2fret(istr,t.int(j),'t')) ),'FontSize',13);
            elseif a.str(j)==istr
                text(x,y,num2str( round(int2fret(istr,a.int(j),'a')) ),'FontSize',13);
            elseif s.str(j)==istr
                text(x,y,num2str( round(int2fret(istr,s.int(j),'s')) ),'FontSize',13);
            elseif e.str(j)==istr
                text(x,y,num2str( e.fret(j) ),'FontSize',13);
            elseif e2.str(j)==istr
                text(x,y,num2str( e2.fret(j) ),'FontSize',13);
            end
            
            if ed.str(j)==istr
                text(x+.25,y,num2str( ed.fret(j) ),'FontSize',13);
            elseif ed2.str(j)==istr
                text(x+.25,y,num2str( ed2.fret(j) ),'FontSize',13);
            end
            
            if edd.str(j)==istr
                text(x+.5,y,num2str( edd.fret(j) ),'FontSize',13);
            elseif edd2.str(j)==istr
                text(x+.5,y,num2str( edd2.fret(j) ),'FontSize',13);
            end
            
            if eddd.str(j)==istr
                text(x+.75,y,num2str( eddd.fret(j) ),'FontSize',13);
            elseif eddd2.str(j)==istr
                text(x+.75,y,num2str( eddd2.fret(j) ),'FontSize',13);
            end
           

        end

        % plot lyric
        y=-1*(6+lyricbuffer+q*(6+linebuffer+lyricbuffer) );
        text(x,y,lyrics{j});
    end
    set(gca,'XTick',[],'YTick',[],'XColor','none','YColor','none');
    ylim([-1*linesperpage*(6+linebuffer+lyricbuffer),0]);
    hold off;
    title([songname,' Page ',num2str(ipage),' of ', num2str(numpages)],'FontSize',14);
    
    % Print pages to Temporary folder
    [status, msg, msgID] = mkdir('Songs\Temporary');
    print(gcf, '-dpdf', ['Songs\Temporary\',songname,' ',num2str(ipage),' of ',num2str(numpages),'.pdf'],'-fillpage');
end

% Bundle pdf into single file
pdfstruct   = dir('Songs\Temporary\*.pdf');
pdflist    = {};
for j=1:length(pdfstruct)
    pdflist{end+1}  = [pdfstruct(j).folder,'\',pdfstruct(j).name];
end
mergePdfs(pdflist,['Songs/' songname '.pdf']);

rmdir('Songs\Temporary','s');

% close all;
clearvars;

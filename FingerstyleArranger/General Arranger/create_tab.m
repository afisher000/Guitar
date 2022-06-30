%create tab
close all;
% Formatting parameters
linebuffer=2;
notesperline=14;
linesperpage=4;
notesperpage=notesperline*linesperpage;


songname='On';
load(['Songs/',songname,'.mat']);


numpages=ceil(numnotes/notesperpage);
for ipage=1:numpages
    
    figure(); hold on;
    % plot tab lines for page
    for i=1:linesperpage
        shift=(i-1)*(6+linebuffer);
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
            y=-1*( (7-istr) +q*(6+linebuffer) );
            
            if melody.str(j)==istr
                text(x,y,num2str( round(int2fret(istr,melody.int(j),'m'))-capo ),'FontSize',13);
            end
            for jj=1:size(bass.note,2)
                if bass.str(j,jj)==istr
                    text(x,y,num2str( round(int2fret(istr,bass.int{j,jj},'b'))-capo ),'FontSize',13);
                end
            end
        end

    end
    set(gca,'XTick',[],'YTick',[],'XColor','none','YColor','none');
    ylim([-1*linesperpage*(6+linebuffer),0]);
    hold off;
    title([songname,' Page ',num2str(ipage),' of ', num2str(numpages)],'FontSize',14);
    
    % Print pages
    [status, msg, msgID] = mkdir(['Songs\',songname]);
    print(gcf, '-dpdf', ['Songs\',songname,'\',songname,' ',num2str(ipage),' of ',num2str(numpages),'.pdf'],'-fillpage');
end
close all;
clearvars;

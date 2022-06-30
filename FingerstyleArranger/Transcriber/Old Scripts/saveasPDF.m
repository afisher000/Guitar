% SaveAsPDF
close all;
clearvars;

params();
lines_page      = 6;
measure_line    = 4;
measure_page    = 24;
xmax            = 100*measure_line;
ymax            = 0;
staffspacing    = 4;
dx              = .25; %Length of beat shift to avoid numbers on lines
maxmeas         = max(T.Measure);
numpages        = ceil(maxmeas/measure_page);

%% Plot Staff
title(songname);
cury    = 1;
pdfcell = {};
for j=1:numpages
    figure(); clf; hold on;
    for jline = 1:lines_page
        %% Thick Vertical Lines
        plot([0 0],-[cury cury+5],'k');
        for jj=1:measure_line
           plot(jj*[100 100], -[cury cury+5],'k');
        end

        %% Horizontal Lines
        for jj=1:6 
            plot([0 xmax],-[cury cury],'k');
            cury    = cury+1;
        end

        %% Staff Spacing
        cury    = cury + staffspacing;
    end
    
    %% Add Notes
    scn     = ismember(T.Measure, (j-1)*measure_page:(j*measure_page-1));
    Tscn    = T(scn,:);
    for jj=1:height(Tscn)
        jmeas   = Tscn.Measure(jj);
        jbeat   = Tscn.Beat(jj);
        jstr    = Tscn.String(jj);
        jfret   = Tscn.Fret(jj);
        xval    = 100*( mod(jmeas,measure_line) + jbeat/bpm) + 100*dx/bpm; %Notes should be offset
        yval    = jstr + floor(jmeas/measure_line) * (6+staffspacing);
    if jfret<10
        text(xval-2,-yval,num2str(jfret),'FontSize',13);
    else
        text(xval-5,-yval,num2str(jfret),'FontSize',13);
    end
    end

    %% Adjust Figure Properties
    set(gca,'XTick',[],'YTick',[],'XColor','none','YColor','none');
    xlim([0 xmax]); ylim(-lines_page*(6+staffspacing)*[j j-1] + [staffspacing 0]);
    hold off;
    if j==1
        title(songname);
    else
        title([songname,' (Page ',num2str(j),')']);
    end
    %% Save Images
    pdfname     = ['PDFs\',songname,' Page ',num2str(j),'.pdf'];
    print(gcf, '-dpdf', pdfname ,'-fillpage');
    pdfcell{end+1} = pdfname;
end

%% Create merged pdf, delete individuals
mergePdfs(pdfcell,['PDFs\',songname,'.pdf']);
for j=1:length(pdfcell)
    delete(pdfcell{j});
end

close all;
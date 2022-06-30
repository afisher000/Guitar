% SaveAsPDF
songname = 'Godfather Theme';
params();
plotPDF     = 1;
meas_page   = meas_line*lines_page;
maxpage     = floor(max(T.Measure)/meas_page);

%% Call plottab for each page
pdfcell = {};
for jpage=0:maxpage
    PDFpage     = jpage;
    
    figure(); 
    clf; 
    set(gca,'XTick',[],'YTick',[],'XColor','none','YColor','none');
    hold on;
    plottab; 
    hold off;
    
    if jpage>0
        title([songname,' (Page ',num2str(jpage+1),')']);
    end
    
    %% Save Images
    pdfname     = [analyzedpdffolder ,songname,' Page ',num2str(jpage+1),'.pdf'];
    print(gcf, '-dpdf', pdfname ,'-fillpage');
    pdfcell{end+1} = pdfname;
end

%% Create merged pdf, delete individuals
mergePDFs(pdfcell,[analyzedpdffolder ,songname,'.pdf']);
for jpage=1:length(pdfcell)
    delete(pdfcell{jpage});
end

close all;
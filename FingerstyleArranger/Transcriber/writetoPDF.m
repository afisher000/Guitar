% SaveAsPDF
songname = 'Annies Song';
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
    
    %% Save Images to PDF
    pdfname     = [transcribedpdffolder,songname,' Page ',num2str(jpage+1),'.pdf'];
    pdfcell{end+1} = pdfname;
    
%     % Figure margins need to be accounted for 
%     figposition = get(gca,'Position');
%     
%     lrmargin    = .25; %inches
%     bmargin     = .25; %inches
%     tmargin     = 
    set(gca,'Position',[0 0 1 .95]);
    print(gcf, '-dpdf', pdfname , '-fillpage');
    
end

%% Create merged pdf, delete individuals
mergePDFs(pdfcell,[transcribedpdffolder,songname,'.pdf']);
for jpage=1:length(pdfcell)
    delete(pdfcell{jpage});
end

close all;
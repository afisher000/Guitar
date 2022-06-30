%% Create Tex File
clc;
close all;
clearvars;

%% Comment
% Songnames can not include commas. 
% That pdf will be blank in the final library.

fid     = fopen('Library.tex','w');

%% Add generic structure
fprintf(fid, ['\\pdfminorversion=7' '\n']);
fprintf(fid, ['\\documentclass{article}' '\n']);
fprintf(fid, ['\\usepackage[utf8]{inputenc}' '\n']);
fprintf(fid, ['\\usepackage{pdfpages}' '\n']);
fprintf(fid, ['\\usepackage{hyperref}' '\n']);
fprintf(fid, ['\\title{Compilation of Music}' '\n']);
fprintf(fid, ['\\author{Andrew Fisher}' '\n']);
fprintf(fid, ['\\begin{document}' '\n']);
fprintf(fid, ['\\maketitle' '\n']);
fprintf(fid, ['\\tableofcontents' '\n']);
fprintf(fid, ['\\clearpage' '\n']);

%% Loop over pdf files
% Read in pdf songfile names
homefolder  = 'F:/Personal Projects/FingerstyleArranger/Transcriber/';
pdffolder   = 'F:/Personal Projects/FingerstyleArranger/Transcriber/Transcribed PDFs/';
songnames   = dir([pdffolder,'*.pdf*']);
for j=1:length(songnames)
    songtitle   = erase(songnames(j).name,'.pdf');
    fprintf(fid, ['\\phantomsection' '\n']);
    fprintf(fid, ['\\addcontentsline{toc}{section}{' songtitle '}' '\n']);
    fprintf(fid, ['\\includepdf[pages=-]{"' pdffolder songtitle '"}' '\n']);
end

fprintf(fid, ['\\end{document}' '\n']);


%% Compile tex file into PDF music library
% currentFolder = pwd;
% system(['cd ' , currentFolder]);
system('pdflatex -quiet Library.tex');
fprintf('Compiled once\n');
system('pdflatex -quiet Library.tex'); %compiling twice to ensure TOC exists
fprintf('Compiled twice\n');
clc;
fclose('all');

%% Move Library pdf
movefile('Library.pdf',homefolder);

%% Send PDF to Test Email
send_email('Guitar Library','A searchable compilation of all guitar pdfs',[homefolder,'Library.pdf']);


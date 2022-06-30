%Create total pdf

% Find all pdfs
currentdir = 'F:\FingerstyleArranger\Hymn Specific\Songs';
songstrct = dir('*.pdf');
songlist = {};
for j=1:length(songstrct)
    if ~strcmp(songstrct(j).name,'MergedSongs.pdf')  %exclude 'MergedSongs.pdf'
        songlist{end+1}=[songstrct(j).folder,'\',songstrct(j).name];
    end
end

mergePdfs(songlist,'MergedSongs.pdf');
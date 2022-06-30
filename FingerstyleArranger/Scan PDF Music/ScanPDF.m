%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Written by Andrew Fisher, Feb 2021
% Script takes pdf scan from hymnal and extracts note information (only
% part and order of notes)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
close all;
clearvars;

%% Read in PDF file
songname   = 'i need thee every hour';
raw     = rgb2gray(imread(PDFtoImg( ['Song PDFs/',songname,'.pdf'] )));
im      = imbinarize(raw,0.5);

%% Take Marginal Sums
vert_sum    = sum(~im,1);
horz_sum    = sum(~im,2);
horz_scn    = find(vert_sum);
im          = imfill( im(:,horz_scn) , 'holes'); %Remove white margin and text
original    = im; 

%% Save images of each staff
[pks,loc]   = findpeaks(horz_sum,'MinPeakHeight',0.8*max(horz_sum));
num_lines   = length(pks)/5;
staffmargin = round((loc(5)-loc(1))/4*3); % 3 extra lines above/below staff
staffheight = loc(5)-loc(1);
for j=1:num_lines
    idxshift    = 5*(j-1);
    image{j}   = im( loc(1+idxshift)-staffmargin : loc( 5+idxshift)+staffmargin , :);
end

%% Map from ypixel to staff
map2staff   = polyfit(loc(1:5),13:-2:5,1); map2staff(2) = 21;

%% Main Loop over images
[soprano, alto, tenor, bass]=deal([]);
for j = 1:num_lines
    im          = image{j};
    
    %% Identify lines using erosion/dilation
    SE          = strel("line",100,90);
    vertlines   = ~imdilate(imerode(~im,SE),SE);
    SE          = strel("line",60,0);
    horzlines   = ~imdilate(imerode(~im,SE),SE);
    all_lines   = horzlines & vertlines;
    measurelines= bwpropfilt(~vertlines,'Extent', [0.999 1]); %measure lines are perfectlysolid
    measurelines= bwpropfilt(measurelines,'MajorAxisLength', [160 180]); %measure lines should be staff height

    %% Remove lines using regionfill
    im_stripped = im;
    imshow(im);
    im_stripped = imbinarize(regionfill(double(im_stripped),~horzlines),0.6);
    im_stripped = imbinarize(regionfill(double(im_stripped),~vertlines),0.9);
%     imshow(im_stripped);
    %% Characterize and sort objects
    im_cleaned  = ~im_stripped;
    im_cleaned  = bwpropfilt(im_cleaned,'Area', [500 Inf]); % Remove small areas
%     imshow(im_cleaned);
    % Properties must include at least those in Shapes.mat
    stats       = regionprops(im_cleaned,'Area','Solidity','ConvexArea','MajorAxisLength','MinorAxisLength','Centroid');
    
    %% Loop over patterns
    [shapevec,xvec,yvec]=deal([]);
    noteshapes = {'h','hh','hs','s','sh','sp','ss','sstail','stail','w','ww'};
    figure(10); set(gcf,'position',[200,500,1400,400]); subplot(2,1,1); subplot(2,1,2); imshow(im_cleaned); %subplots for current shape and notes identified
    
    for jj = 1:length(stats)
        [shape,error]  = compare2shapes(stats(jj));
        xcoord          = stats(jj).Centroid(1);
        ycoord          = stats(jj).Centroid(2);
        shapevec{jj}    = shape;
        xvec(jj)        = xcoord;
        yvec(jj)        = ycoord;
        
        % Plot check of pattern matching
        figure(10); subplot(2,1,1); imshow(im_cleaned); hold on; scatter(xcoord,ycoord,'rx','LineWidth',5); title(sprintf('Shape: %s, Error: %.2f %%',shape,100*error)); hold off;
        
        if ismember(shape,noteshapes)
            figure(10); subplot(2,1,2); hold on; scatter(xcoord,ycoord,'rx','LineWidth',5); title('Identified Notes'); hold off;
        end
        if error > 0.10
            fprintf('Error = %.2f at j=%i and jj=%i\n',error,j,jj);
            
            % Uncomment to allow user to add shape to database
%             userflag    = input('Do you want to add to database? ("y" if yes):','s');
            userflag    = 'n';
            if strcmp(userflag,'y')
                % Add shapes to Database to improve statistics if error > thresh
                z = stats(jj);
                shapefromuser   = input('Shape?:','s');
                t1cell = {shapefromuser, z.Area,z.Solidity,z.ConvexArea,z.MajorAxisLength,z.MinorAxisLength};
                load('ShapeDatabase.mat');
                t1  = cell2table(t1cell,'VariableNames',Database.Properties.VariableNames);
                Database = [Database;t1];
                save('ShapeDatabase.mat','Database');
            end
        end
        

    end 
    
    
    
    %% Create music table
    % Include notes and accidentals
    % Map to staff
    linewidth       = length(horz_scn);
    line            = floor((j-1)/2);
    music           = table('Size',[0 3],'VariableTypes',{'double','double','string'});
    music.Properties.VariableNames = {'Xpixel','Staff','Label'};
    for jj=1:length(shapevec)
        if ismember( shapevec{jj}, {'s','h','w'})
            xval    = xvec(jj) + line*linewidth;
            yval    = round( polyval( map2staff, yvec(jj) ) );
            label   = 'note';
            music   = [music; {xval, yval, label}];
        elseif ismember( shapevec{jj}, {'ss','hh','ww','sh','hs'})
            xval    = xvec(jj) + line*linewidth;
            yval1   = round( polyval( map2staff, yvec(jj)+17.5 ) );
            yval2   = round( polyval( map2staff, yvec(jj)-17.5 ) );
            label   = 'note';
            music   = [music; {xval, yval1, label}];
            music   = [music; {xval, yval2, label}];
        elseif strcmp(shapevec{jj},'stail')
            xval    = xvec(jj) + line*linewidth;
            yval    = round( polyval( map2staff, yvec(jj)-17.5 ) ); %raise centroid
            label   = 'note';
            music   = [music; {xval, yval, label}];
        elseif strcmp(shapevec{jj},'sstail')
            xval    = xvec(jj) + line*linewidth;
            yval1   = round( polyval( map2staff, yvec(jj) ) );
            yval2   = round( polyval( map2staff, yvec(jj)-35 ) ); %raise centroid
            label   = 'note';
            music   = [music; {xval, yval1, label}];
            music   = [music; {xval, yval2, label}];
        elseif strcmp(shapevec{jj},'sp')
            xval    = xvec(jj) + line*linewidth;
            yval    = round( polyval( map2staff, yvec(jj) ) );
            label   = 'sharp';
            music   = [music; {xval, yval, label}];
        elseif strcmp(shapevec{jj},'n')
            xval    = xvec(jj) + line*linewidth;
            yval    = round( polyval( map2staff, yvec(jj) ) );
            label   = 'natural';
            music   = [music; {xval, yval, label}];
        elseif strcmp(shapevec{jj},'f')
            xval    = xvec(jj) + line*linewidth;
            yval    = round( polyval( map2staff, yvec(jj)+12 ) ); %lower centroid
            label   = 'flat';
            music   = [music; {xval, yval, label}];
        end
    end
    
    %% Calculate measure line positions
    stats       = regionprops(measurelines,'Centroid');
    for jj=1:length(stats)
        xval    = stats(jj).Centroid(1) + line*linewidth;
        yval    = 0; %space holder, isn't used
        label   = 'measure';
        music   = [music; {xval, yval, label}];
    end
   
    %% Sort music table
    % Try to order by xpixel, then staff
    music{:,1}  = 10*round(music{:,1}/10);
    music{:,1}  = music{:,1}+music{:,2}; %cheat to force alto/bass note to come first
    music       = sortrows(music,[1 2]);
   
    %% Identify key signature
    % Include 150 pixel shift to ensure first accidentals not acting on note
    firstnote   = find( strcmp( music{:,{'Label'}} , 'note') , 1 );
    keynum      = sum( music{:,{'Xpixel'}}< music{firstnote,1}-150 );
    if keynum == 0
        keysig  = [];
        keysign = [];
    elseif strcmp( music{1,{'Label'}} , 'flat' )
        ref     = music{keynum,2}; %get staff numbers, include octaves
        expand_ref = [ref-14, ref-7, ref, ref+7, ref+14];
        keysig  = expand_ref( logical((expand_ref>=1) .* (expand_ref<=21)) );
        keysign = -1;
    elseif strcmp( music{1,{'Label'}} , 'sharp' )
        ref     = music{keynum,2}; %get staff numbers, include octaves
        expand_ref = [ref-14, ref-7, ref, ref+7, ref+14];
        keysig  = expand_ref( logical((expand_ref>=1) .* (expand_ref<=21)) );
        keysign = 1;
    end


    
    
    %% Fill Part Vectors
    % n by 2 vectors. 1st col = xpixel. 2nd col = chromatic value
    if mod(j,2) % odd and treble
        staff2chromatic = [5 7 9 11 0 2 4 5 7 9 11 0 2 4 5 7 9 11 0 2 4];
    else % even and bass
        staff2chromatic = [9 11 0 2 4 5 7 9 11 0 2 4 5 7 9 11 0 2 4 5 7];
    end
    
    accidental = zeros(1,21);
    accidental(keysig) = keysign; %default key signature
    
    doublet = 0;
    res     = 60; %if distance between two notes is < res, they are considered at the same time.
    for jj=1:height(music)
        if doublet %skip second note entry
            doublet = 0;
            continue;
        end
        switch music{jj,3}
            case 'flat' %flat and sharp can handle double accidentals
                accidental( music{jj,2} ) = accidental( music{jj,2} ) - 1; 
            case 'sharp'
                accidental( music{jj,2} ) = accidental( music{jj,2} ) + 1;
            case 'natural'
                accidental( music{jj,2} ) = 0;
            case 'measure'
                accidental = zeros(1,21);
                accidental(keysig) = keysign;
            case 'note' % convert to chromatic and apply accidentals
                notescn         = strcmp( music{:,'Label'},'note');
                multiplicity    = length( find( abs(music{notescn,1} - music{jj,1})<res ) );
                if mod(j,2) %soprano/alto
                    if multiplicity==1
                        idx     = music{jj,2};
                        alto    = [alto ; [music{jj,1}, staff2chromatic(idx) + accidental(idx) ]];
                        soprano = [soprano; [music{jj,1}, staff2chromatic(idx) + accidental(idx) ]]; 
                    elseif multiplicity==2
                    	idx     = music{jj,2};
                        idx2     = music{jj+1,2};
                        alto    = [alto ; [music{jj,1}, staff2chromatic(idx) + accidental(idx) ]];
                        soprano = [soprano; [music{jj+1,1}, staff2chromatic(idx2) + accidental(idx2) ]];
                        doublet = 1;
                    else
                        error('Code not ready for multiplicity > 2'); % need to add recognition shapes and change doublet system
                    end
                else %tenor/bass
                    if multiplicity==1
                        idx     = music{jj,2};
                        bass    = [bass ; [music{jj,1}, staff2chromatic(idx) + accidental(idx) ]];
                        tenor   = [tenor; [music{jj,1}, staff2chromatic(idx) + accidental(idx) ]];
                    elseif multiplicity==2
                        idx     = music{jj,2};
                        idx2     = music{jj+1,2};
                        bass    = [bass ; [music{jj,1}, staff2chromatic(idx) + accidental(idx) ]];
                        tenor   = [tenor; [music{jj+1,1}, staff2chromatic(idx2) + accidental(idx2) ]];
                        doublet = 1;
                    else
                        error('Code not ready for multiplicity > 2');
                    end
                end

        end
    end
    
end

%% Unify Parts, fill .int structures
individual  = sort([soprano(:,1); alto(:,1); tenor(:,1); bass(:,1)]);
scn         = find(diff(individual) > res);
combined    = individual([scn;end]);

for j=1:length(combined)
    s_idx    = find( abs(soprano(:,1) - combined(j)) < res );
    a_idx    = find( abs(alto(:,1) - combined(j)) < res);
    t_idx    = find( abs(tenor(:,1) - combined(j)) < res);
    b_idx    = find(abs(bass(:,1) - combined(j)) < res);
    
    if s_idx
        s.int(j) = soprano(s_idx,2);
    else
        s.int(j) = 12; %12 on chromatic implies silence
    end
    if a_idx
        a.int(j) = alto(a_idx,2);
    else
        a.int(j) = 12;
    end   
    if t_idx
        t.int(j) = tenor(t_idx,2);
    else
        t.int(j) = 12;
    end  
    if b_idx
        b.int(j) = bass(b_idx,2);
    else
        b.int(j) = 12;
    end
end
       
%% Create Output Structures for Fingerstyle Arranger
if keysign<1 %flat or neutral
    noteset = {'c' 'db' 'd' 'eb' 'e' 'f' 'gb' 'g' 'ab' 'a' 'bb' 'b' ''};
else %sharp
    noteset={'c' 'cs' 'd' 'ds' 'e' 'f' 'fs' 'g' 'gs' 'a' 'as' 'b' ''};
end
int2note=containers.Map([0 1 2 3 4 5 6 7 8 9 10 11 12],noteset);
s.str = arrayfun(@(x) int2note(x), s.int, 'UniformOutput', false);
a.str = arrayfun(@(x) int2note(x), a.int, 'UniformOutput', false);
t.str = arrayfun(@(x) int2note(x), t.int, 'UniformOutput', false);
b.str = arrayfun(@(x) int2note(x), b.int, 'UniformOutput', false);

numnotes = length(s.int);
[s.str, a.str, t.str, b.str, e.str, e.fret, ed.str, ed.fret, ...
    e2.str, e2.fret, ed2.str, ed2.fret, edd.str, edd.fret, ...
    edd2.str, edd2.fret, eddd.str, eddd.fret, eddd2.str, eddd2.fret]=deal(zeros(1,numnotes));

%% Input Title, Lyrics, and write to file.
% songname=input('What is the song name?\n','s'); %give user option to name song
fprintf('Enter the lyrics for each note, separate by spaces\n');
full_lyrics = input('','s');

lyric_error = 1;
while lyric_error==1
    if length(strsplit(full_lyrics))~=numnotes
        fprintf('Length of lyrics (%i) does not match number of notes (%i)\n',length(strsplit(full_lyrics)),numnotes);
        fprintf('Revisit previous entry and correct the lyrics');
        full_lyrics=input('','s');
    else
        lyric_error=0;
        lyrics = strsplit(full_lyrics);
        fprintf('Lyrics successfully uploaded...\n');
    end
end

save(['F:\FingerstyleArranger\Hymn Specific\Songs\',songname,'.mat'],'s','a','t','b','e','ed','edd','eddd','e2','ed2','edd2','eddd2','lyrics','numnotes');
fprintf('Song data saved to \Hymn Specific\Songs folder\n');
    


    
    

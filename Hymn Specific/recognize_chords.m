%%% recognize_chords
% Still work in progress, 2/14/2021
% Goal is to identify chords of hymns and output as string.
% Could be used to find best key for guitar

close all;
clc;
clearvars;

%% Read in song
songname='moment by moment';
load(['Songs/',songname,'.mat']);

%% Transpose 
% without changing '12' elements (indicates silence)
capo    = 0;
sflag    = (s.int==12); s.int   = mod(s.int - capo,12); s.int(sflag)=12; 
aflag    = (a.int==12); a.int   = mod(a.int - capo,12); a.int(aflag)=12;
tflag    = (t.int==12); t.int   = mod(t.int - capo,12); t.int(tflag)=12;
bflag    = (b.int==12); b.int   = mod(b.int - capo,12); b.int(bflag)=12;

%% Define chord dictionary
dict  =   { 
                [0 4 7],        ' '     ;
                [0 3 7],        'm'     ;
                [0 4 7 10],     '7'     ;
                [0 3 7 10],     'm7'    ;
                [0 7 10],       '7sus'  ;
                [0 4 7 9],      '6'     ;
                [0 3 7 9],      'm6'    ;
                [0 2 7],        'sus2'  ;
                [0 5 7],        'sus4'  ;
                [0 4 7 10 2],   '9'     ; 
                [0 3 6],        'dim'   ;
                [0 4 7 11],     'maj7'  ;
                [0 4 8],        'aug'   ;
                };
Dict        = cell2table(dict);
Dict.Properties.VariableNames = {'Notes' 'Identifier'};
getKey_sharp = {'C' 'C#' 'D' 'D#' 'E' 'F' 'F#' 'G' 'G#' 'A' 'A#' 'B'};
getKey_flat = {'C' 'Db' 'D' 'Eb' 'E' 'F' 'Gb' 'G' 'Ab' 'A' 'Bb' 'B'};

%% Loop over song
for j = 1:length(s.int)
    notes   = unique( [s.int(j) a.int(j) t.int(j) b.int(j)] );
    if ismember(12,notes) || length(notes)<3 %if silence for some notes, or less than 3 notes
        chord{j} = ' ';
        continue;
    end
    
    %% Maximize match over chord type and key
    match = zeros( 12 , height(Dict) );
    for jj = 1:12 % loop over keys
        pattern = mod( notes - jj + 1, 12);
        for jjj = 1:height(Dict) %look over chord types
            ref     = Dict{jjj,1}{1}; 
            check(jj,jjj)  = sum(ismember(pattern,ref))/length(pattern);    % Test entire pattern fits in ref
            check2(jj,jjj) = sum(ismember(ref,pattern))/length(ref);        % How much of ref does pattern cover?
            
            if sum(ismember(pattern,ref)) < length(pattern)
                match(jj,jjj) = 0;
            else
                match(jj,jjj) = sum(ismember(ref,pattern))/length(ref);
            end
        end
    end
    [val, idx] = max(match(:)); %When duplicate maximum, tie goes to simplest chord type
    [idx_key idx_type]  = ind2sub(size(match),idx);

    %% Define keysig
    if j==1
        if ismember(idx_type,[0 5 10 3 8 1 6]) %C,F,Bb,Eb,Ab,Db,Gb (circle of fifths)
            getKey  = getKey_flat;
        else %G,D,A,E,B
            getKey  = getKey_sharp;
        end
    end
    
    %% Add chord
    root    = getKey{b.int(j)+1};
    key     = getKey{idx_key};
    type    = Dict{idx_type,2}{1};
    if strcmp(root,key)
        chord{j} = strcat(key,type);
    else
        chord{j} = strcat(key,type,'/',root);
    end
    
    %% Remove chord for small match
    if val<0.5
        chord{j} = ' ';
        continue;
    end
    
%     %% Display chords with less than perfect match
%     if val < 1
%         if length(notes)==3
%             fprintf('Match = %.2f, Root = %s, Notes = %d, %d, and %d\n',val,root,notes(1),notes(2),notes(3));
%         elseif length(notes)==4
%             fprintf('Match = %.2f, Root = %s, Notes = %d, %d, %d, and %d\n',val,root,notes(1),notes(2),notes(3),notes(4));
%         end
%     end
end
fprintf('Chords done\n');



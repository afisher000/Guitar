function [melody bass]=enter_notes(key)
melody.note={};
bass.note={};
rectsize=.1;
whitekey2note={'c' 'd' 'e' 'f' 'g' 'a' 'b'};

if strcmp(key,'sharp')
    blackkey2note={'cs' 'ds' '??' 'fs' 'gs' 'as' '??'};
else
    blackkey2note={'db' 'eb' '??' 'gb' 'ab' 'bb' '??'};
end

figure(1); fig=gcf; set(gcf,'Position',[100,100,1500,800]);
j=1; breakvar=0; mult=1;
while breakvar==0
    clf;
    % set up figure
    xlim([0.5,15.5]); ylim([0.5,3.5]); title(['Chord Number: ', num2str(j),'   Note Number: ',num2str(mult)]);
    set(gca,'XTick',[],'YTick',[],'XColor','none','YColor','none');
    
    % STOP and NEXT CHORD button
    rectangle('Position',[2 2.5 4 1]);
    text(3.5,3,'STOP','FontSize',20);
    rectangle('Position',[10 2.5 4 1]);
    text(11,3,'NEXT CHORD','FontSize',20);
  
    % white and black keys
    for i=1:15 
        rectangle('Position',[i-0.5 0.5 1 2]);
    end
    for i=1:13 
        if ismember(i,[3 7 10])
            continue;
        end
        rectangle('Position', [i+0.25 1.5 0.5 1] , 'FaceColor',[0,0,0]);
    end
    
    % Plot melody note (with red rectangle on all octaves)
    try
        if ~isempty( find(ismember(whitekey2note,melody.note{j})) )
            xnote=find(ismember(whitekey2note,melody.note{j}));
            ynote=1+.2;
            rectangle('Position', [xnote-rectsize ynote-rectsize, 2*rectsize 2*rectsize], 'FaceColor',[1 0 0]);
            xnote=xnote+7;
            rectangle('Position', [xnote-rectsize ynote-rectsize, 2*rectsize 2*rectsize], 'FaceColor',[1 0 0]);
        elseif ~isempty( find(ismember(blackkey2note,melody.note{j})) )
            xnote=find(ismember(blackkey2note,melody.note{j}))+0.5;
            ynote=2+.2;
            rectangle('Position', [xnote-rectsize ynote-rectsize, 2*rectsize 2*rectsize], 'FaceColor',[1 0 0]);
            xnote=xnote+7;
            rectangle('Position', [xnote-rectsize ynote-rectsize, 2*rectsize 2*rectsize], 'FaceColor',[1 0 0]);
        end
    catch
    end
    
    % Plot bass notes (with blue rectangle and number on all octaves)
    for jj=1:size(bass.note,2)
        try
            if ~isempty( find(ismember(whitekey2note,bass.note{j,jj})) )
                xnote=find(ismember(whitekey2note,bass.note{j,jj}));
                ynote=1-.2;
                rectangle('Position', [xnote-rectsize ynote-rectsize, 2*rectsize 2*rectsize], 'FaceColor',[0 0 1]);
                text(xnote-rectsize,ynote,num2str(jj),'FontSize',20);
                xnote=xnote+7;
                rectangle('Position', [xnote-rectsize ynote-rectsize, 2*rectsize 2*rectsize], 'FaceColor',[0 0 1]);
                text(xnote-rectsize,ynote,num2str(jj),'FontSize',20);
            elseif ~isempty( find(ismember(blackkey2note,bass.note{j,jj})) )
                xnote=find(ismember(blackkey2note,bass.note{j,jj}))+0.5;
                ynote=2-.2;
                rectangle('Position', [xnote-rectsize ynote-rectsize, 2*rectsize 2*rectsize], 'FaceColor',[0 0 1]);
                text(xnote-rectsize,ynote,num2str(jj),'FontSize',20);
                xnote=xnote+7;
                rectangle('Position', [xnote-rectsize ynote-rectsize, 2*rectsize 2*rectsize], 'FaceColor',[0 0 1]);
                text(xnote-rectsize,ynote,num2str(jj),'FontSize',20);
            end
        catch
        end
    end
    
    
    
    [x,y,button]=ginput(1);
    y=round(y);
    
    switch button
        case 1 %left click; add to bass
            if y==1
                x=round(x);
                bass.note{j,mult}= whitekey2note{ mod(x-1,7)+1 };
                mult=mult+1;
            elseif y==2
                x=round(x-0.5);
                if ismember( mod(x-1,7)+1 , [1 2 4 5 6])
                    bass.note{j,mult}= blackkey2note{ mod(x-1,7)+1 };
                    mult=mult+1;
                end
            else
                if x<8
                    breakvar=1;
                    if length(melody.note) > size(bass.note,1)
                        bass.note{ length(melody.note) ,1}=[];
                    elseif length(melody.note) < size(bass.note,1)
                        melody.note{ size(bass.note,1) }=[];
                    end
                else
                    j=j+1;
                    mult=1;
                end
            end
        case 2 % middle click; reduce mult
            mult=max(1,mult-1);
        case 3 % right click; add to melody
            if y==1
                x=round(x);
                melody.note{j}= whitekey2note{ mod(x-1,7)+1 };
            elseif y==2
                x=round(x-0.5);
                if ismember( mod(x-1,7)+1 , [1 2 4 5 6])
                    melody.note{j}= blackkey2note{ mod(x-1,7)+1 };
                end
            end
    end
end
close('1');
function struct=enter_notes(lyrics,key)
% Called by input_song.
% Key is identifier for sharp or flat musical key.
% Lyrics gives the total number of notes.

whitekey2note={'c' 'd' 'e' 'f' 'g' 'a' 'b'};
if strcmp(key,'sharp')
    blackkey2note={'cs' 'ds' '??' 'fs' 'gs' 'as' '??'};
else
    blackkey2note={'db' 'eb' '??' 'gb' 'ab' 'bb' '??'};
end

figure(1); fig=gcf; set(gcf,'Position',[100,100,1500,600]);
for j=1:length(lyrics)
    % set up figure
    title(lyrics{j}); xlim([0.5,15.5]); ylim([0.5,2.5]);
    set(gca,'XTick',[],'YTick',[],'XColor','none','YColor','none');
    
    for i=1:15 %white rectangles
        rectangle('Position',[i-0.5 0.5 1 2]);
    end
    for i=1:13 %black rectangles
        if ismember(i,[3 7 10])
            continue;
        end
        rectangle('Position', [i+0.25 1.5 0.5 2] , 'FaceColor',[0,0,0]);
    end
    %get input
    [x,y]=ginput(1);
    y=round(y);
    if y==1
        x=round(x);
        struct.note{j}= whitekey2note{ mod(x-1,7)+1 };
    else
        x=round(x-0.5);
        struct.note{j}= blackkey2note{ mod(x-1,7)+1 };
    end
    

end
close('1');
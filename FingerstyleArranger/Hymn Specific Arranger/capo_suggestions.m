function capo_suggestions(GC)
% GC counts the number of bassnotes for each alphabetical note
% An ideal capo position would line the most bassnotes up with the 
% open frets of the lower guitar strings.

% To compute a simple numerical "score" for each capo position, add the
% number of notes on each open string scaling by [1 1 0.5 0 0 0].
% Open fret locations (capo=0): [0; 0; 3; 0; 1; 0; 0; 4; 0; 2; 0; 5;];
GC = GC(1:end-1);

% for each iteration, GC(5)+GC(10)+0.5*GC(3)
scorevec=[];
capovec = [];
for capo = -5:6
    capovec = [capovec,capo];
    GCvec = circshift(GC,-capo);
	scorevec = [scorevec, GCvec(5)+GCvec(10)+0.5*GCvec(3)];
end
figure(); plot(capovec,scorevec); ylabel('Score'); xlabel('Capo Adjustment');
title('Suggested Capo Adjustment'); movegui('northeast');

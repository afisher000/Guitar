

for istr=1:6
eps=.03; % shift in y so black lines can be seen

    % Loop over melody notes
    if (melody.played(j)==1 && melody.str(j)==istr)
        scatter(int2fret(istr,melody.int(j),'m'),istr+eps,200,'k*');
    elseif melody.played(j)==0 && melody.int(j)~=-1
        scatter(int2fret(istr,melody.int(j),'m'),istr+eps,200,'r*');
    end

    % Loop over bass notes
    for jj=1:size(bass.note,2)
        if bass.played(j,jj)==1 && bass.str(j,jj)==istr
            scatter( int2fret(istr,bass.int{j,jj},'b',(jj-1)/(size(bass.note,2)-1) ),istr+eps,200,'k*');
        elseif bass.played(j,jj)==0 && bass.int{j,jj}~=-1
            colorshade=(jj-1)/size(bass.int,2);
            scatter( int2fret(istr,bass.int{j,jj},'b',(jj-1)/(size(bass.note,2)-1) ),istr+eps,200,'*','MarkerEdgeColor',[0 colorshade 1-colorshade]);
        end
    end

end
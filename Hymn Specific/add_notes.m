% Called by select_notes. This adds the notes onto the guitar fretboard for
% selection.

for istr=1:6
eps=.03; % shift in y so black lines can be seen

    % Loop over s notes
    if s.str(j)==istr
        scatter(int2fret(istr,s.int(j),'s'),istr+eps,200,'k*');
    elseif s.str(j)==0
        scatter(int2fret(istr,s.int(j),'s'),istr+eps,200,'r*');
    end

    % Loop over a notes
    if a.str(j)==istr
        scatter(int2fret(istr,a.int(j),'a'),istr+eps,200,'k*');
    elseif a.str(j)==0
        scatter(int2fret(istr,a.int(j),'a'),istr+eps,200,'m*');
    end

    % Loop over a notes
    if t.str(j)==istr
        scatter(int2fret(istr,t.int(j),'t'),istr+eps,200,'k*');
    elseif t.str(j)==0
        scatter(int2fret(istr,t.int(j),'t'),istr+eps,200,'g*');
    end

    % Loop over a notes
    if b.str(j)==istr
        scatter(int2fret(istr,b.int(j),'b'),istr+eps,200,'k*');
    elseif b.str(j)==0
        scatter(int2fret(istr,b.int(j),'b'),istr+eps,200,'b*');
    end
    

    if  e.str(j)==istr
        scatter(e.fret(j),istr+eps,200,'k^');
    end

    % Loop over extra notes
    if  e2.str(j)==istr
        scatter(e2.fret(j),istr+eps,200,'k^');
    end

    % Loop over extra notes
    if  ed.str(j)==istr
        scatter(ed.fret(j),istr+eps,200,'k>');
    end

    % Loop over extra notes
    if  ed2.str(j)==istr
        scatter(ed2.fret(j),istr+eps,200,'k>');
    end

    % Loop over extra notes
    if  edd.str(j)==istr
        scatter(edd.fret(j),istr+eps,200,'kv');
    end

    % Loop over extra notes
    if  edd2.str(j)==istr
        scatter(edd2.fret(j),istr+eps,200,'kv');
    end

    % Loop over extra notes
    if  eddd.str(j)==istr
        scatter(eddd.fret(j),istr+eps,200,'k<');
    end

    % Loop over extra notes
    if  eddd2.str(j)==istr
        scatter(eddd2.fret(j),istr+eps,200,'k<');
    end
end
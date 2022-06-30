% Update structures

switch part
    case 'soprano'
        if qfret==round(int2fret(qstr,s.int(j),'s'))
            if s.str(j) %note was played
                s.str(j)=0;
            else %note wasn't played
                s.str(j)=qstr;
            end
        end
    case 'alto'
        if qfret==round(int2fret(qstr,a.int(j),'a'))
            if a.str(j)
                a.str(j)=0;
            else
                a.str(j)=qstr;
            end
        end
    case 'tenor'
        if qfret==round(int2fret(qstr,t.int(j),'t'))
            if t.str(j)
                t.str(j)=0;
            else
                t.str(j)=qstr;
            end
        end
    case 'bass'
        if qfret==round(int2fret(qstr,b.int(j),'b'))
            if b.str(j)
                b.str(j)=0;
            else
                b.str(j)=qstr;
            end
        end
    case 'e'
        if e.str(j)
            e.str(j)=0;
            e.fret(j)=0;
        else
            e.str(j)=qstr;
            e.fret(j)=qfret;
        end
    case 'e2'
        if e2.str(j)
            e2.str(j)=0;
            e2.fret(j)=0;
        else
            e2.str(j)=qstr;
            e2.fret(j)=qfret;
        end
    case 'ed'
        if ed.str(j)
            ed.str(j)=0;
            ed.fret(j)=0;
        else
            ed.str(j)=qstr;
            ed.fret(j)=qfret;
        end
    case 'ed2'
        if ed2.str(j)
            ed2.str(j)=0;
            ed2.fret(j)=0;
        else
            ed2.str(j)=qstr;
            ed2.fret(j)=qfret;
        end
    case 'edd'
        if edd.str(j)
            edd.str(j)=0;
            edd.fret(j)=0;
        else
            edd.str(j)=qstr;
            edd.fret(j)=qfret;
        end
    case 'edd2'
        if edd2.str(j)
            edd2.str(j)=0;
            edd2.fret(j)=0;
        else
            edd2.str(j)=qstr;
            edd2.fret(j)=qfret;
        end
    case 'eddd'
        if eddd.str(j)
            eddd.str(j)=0;
            eddd.fret(j)=0;
        else
            eddd.str(j)=qstr;
            eddd.fret(j)=qfret;
        end
    case 'eddd2'
        if eddd2.str(j)
            eddd2.str(j)=0;
            eddd2.fret(j)=0;
        else
            eddd2.str(j)=qstr;
            eddd2.fret(j)=qfret;
        end
end
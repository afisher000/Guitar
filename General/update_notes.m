% Update structures

switch curkey
    case 'm'
        if qfret==round(int2fret(qstr,melody.int(j),'m'))
            if melody.played(j)==0
                melody.played(j)=1;
                melody.str(j)=qstr;
                elsemb
                melody.played(j)=0;
                melody.str(j)=0;
            end
        end
    case 'b'
        for jj=1:size(bass.note,2)
            if qfret==round(int2fret(qstr,bass.int{j,jj},'b'))
                if bass.played(j,jj)==0
                    bass.played(j,jj)=1;
                    bass.str(j,jj)=qstr;
                    break;
                elseif bass.str(j,jj)==qstr
                    bass.played(j,jj)=0;
                    bass.str(j,jj)=0;
                    break;
                end
            end
        end
end
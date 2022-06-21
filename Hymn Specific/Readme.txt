Readme:

Order of matlab functions for creating fingerstyle arrangement:

1) input_song.m
	Prompts for lyrics and notes (entered on piano keyboard)
	Subfunctions are enter_notes.m
    Alternatively, code is being developed to scan a pdf instead of entering manually.

2) select_notes.m
	Script to pick which notes are included in arrangement.
	e,e2,ed,ed2,..etc are extra notes that happen for "off-lyric" notes.
	d's represent delays and 2 suffix allows multiple notes at each delay.
	Subfunctions are create_fretboard.m, add_notes.m, update_notes.m, rapid_input.

	Options when selecting notes:
		left/right arrow  	- change note number
		p                   - jump to entered note number
		s,a,t,b             - enter soprano, alto, tenor, or bass note
		1 or 2              - enter e or e2 note
		3 or 4              - enter ed or ed2 note
		5 or 6              - enter edd or edd2 note
		7 or 8              - enter eddd or eddd2 note
		r                   - enter rapid notes (usually for soprano line)
        backspace           - clear all notes in window 
        delete              - clear entire song (prompts to confirm)
		escape              - exit and save

3) create_tab.m
	Creates tab based on saved notes.
	Prints to a pdf file.


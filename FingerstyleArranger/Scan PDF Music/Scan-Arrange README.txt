FingerstyleArranger README:

1) Save song as PDF file
- Current use of the code has been limited to a specific pdf hymnal. Generalization
	to any pdf music may require extension shape identification training.

2) ScanPDF.m
- Confirm using fig(11) that notes are correctly identified
- If not, you can add shapes to database. Switch commenting on userflag variable
	and set error threshold to be low enough that the code gives
	the option to add the shape to ShapeDatabase. Then you will have to add
	the shape type to ShapeStatistics.m and run that file.
- Identifier tags are explained in ShapeStatistics.m
- Enter lyrics when prompted. The length of the lyrics (when split by spaces)
	must equal the number of played chords. To accomodate notes that don't
	have lyrics, enter '-' as a placeholder. If the code rejects the entered
	lyrics, review the previous entry by hitting the up arrow and make the 
	necessary corrections.
- The song data is saved in "\Hymn Specific\Songs".

3) select_notes.m
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

4) create_tab.m
	Creates tab based on saved notes.
	Saves pdf files in a folder with the songname in "\Hymn Specific\Songs"



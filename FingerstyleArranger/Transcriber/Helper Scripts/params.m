%% Parameters
clc;
close all;
warning('off','all');

MIDIfolder              = 'F:\Personal Projects\FingerstyleArranger\Transcriber\Analyze MIDI\Original MIDIs\';
matfolder               = 'F:\Personal Projects\FingerstyleArranger\Transcriber\Song Matfiles\';
origwavfolder           = 'F:\Personal Projects\FingerstyleArranger\Transcriber\Analyze Spectrogram\Original WAVs\';
analyzedpdffolder       = 'F:\Personal Projects\FingerstyleArranger\Transcriber\Analyze Spectrogram\Analyzed PDFs\';
transcribedpdffolder    = 'F:\Personal Projects\FingerstyleArranger\Transcriber\Transcribed PDFs\';
transcribedwavfolder    = 'F:\Personal Projects\FingerstyleArranger\Transcriber\Transcribed WAVs\';

if ~isfile([matfolder,songname,'.mat'])
    error('Song has not been initialized. Run initializesong.m first.\n');
end
load([matfolder, songname,'.mat']);

%% Spectrogram Parameters
tmin    = 0;
tspan   = 6;
tmax    = tmin+tspan;
wfac    = 0.5;
ofac    = 0.5;
Nmin    = -4; %leave fixed, min note
Nmax    = 40; %adjustable, max note

%% Initialize cursor
curmeas = 0;
curbeat = 0;
curstr  = 1;
stepsize = 0.5;
stepsizevec = [1/4, 1/3, 1/2, 1, bpm];
minstepfac  = prod( 1./stepsizevec(stepsizevec<1));
%% Modes
playmode = 0; %plays sound of notes at same location as you move around tab
fastmode = 0; %only plots current line on tab to reduce lag

%% Tab Parameters
rgb             = .5*[1 1 1];
plotPDF         = 0; %flag for plotting PDF
curtime         = 0;
curmeas         = 0;
curbeat         = 0;
curstr          = 1;
lines_page      = 8;
meas_line       = 4;
staffbuffer     = 4;
measurebuffer   = 10;
dy              = .1; %y shift to make numbers readable

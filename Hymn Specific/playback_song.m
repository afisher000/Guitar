%Play back song
Fs = 44100;
freq = 100;
F   = linspace(1/Fs,freq*4.5,1000); %freq vector
T   = zeros(Fs*4, 1); % 4 second time vector


delay   = round(Fs/freq);
b   = firls(1, [0 1],[ 1 1]);
a   = [1 zeros(1,delay) 1 1];
L   = max(length(b),length(a))-1;
zi  = rand(L,1);
% zi  = mod( (1:L)/140 , 1);
note = filter(b,a,T,zi);
note = note-mean(note);
note = note/max(abs(note));

hplayer = audioplayer(note,Fs);
play(hplayer)


[H,W] = freqz(b, a, F, Fs);
figure(10);
plot(W, 20*log10(abs(H)));
title('Harmonics of an open A string');
xlabel('Frequency (Hz)');
ylabel('Magnitude (dB)');
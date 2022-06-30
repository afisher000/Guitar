% Explain function
[y, Fs]  = audioread([origwavfolder,songname,'.wav']);
TMAX        = length(y)/Fs;

%% Define the beat lattice of the song
y2   = smooth(y.^2,1000);
L       = length(y2);
dt      = 60/BPM; % time between beats
dN      = round(dt*Fs);

for j=1:dN
    temp(j)     = sum(y2(j:dN:L));
end
[~,idx] = max(temp);

%% Define beattimes and anchortimes
beattimes   = (idx:dN:L)/Fs;
anchortimes = (idx:round(dN/4):L)/Fs;
save([matfolder,songname,'.mat'],'TMAX','anchortimes','beattimes','-append');

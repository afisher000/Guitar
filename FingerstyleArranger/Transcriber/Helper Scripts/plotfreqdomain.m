%% Plot Frequency Domain
fmin        = 82.41*2^(Nmin/12);
fmax        = 82.41*2^(Nmax/12);

%% Compute Spectrogram
window      = round(Fs*wfac); %small helps time res, large helps freq res
overlap    = round(window*ofac); 
[s,f,t,ps]  = spectrogram(y,window,overlap,fmin:fmax,Fs);
flog        = 12/log(2) * log(f/82.41); %convert frequency to note number

%% Extend Spectrogram to cover figure
t   = [0,t,tspan];
ps  = [ mean(ps(:))*ones(length(f),1) , ps , mean(ps(:))*ones(length(f),1) ];

%% Define figure properties
ax          = gca;
ax.CLim     = [ log(mean(ps(:))) log(max(ps(:))) ];
shading interp; 
view([0 0 1]);
ax.XLabel.String = 'Note Number';
ax.YLabel.String = 'Time (s)';
ax.XLim     = [Nmin Nmax];
ax.YLim     = [tmin tmax];
notenames       = repmat( {'C' 'Cs' 'D' 'Ds' 'E' 'F' 'Fs' 'G' 'Gs' 'A' 'As' 'B'} , [1 4]);
ax.XTick        = Nmin:Nmax;
ax.XTickLabel   = notenames(1:(Nmax-Nmin+1));

%% Plot spectrogram
[FLOG,Time] = meshgrid(flog,t);
pcolor(ax,FLOG,Time+tmin,log(ps')); 
shading interp;

%% Plot Vertical Lines (notes)
xtemp   = reshape( repmat( Nmin:Nmax, 3, 1), 1, []);
ytemp   = repmat([tmin tmax tmin], 1, Nmax-Nmin+1);
plot(ax, xtemp, ytemp, 'k');


%% Plot Horizontal Lines (beats)
xtemp   = repmat([Nmin Nmax Nmin], 1, length(beattimes));
ytemp   = reshape( repmat( beattimes, 3, 1), 1, []);
plot(ax, xtemp, ytemp, 'k');
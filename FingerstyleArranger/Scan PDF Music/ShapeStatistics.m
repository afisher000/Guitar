%% Used to update ShapeStatistics
% s = single solid
% ss = double solid
% h = single half
% hh = double half
% w = whole
% ww = double whole
% sh = solid over half
% hs = half over solid
% r = quarter rest
% rbar = rest bar (cut in half by image processing)
% rbarfull = full rest bar
% rtail = 8th rest tail
% stail = single solid with 8th tail
% sstail = double solid with 8th tail
% tc = treble clef
% bc = bass clef
% d3 = the digit 3
% d4 = the digit 4
% d8 = the digit 8
% f = flat
% n = natural
% sp = sharp

clearvars;
close all;
load('ShapeDatabase.mat');
T=Database;

type = {'s' 'ss' 'h' 'hh' 'w' 'ww' 'sh' 'hs' 'r' 'rbar' 'rbarfull' 'rtail' 'stail' 'sstail' 'tc' 'bc' 'd3' 'd4' 'd8' 'f' 'n' 'sp'};

for j=1:length(type)
    scn                     = strcmp( T{:,{'shape'}} , type{j});
    Area.mu                 = mean(T{scn,2});
    Solidity.mu             = mean(T{scn,3});
    ConvexArea.mu           = mean(T{scn,4});
    MajorAxisLength.mu      = mean(T{scn,5});
    MinorAxisLength.mu      = mean(T{scn,6});
    Area.sig                = std(T{scn,2});
    Solidity.sig            = std(T{scn,3});
    ConvexArea.sig          = std(T{scn,4});
    MajorAxisLength.sig     = std(T{scn,5});
    MinorAxisLength.sig     = std(T{scn,6});
    
%     ratio(1) = std(T{scn,2})/mean(T{scn,2});
%     ratio(2) = std(T{scn,3})/mean(T{scn,3});
%     ratio(3) = std(T{scn,4})/mean(T{scn,4});
%     ratio(4) = std(T{scn,5})/mean(T{scn,5});
%     ratio(5) = std(T{scn,6})/mean(T{scn,6});
    
    eval( strcat(type{j},'.Area.mu = Area.mu') );
    eval( strcat(type{j},'.Solidity.mu = Solidity.mu') );
    eval( strcat(type{j},'.ConvexArea.mu = ConvexArea.mu') );
    eval( strcat(type{j},'.MajorAxisLength.mu = MajorAxisLength.mu') );
    eval( strcat(type{j},'.MinorAxisLength.mu = MinorAxisLength.mu') );
    eval( strcat(type{j},'.Area.sig = Area.sig') );
    eval( strcat(type{j},'.Solidity.sig = Solidity.sig') );
    eval( strcat(type{j},'.ConvexArea.sig = ConvexArea.sig') );
    eval( strcat(type{j},'.MajorAxisLength.sig = MajorAxisLength.sig') );
    eval( strcat(type{j},'.MinorAxisLength.sig = MinorAxisLength.sig') );
%     max(ratio)
end

clear Area ConvexArea Database j MajorAxisLength MinorAxisLength scn Solidity T type
save('ShapeStats.mat');

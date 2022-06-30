function [beatOut,msgOut] = createMessage(messageIn,beatIn,deltaTimeIn,ticksPerQNoteIn)

if messageIn < 0     % Ignore Sysex message/meta-event data
    beatOut = beatIn;
    msgOut = midimsg(0);
    return
end

% Create RawBytes field
messageLength = length(messageIn);
zeroAppend = zeros(8-messageLength,1);
bytesIn = transpose([messageIn;zeroAppend]);

% deltaTimeIn and ticksPerQNoteIn are both uints
% Recast both values as doubles
d = double(deltaTimeIn);
t = double(ticksPerQNoteIn);

% Create Timestamp field and tsOut
beatOut = beatIn+d;

% Create midimsg object
midiStruct = struct('RawBytes',bytesIn,'Timestamp',beatOut);
msgOut = midimsg.fromStruct(midiStruct);

end
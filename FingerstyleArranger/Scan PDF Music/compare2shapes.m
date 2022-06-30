function [shape minerror] = compare2shapes(data)
% This function identifies a pattern in an image by comparing to previously
% save shapes. 

% Input: A structure with the same entries as shapes in 'Shapes.mat' (from
% regionprops)

% Output: String of shape that is best matched. Or 'none' if max error
% greater than the threshhold

load('ShapeStats.mat');
shapes  = who('-file','ShapeStats.mat'); %shape names
props = fieldnames(s); %s is a variable from ShapeStats.mat

for ishape = 1:length(shapes)
    for iprop = 1:length(props)
        try
            % Compute with mean only
            ideal   = eval(strcat(shapes{ishape},'.',props{iprop},'.mu'));
            measured= eval(strcat(getVarName(data),'.',props{iprop}));
            
            % Possible to use std if needed
            %??
        catch
            error('Check that data fields for pattern match data fields in ShapeStats.mat');
        end
        errors(ishape,iprop) = abs((measured-ideal)/ideal);
    end
end

meanerror  = mean(errors,2); %Average over property errors
[minerror ishape] = min(meanerror); %Minimize over shape errors

if minerror>0.20
    shape = 'none';
else
    shape = shapes{ishape};
end

end


%% Subfunction to get variable name as string
function out = getVarName(var)
    out = inputname(1);
end
% Written by ChatGPT 
% 2024/1/3
% usage:
% string1 = 'wout_ITER_free_ripple.nc';
% truncatedString1 = truncateString(string1);
% disp(truncatedString1); => ITER_free_ripple

function truncatedString = truncateString(inputString)
    % Use regular expression to extract the desired portion
    match = regexp(inputString, '(?<=_)([^.]+)', 'match', 'once');

    % Check if a match is found
    if ~isempty(match)
        truncatedString = match;
    else
        truncatedString = inputString; % Return the original string if no match is found
    end
end

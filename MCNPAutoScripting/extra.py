
def fold128(text):
    """
    Folds a string to a maximum of 128 characters per line.

    Parameters:
    text (str): The input string to be folded.

    Returns:
    str: The folded string.
    """
    new_lines = []
    lines = text.split(' ')
    
    new_line = ''
    i=0
    
    while i < len(lines):

        if len('    '+new_line + lines[i] + ' ') < 128:
            new_line += lines[i] + ' '
            i += 1
        else:
            # lines[i] = new_line
            # new_line = ''
            new_lines.append(new_line)
            new_line = ''
            i += 1
    new_lines.append(new_line)
    new_lines = [e for e in new_lines if e != '']
    return '\n\t'.join(new_lines)

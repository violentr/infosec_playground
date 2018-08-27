def escape_characters_in_string(string)
  pattern = /(\'|\"|\.|\*|\/|\-|\\)/
  string.gsub(pattern){|match|"\\"  + match} # <-- Trying to take the currently found match and add a \ before it I have no idea how to do that).
end

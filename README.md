# File Timestamper
Small toolset for handling filenames with timestamps. Original use 
case is for timestamps with formats of the type 
`<Year><Month><Day>_<Hour><Minute><Second>` where each field is 
zero padded to give 8 digits, an underscore, then six digits. This
format is considered the default for formatting timestamps, but 
parsing filenames/strings with timestamps is more general, because 
it uses `dateutil.parser.parse`.

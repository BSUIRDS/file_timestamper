# File Timestamper
Small toolset for handling filenames with timestamps. 

Filenames are expected to be in the format `<stem><stamp><suffix>` 
where files sharing the same `<stem>` but different timestamps, 
`<stamp>`, represent a simple way to track file versions.

The `latest_version` function finds the file with the most
recent timestamp, among all files sharing the same `<stem>`
(and, optionally, the same `<suffix>`, i.e. extension).

The original use case was for files generated by Evisions Argos
reporting software, which have timestamps like e.g., 
`20200101_140000` for 2pm Jan 1st 2020. This code has been made
a little more general.

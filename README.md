# concatsql

Concatenate files *.sql or others in only file

> This app has the ability to concatenate sql files (or other if
> configured), into one, since different paths are provided, in addition
> to filter by date ranges by edition

**Arguments**

-l = [List configuration config.json]

-v = [Check parameters config.json]

-e = [Run the process with the information contained in config.json]

-u = [Upgrade config.json with the information sent in the additional parameters]

    pathfiles="path0,path1,path2"	[Flights in the wrapper file folders]
    namefile="complete.sql"			[Output file name and path]
    openfile=1 						[Open file generated after execution]
    fromdate="YYYY-MM-DD"			[Filter files more equal date]
    todate="YYYY-MM-DD"				[Filter files with same date less]

> TODO(@iscenigmax):  	
>	-Send file via FTP or email
>	-Compatibility to
> respond through a browser
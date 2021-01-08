# IGOR is for pulling and archiving financial reports for following analysis

edgar : make initial query to SEC database
igor_tools : use edgar and drill into SEC pages to get .htmls of final reports
igor_sidekick : extract information from individual .html reports

- [ ] dont store timezone, allow it to be set when changing problem setting, then convert it to utc and use that internally
- [ ] all of the discord integration
	- [ ] server setting changes
	- [ ] discord ui folder
	- [ ] cogs folder
	- [ ] setting the output channel
- [ ] make a user object or something where each user can store their leetcode username. make a data structure to store these. would store their discord id as key or something, then their leetcode username and their points
- [ ] implement the point system where you can submit, this would have to store active problems within a server. can store the points in the user structures. will use the recent ac query to get the most recent problems 
- [ ] the other bucket management and setting changes. ie if they want to be part of the daily lc or contests, make sure that if they want to be removed they are also removed from the buckets
- [ ] look into SQL/JSon problems and if i can sort them out
- [ ] add more helper methods to query manager to simplify use
- [ ] delete the archives folder
- [ ] create some testing servers and let it run overnight
- [ ] delete the notes folder, move the changelog to root
- [ ] maybe for alerts i can have a userole server setting and a link role command which sets the role to use in alerts

https://github.com/akarsh1995/leetcode-graphql-queries/tree/main
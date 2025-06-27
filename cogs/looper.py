import time
import discord 
from discord import app_commands
from discord.ext import commands, tasks
from utils import problem_helper as probh
from utils import datetime_helper as timeh
from models.app import App
from models.alert import Alert, AlertType
from models.problem import Problem
from mediators.alert_builder import AlertBuilder
from services.problem_service import ProblemService
from view.problem_embed import ProblemEmbed
from view.alert_embed import AlertEmbed
from buckets.static_time_bucket import StaticTimeAlert

WEEKLY_CONTEST_DOW = 6  # Saturday
WEEKLY_CONTEST_HOUR = 22  # 10 PM
WEEKLY_CONTEST_INTERVAL = 2  # 30 minutes

BIWEEKLY_CONTEST_DOW = 0  # Sunday
BIWEEKLY_CONTEST_HOUR = 10  # 10 AM
BIWEEKLY_CONTEST_INTERVAL = 2  # 30 minutes

DAILY_PROBLEM_HOUR = 8  # 8 PM
DAILY_PROBLEM_INTERVAL = 0  # 0 minutes

class Looper(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client 
        self.app: App = client.app
        
        self.mainloop.start()
        self.updateProblemset.start()
    
    @tasks.loop(minutes=1)
    async def mainloop(self) -> None:
        dow = int(time.strftime('%w'))  # 0 = sunday, 6 = saturday
        hour = int(time.strftime('%H'))
        minute = int(time.strftime('%M'))
        
        intervals = [0, 15, 30, 45]  # 0=0, 15=1, 30=2, 45=3. problem intervals are 15 minutes
        if minute not in intervals:
            minInterval = None
        else:
            minInterval = minute // 15

        # minute = 15
        # dow = 6
        # hour = 1
        # minInterval = 3
        
        # dow = WEEKLY_CONTEST_DOW
        # hour = WEEKLY_CONTEST_HOUR
        # minInterval = WEEKLY_CONTEST_INTERVAL
        
        # dow = BIWEEKLY_CONTEST_DOW
        # hour = BIWEEKLY_CONTEST_HOUR
        # minInterval = BIWEEKLY_CONTEST_INTERVAL
        
        # hour = DAILY_PROBLEM_HOUR
        # minInterval = DAILY_PROBLEM_INTERVAL

        print("handling alerts")
        await self.handleProblemAlerts(dow, hour, minInterval)
        await self.handleContestAlerts(dow, hour, minute)
        await self.handleStaticAlerts(dow, hour, minInterval)
        print("finished handling alerts")
        
        
    # update the problemset every 48 hours
    @tasks.loop(hours=48)
    async def updateProblemset(self) -> None:
        probh.updateProblemSet() # scrape new problems
        self.app.problemService.initProblemSets() # reinitialize the problem service

    @updateProblemset.before_loop
    @mainloop.before_loop
    async def before_loop(self) -> None:
        await self.client.wait_until_ready()

    async def handleProblemAlerts(self, dow: int, hour: int, minInterval: int | None):
        
        async def handleProblem(problem: Problem):
            if problem.serverID not in self.app.servers:
                print(f"Server ID {problem.serverID} not found in app servers.")
                return
            
            server = self.app.servers[problem.serverID]
            channelID = server.settings.postingChannelID
            if channelID is None:
                print(f"Posting channel ID not set for server {server.serverID}.")
                return
            
            problemService: ProblemService = self.app.problemService
            slug, difficulty = problemService.selectProblem(problem)
            problemInfo = self.app.queryService.getQuestionInfo(slug)

            channel = self.client.get_channel(channelID)
            await channel.send(embed=ProblemEmbed(slug, problemInfo))
            server.addPreviousProblem(slug)  # add the problem to the server's previous problems

        if minInterval is None:
            # if we aren't on a proper interval, we don't need to do anything
            return
        
        bucket = self.app.problemBucket.getBucket(dow, hour, minInterval)
        if bucket is None or len(bucket) == 0:
            return
        
        # FIXME: use the alert builder to build the alerts
        
        for problemKey in bucket:
            # serverid::problemid
            serverID, problemID = problemKey.split("::")
            serverID = int(serverID)
            problemID = int(problemID)
            
            if serverID not in self.app.servers:
                continue
            
            server = self.app.servers[serverID]
            problem = server.problems[problemID]
            await handleProblem(problem)


    async def handleContestAlerts(self, dow: int, hour: int, minute: int):
        HOURS_PER_DAY = 24
        MINS_PER_HOUR = 60
        MINS_PER_INTERVAL = 15
        
        alertBuilder: AlertBuilder = self.app.alertBuilder 
        
        def getContestMinsAway(contestDOW, contestHour, contestInterval):
            # Calculate days away
            daysAway = contestDOW - dow
            if daysAway < 0:
                daysAway += 7

            # Calculate hours away
            hoursAway = contestHour - hour
            if hoursAway < 0:
                daysAway += 1
                hoursAway += HOURS_PER_DAY

            # Calculate minutes away (interval * 15 gives actual minutes)
            contestMinute = contestInterval * MINS_PER_INTERVAL
            minsAway = contestMinute - minute
            if minsAway < 0:
                hoursAway -= 1
                minsAway += MINS_PER_HOUR
                if hoursAway < 0:
                    daysAway -= 1
                    hoursAway += HOURS_PER_DAY

            # Return total minutes (days + hours + minutes)
            return (daysAway * HOURS_PER_DAY * MINS_PER_HOUR + 
                    hoursAway * MINS_PER_HOUR + 
                    minsAway)

        weeklyContestMinsAway = getContestMinsAway(WEEKLY_CONTEST_DOW, WEEKLY_CONTEST_HOUR, WEEKLY_CONTEST_INTERVAL)
        
        # FIXME: biweekly contest is every 2 weeks, so we need to adjust the calculation
        # maybe perform an api query to check if its up 
        biweeklyContestMinsAway = getContestMinsAway(BIWEEKLY_CONTEST_DOW, BIWEEKLY_CONTEST_HOUR, BIWEEKLY_CONTEST_INTERVAL)

        print(f"Minutes until weekly contest: {weeklyContestMinsAway}")
        print(f"Minutes until biweekly contest: {biweeklyContestMinsAway}")

        # Notification intervals (in minutes)
        intervals = [
            15,      # 15 mins
            30,      # 30 mins  
            60,      # 1 hr
            120,     # 2 hrs
            360,     # 6 hrs
            720,     # 12 hrs
            1440,    # 1 day
        ]
        
        if weeklyContestMinsAway in intervals:
            print("Weekly contest is within an alert interval.")
            alerts = alertBuilder.buildContestAlerts(weeklyContestMinsAway, AlertType.CONTEST_TIME_AWAY, AlertType.WEEKLY_CONTEST)
            for alert in alerts:
                if alert.channelID is None:
                    print(f"Alert {alert.alertType} for server {alert.serverID} has no channel ID.")
                    continue
                
                channel = self.client.get_channel(alert.channelID)
                await channel.send(embed=AlertEmbed(alert))
        
        if biweeklyContestMinsAway in intervals:
            print("Biweekly contest is within an alert interval.")
            alerts = alertBuilder.buildContestAlerts(biweeklyContestMinsAway, AlertType.CONTEST_TIME_AWAY, AlertType.BIWEEKLY_CONTEST)
            for alert in alerts:
                if alert.channelID is None:
                    print(f"Alert {alert.alertType} for server {alert.serverID} has no channel ID.")
                    continue
                
                channel = self.client.get_channel(alert.channelID)
                await channel.send(embed=AlertEmbed(alert))

        # for contest alerts
        # needs interval of contest away length
        # we can assume that the contests are technically static times
        # thus these technically won't change
        # set the specific contest times, calculate the current time away
        # check if its a proper interval,
        # if it is, then gather the alerts
        pass

    async def handleStaticAlerts(self, dow: int, hour: int, minInterval: int):
        
        async def sendStaticAlerts(alerts: list[Alert]):
            for alert in alerts:
                if alert.channelID is None:
                    print(f"Alert {alert.alertType} for server {alert.serverID} has no channel ID.")
                    continue
                
                channel = self.client.get_channel(alert.channelID)
                await channel.send(embed=AlertEmbed(alert))
    
        # alerts happen on either 0min or 30mins which are both intervals
        if minInterval is None:
            return
        
        alertBuilder = self.app.alertBuilder
        
        # leetcode weekly: saturday 10 30 pm
        if dow == WEEKLY_CONTEST_DOW and hour == WEEKLY_CONTEST_HOUR and minInterval == WEEKLY_CONTEST_INTERVAL:
            weeklyAlerts = alertBuilder.buildStaticAlerts(StaticTimeAlert.WEEKLY_CONTEST)
            await sendStaticAlerts(weeklyAlerts)

        # leetcode biweekly: sunday 10 30 am
        if dow == BIWEEKLY_CONTEST_DOW and hour == BIWEEKLY_CONTEST_HOUR and minInterval == BIWEEKLY_CONTEST_INTERVAL:
            biweeklyAlerts = alertBuilder.buildStaticAlerts(StaticTimeAlert.BIWEEKLY_CONTEST)
            await sendStaticAlerts(biweeklyAlerts)

        # leetcode daily resets at 8pm
        if hour == DAILY_PROBLEM_HOUR and minInterval == DAILY_PROBLEM_INTERVAL:
            dailyAlerts = alertBuilder.buildStaticAlerts(StaticTimeAlert.DAILY_PROBLEM)
            await sendStaticAlerts(dailyAlerts)


async def setup(client: commands.Bot) -> None: 
    await client.add_cog(Looper(client))
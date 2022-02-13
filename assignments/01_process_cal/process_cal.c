#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define MAX_LINE_LEN 200
#define MAX_EVENTS 1000

const char* MONTHS[13] = {"",
    "January", "February", "March",
    "April", "May", "June", "July",
    "August", "September", "October",
    "November", "December"
};

typedef struct {
    int day;
    int month;
    int year;
    char dweek[10];
} Date;

typedef struct {
    char description[80];
    char timezone[12];
    char location[80];
    Date date;
    // char dweek[10];
    char start[6];
    char end[16];
} Event;

void readFile(char*, Event*);
void filterEvents(Event*, Event*, Date, Date);
void sortEvents(Event*);
void printEvents(Event*);
int countEvents(Event*);
int compareDates(Date, Date);
int compareTimes(char*, char*);
void swap(Event*, int, int);
Date getDate(char*);
void getTime(struct tm*, char*);
void printLine(char*);

/*
    Function: main
    Description: represents the entry point of the program.
    Inputs:
        - argc: indicates the number of arguments to be passed to the program.
        - argv: an array of strings containing the arguments passed to the program.
    Output: an integer describing the result of the execution of the program:
        - 0: Successful execution.
        - 1: Erroneous execution.
*/
int main(int argc, char* argv[])
{
    // configure arguments
    char startArg[MAX_LINE_LEN];
    sscanf(argv[1], "--start=%s", startArg);

    char endArg[MAX_LINE_LEN];
    sscanf(argv[2], "--end=%s", endArg);

    char filename[MAX_LINE_LEN];
    sscanf(argv[3], "--file=%s", filename);

    Date start = getDate(startArg);
    Date end = getDate(endArg);

    // create, filter and sort events
    Event eventlist[MAX_EVENTS];
    readFile(filename, &eventlist[0]);

    Event calendar[MAX_EVENTS];
    filterEvents(calendar, eventlist, start, end);

    sortEvents(calendar);

    // print formatted calendar
    printEvents(calendar);
}

/*
    Function: readFile
    Description: read events from file and write to list of events
    Input:
        - filename: string representing the path to the file to be read
        - eventlist: pointer to list of events to write to
*/
void readFile(char* filename, Event* eventlist) {
    FILE* calendar = fopen(filename, "r");
    if (calendar == NULL) {
        printf("filename invalid.\n");
        exit(1);
    }

    char temp[255];
    int i = 0;
    fscanf(calendar, "<%s>\n", temp);
    fscanf(calendar, "\t<%s>\n", temp);

    while (strcmp(temp, "</calendar>") != 0 && i <= MAX_EVENTS) {
        fscanf(calendar, "\t\t<description>%[^<]</description>\n", eventlist[i].description);
        fscanf(calendar, "\t\t<timezone>%[^<]</timezone>\n", eventlist[i].timezone);
        fscanf(calendar, "\t\t<location>%[^<]</location>\n", eventlist[i].location);
        fscanf(calendar, "\t\t<day>%[^<]</day>\n", temp);
        eventlist[i].date.day = atoi(temp);
        fscanf(calendar, "\t\t<month>%[^<]</month>\n", temp);
        eventlist[i].date.month = atoi(temp);
        fscanf(calendar, "\t\t<year>%[^<]</year>\n", temp);
        eventlist[i].date.year = atoi(temp);
        fscanf(calendar, "\t\t<dweek>%[^<]</dweek>\n", eventlist[i].date.dweek);
        fscanf(calendar, "\t\t<start>%[^<]</start>\n", eventlist[i].start);
        fscanf(calendar, "\t\t<end>%[^<]</end>\n", eventlist[i].end);
        fscanf(calendar, "\t</%s>\n", temp);
        fscanf(calendar, "%s\n", temp);
        i++;
    }

    fclose(calendar);
}

/*
    Function: filterEvents
    Description: copy events between start and end dates from events to calendar
    Inputs:
        - calendar: pointer to list of events to write to
        - eventlist: pointer to list of events to read from
        - start: date before/on first event
        - end: date on/after last event
*/
void filterEvents(Event* calendar, Event* eventlist, Date start, Date end) {
    int i = 0;
    int j = 0;
    Date cur;
    int numEvents = countEvents(eventlist);

    for (int i = 0; i < numEvents; i++) {
        cur = eventlist[i].date;
        if (compareDates(cur, start) >= 0 && compareDates(cur, end) <= 0) {
            strcpy(calendar[j].description, eventlist[i].description);
            strcpy(calendar[j].timezone, eventlist[i].timezone);
            strcpy(calendar[j].location, eventlist[i].location);
            calendar[j].date = cur;
            strcpy(calendar[j].start, eventlist[i].start);
            strcpy(calendar[j].end, eventlist[i].end);
            j++;
        }
    }

    calendar[j].date.year = 0;
}

/*
    Function: sortEvents
    Description: sort list of events by date & time
    Input:
        - calendar: pointer to list of events to be sorted
*/
void sortEvents(Event* calendar) {
    int numEvents = countEvents(calendar);
    int min;
    for (int i = 0; i < numEvents; i++) {
        min = i;
        for (int j = i+1; j < numEvents; j++) {
            int comparison = compareDates(calendar[min].date, calendar[j].date);
            if (comparison > 0) {
                min = j;
            } else if (!comparison && compareTimes(calendar[min].start, calendar[j].start) >= 0) {
                min = j;
            }
        }
        swap(calendar, i, min);
    }
}

/*
    Function: printEvents
    Description: print events according to specified format (headers incl.)
    Input:
        - calendar: pointer to list of sorted events to be printed
*/
void printEvents(Event* calendar) {
    int numEvents = countEvents(calendar);
    Event cur;
    Date date;
    struct tm starttime;
    struct tm endtime;
    char start[MAX_LINE_LEN];
    char end[MAX_LINE_LEN];
    char line[MAX_LINE_LEN];

    for (int i = 0; i < numEvents; i++) {
        cur = calendar[i];
        getTime(&starttime, cur.start);
        getTime(&endtime, cur.end);

        if (i == 0 || compareDates(calendar[i-1].date, cur.date)) {
            date = cur.date;
            char header[MAX_LINE_LEN];
            if (i != 0) {
                printf("\n");
            }
            sprintf(header, "%s %d, %d (%s)", MONTHS[date.month], date.day, date.year, date.dweek);
            printf("%s\n", header);
            printLine(header);
        }

        strftime(start, MAX_EVENTS, "%I:%M %p", &starttime);
        strftime(end, MAX_EVENTS, "%I:%M %p", &endtime);
        sprintf(line, "%s {{%s}} | %s", cur.description, cur.location, cur.timezone);
        printf("%s to %s: %s", start, end, line);

        if (i < numEvents - 1) {
            printf("\n");
        }
    }
}

/*
    Function: countEvents
    Description: count number of events in a given list
    Input:
        - calendar: pointer to list of events to count
    Output: number of events with year != 0
*/
int countEvents(Event* calendar) {
    int i = 0;
    // date.year == 0 implies event hasn't been initialized
    while (calendar[i].date.year != 0 && i < MAX_EVENTS) {
        i++;
    }
    return i;
}

/*
    Function: compareDates
    Description: compare two dates date1 and date2
    Inputs:
        - date1: first struct of type Date
        - date2: second struct of type Date
    Output: 0 if date1 = date2, -1 if date1 before date2, daydiff > 0 if date1 after date2
*/
int compareDates(Date date1, Date date2) {
    int yeardiff = date1.year - date2.year;
    int monthdiff = date1.month - date2.month;
    int daydiff = date1.day - date2.day;

    if (yeardiff > 0) {
        return yeardiff;
    } else if (yeardiff == 0) {
        if (monthdiff > 0) {
            return monthdiff;
        } else if (monthdiff == 0) {
            if (daydiff >= 0) {
                return daydiff;
            }
        }
    }
    return -1;
}

/*
    Function: compareTimes
    Description: compare two times t1 and t2
    Inputs:
        - t1: first time with format "hh:mm"
        - t2: second time with format "hh:mm"
    Output: 0 if t1 = t2, -1 if t1 before t2, mindiff > 0 if t1 after t2
*/
int compareTimes(char* t1, char* t2) {
    int hour1, hour2, min1, min2;

    sscanf(t1, "%d:%d", &hour1, &min1);
    sscanf(t2, "%d:%d", &hour2, &min2);

    int hourdiff = hour1 - hour2;
    int mindiff = min1 - min2;

    if (hourdiff > 0) {
        return hourdiff;
    } else if (hourdiff == 0) {
        if (mindiff >= 0) {
            return mindiff;
        }
    }
    return -1;
}

/*
    Function: swap
    Description: swap events with indices e1 and e2 in a calendar
    Inputs:
        - eventlist: list of type Event
        - e1: index of first item to swap
        - e2: index of second item to swap
*/
void swap(Event* eventlist, int e1, int e2) {
    Event temp = eventlist[e1];
    eventlist[e1] = eventlist[e2];
    eventlist[e2] = temp;
}

/*
    Function: getDate
    Description: get struct of type Date from string
    Input:
        - string: date string of format "yyyy/mm/dd"
    Output: struct of type Date containing year, month and day
*/
Date getDate(char* string) {
    Date date;
    char* token = strtok(string, "/");
    date.year = atoi(token);
    token = strtok(NULL, "/");
    date.month = atoi(token);
    token = strtok(NULL, "/");
    date.day = atoi(token);
    return date;
}

/*
    Function: getTime
    Description: initialize struct of type tm from string
    Inputs:
        - time: pointer to struct of type tm to be written to
        - string: time string of format "hh:mm"
    Output: struct of type Date containing year, month and day
*/
void getTime(struct tm* time, char* string) {
    int hour, min;
    sscanf(string, "%d:%d", &hour, &min);
    time->tm_hour = hour;
    time->tm_min = min;
}

/*
    Function: printLine
    Description: print line beneath header of same length
    Input:
        - header: string to be underlined
*/
void printLine(char* header) {
    int length = strlen(header);
    for (int i = 1; i < length; i++) {
        printf("-");
    }
    printf("-\n");
}

import plistlib
import numpy as np
import matplotlib.pyplot as plt
import argparse

# get the tracks of a playlist
def getPlist(fileName):
    with open(fileName, "rb") as fp:
        return plistlib.load(fp)

def findDuplicates(fileName):
    print("Finding duplicate tracks in %s... " % fileName)
    # read in a playlist
    plist = getPlist(fileName)
    # get the tracks from the Tracks dictionary
    tracks = plist['Tracks']
    # create a track name dictionary
    trackNames = {}
    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            # look for existing entries
            if name in trackNames:
                # if a name and duration match, increment the count
                # round the track length to the nearest second
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                # add dictionary entry as tuple (duration count)
                trackNames[name] = (duration, 1)
        except:
            # ignore
            pass

    # store duplicates as (name, count) tuples
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    # save duplicates to a file
    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
    else:
        print("No duplicate tracks found!")
    f = open("dup.txt","w")
    for val in dups:
        f.write("%d %s\n" % (val[0], val[1]))
    f.close()

# find common tracks between two playlists
def findCommonTracks(fileNames):
    # a list of sets of track names
    trackInfoSets = []
    for fileName in fileNames:
        # create a new set
        trackInfos = set()
        # read in playlist
        plist = getPlist(fileName)
        # get the tracks
        tracks = plist['Tracks']
        # iterate through the tracks
        for trackId, track in tracks.items():
            try:
                # add the track info to a set
                duration = track['Total Time']//1000
                trackInfos.add((track['Name'],duration))
            except:
                # ignore
                pass
        # add to list
        trackInfoSets.append(trackInfos)
    # get the set of common tracks
    commonTracks = set.intersection(*trackInfoSets)
    # write to file
    if len(commonTracks) > 0:
        with open('common.txt','wb') as f:
            for val in commonTracks:
                s = "%s %.1fmin\n" % (val[0], val[1]/60)
                f.write(s.encode('UTF-8'))
        print("%d common tracks found. "
              "Track names written to common.txt." % len(commonTracks))
    else:
        print("No common tracks!")

# collect rating and total time data
def plotStats(fileName):
    # read in a playlist
    plist = getPlist(fileName)
    # get tracks from the plist
    tracks = plist['Tracks']
    # create lists of song ratings and track durations
    ratings = []
    durations = []
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            # ignore
            pass
    # ensure that valid data was collected
    if (not ratings) or (not durations):
        print("No valid Album Rating/Total Time data in %s." % fileName)
        return

    # scatter plot
    x = np.array(durations, np.int32)
    # convert to minutes
    x = x/60000
    y = np.array(ratings, np.int32)
    # plot 
    plt.subplot(2, 1, 1)
    plt.plot(x, y, 'o')
    plt.axis([0, 1.05*np.max(x), -1, 110])
    plt.xlabel('Track duration')
    plt.ylabel('Track rating')
    # plot histogram
    plt.subplot(2, 1, 2)
    plt.hist(x, bins=20)
    plt.xlabel('Track duration')
    plt.ylabel('Count')
    plt.show()


def main():
    # create parser
    descStr = """
    This program analyzes playlist files(.xml) exported from iTunes
    """
    parser = argparse.ArgumentParser(description=descStr)
    # add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # add expected arguments
    group.add_argument("--common", nargs='*', dest='plFiles', required=False)
    group.add_argument("--stats", dest='plFile', required=False)
    group.add_argument("--dup", dest='plFileD', required=False)

    # parse args
    args = parser.parse_args()

    if args.plFiles:
        # find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")


if __name__ == '__main__':
    main()
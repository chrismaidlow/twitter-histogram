#######################################################################
# Computer Project #9
# 
# Algorithm
#
#   Prompt for file until opened. Parse through data creating list of lists. 
#   Use accompanying functions to parse body of each line and check hashtag
#   validity. Use dictionarys and sets to organize, display, and gain info 
#   from data using histograms and plotting. Display results to end user
#
########################################################################

import string, calendar, pylab

import csv

import string

import operator

MONTH_NAMES = [calendar.month_name[month] for month in range(1,13)]

def open_file():
    '''Ask for filename until correct input'''
    
    filename = input("Input a filename: ")
    
    while True:
    
        try:
            
            fp = open(filename)
            print()
            return fp
            
        except FileNotFoundError:
            
            print("Error in input filename. Please try again.") 
            
            filename = input("Input a filename: ")
            
            
def validate_hashtag(s):
    '''Validate string is a valid hashtag via twitter's standards'''
    
    #skip hashtag
    for ch in s[1:]:
        
        #if tag contains punctuation = False
        if ch in string.punctuation:
            
            return False
        
    #If length 2 and second character a number return false
    if len(s) == 2:
        
        if s[1].isdigit():
            
            return False
        
        else:
            
            return True
    else:
        
        return True
        
def get_hashtags(body):
    '''parse data string for any hashtags contained within'''
    
    tweet_list = []
    
    #search through text body until finding first hashtag
    beg = body.find("#")
                          
    #find returns -1 when no ch found - this will break loop
    while beg != -1:
        
        #Ebd is signified by space
        end = body.find(' ', beg)
        
        #This guarentees no cutoff if last character in body included in hash
        if end == -1:
            
            tweet = body[beg:]
            
        else:
            
            tweet = body[beg:end]

        #Call validate tweet function for final check of legitamacy 
        if validate_hashtag(tweet) == True:
            
            #Append tweet
            tweet_list.append(tweet)
        
        beg = body.find("#", end)
                        
    return tweet_list

def read_data(fp):
    '''Parse through data file creating a list of three entry lists'''
    
    master_list = []

    for line in fp:
        
        three_entry_list = []
        tweet_list = []
        
        sep = line.strip().split(",")
        
        username = sep[0]
        month = int(sep[1])
        body = sep[2]
        
        three_entry_list.append(username)
        three_entry_list.append(month)
        
        #returns list of hashtags for body of current line
        tweet_list = get_hashtags(body)
        
        #Each 3 entry list to be appended to the master list
        three_entry_list.append(tweet_list)
        
        master_list.append(three_entry_list)
    
    return master_list

def get_histogram_tag_count_for_users(data,usernames):
    '''Create histograms of total times hashtag used'''
    
    hist_dict = {}
    
    for item in data:
        
        user = item[0]
        
        #check if user in usernames
        if user in usernames:
        
            hashes = item[2]
            
            for tag in hashes:
                
                #if tag in dict iterate count
                if tag in hist_dict:
                    
                    hist_dict[tag] += 1
                
                #Add to dict if new
                else:
                    
                    hist_dict[tag] = 1
    
    return hist_dict

def get_tags_by_month_for_users(data,usernames):
    ''' Create list of tuples containing used hashtags for each month '''
    
    #list of months and their set 
    tup_list = [(1,set()),(2,set()),(3,set()),(4,set()),(5,set()),(6,set()),(7,set()),(8,set()),(9,set()),(10,set()),(11,set()),(12,set())]
    
    #iterate through data
    for item in data:
        
        user = item[0]
        
        #check if member
        if user in usernames:
        
            month = item[1]
            
            hashtags = item[2]
            
            for item in tup_list:
                
                entry_month = item[0]
                
                set_month = item[1]
                
                #if equal add month to set
                
                if month == entry_month:
                    
                    for item in hashtags:
                        
                        set_month.add(item)            
                        
    return tup_list
                    
def get_user_names(L):
    '''Parse data file and create list of usernames'''
    
    username_list = []
    
    #Add unique names to list
    for item in L:

        name = item[0]
        
        if name not in username_list:
        
            username_list.append(name)
    
    #sort alpha        
    sorted_list = sorted(username_list)
    
    return sorted_list

def three_most_common_hashtags_combined(data,usernames):
    '''Create list of the three most common hashtags combined'''
    
    common_list = []
    
    #Call external function to get dictionary
    diction = get_histogram_tag_count_for_users(data,usernames)
    
    #iterate throught dict
    for key, value in diction.items():
        
        tup = (value, key)

        common_list.append(tup)        
     
    #Sort by largest
    by_count = sorted(common_list, reverse = True)
    
    #Slice count
    sliced_count = by_count[0:3]
    
    return sliced_count
        
def three_most_common_hashtags_individuals(data,usernames):
    '''Create list of three most common hashtags for individual users'''
    
    common_list = []
    
    for user in usernames:
        
        #Call external function
        diction = get_histogram_tag_count_for_users(data,user)
        
        #iterate through dictionary
        for key, value in diction.items():
        
            #include username for list
            tup = (value, key, user)

            common_list.append(tup)        
    
    #sort and slice    
    by_count = sorted(common_list, reverse = True)
    
    sliced_count = by_count[0:3]
    
    return sliced_count  
            
def similarity(data,user1,user2):
    '''Create list of sets for each month showing intersection of hashtags'''

    #Create set one and two by calling function
    set1 = get_tags_by_month_for_users(data,[user1])
     
    set2 = get_tags_by_month_for_users(data,[user2])
     
    return_list = []
    
    count = 0
    
    #for each month find intersecting hashtags, create tuple, append to list
    for item in set1:
        
        set_dat = item[1]
        
        set_dat2 = set2[count]
        
        count += 1
    
        inter = set_dat & set_dat2[1]
        
        tup = (count, inter)
        
        return_list.append(tup)
           
    return return_list
     
        
def plot_similarity(x_list,y_list,name1,name2):
    '''Plot y vs. x with name1 and name2 in the title.'''
    
    pylab.plot(x_list,y_list)
    pylab.xticks(x_list,MONTH_NAMES,rotation=45,ha='right')
    pylab.ylabel('Hashtag Similarity')
    pylab.title('Twitter Similarity Between '+name1+' and '+name2)
    pylab.tight_layout()
    pylab.show()
    # the next line is simply to illustrate how to save the plot
    # leave it commented out in the version you submit
    #pylab.savefig("plot.png")


def main():
    """Main driver of the program"""
    
    # Open the file
    # Read the data from the file
    fp = open_file()
    data = read_data(fp)
    
    # Create username list from data    
    usernames = get_user_names(data)
    
    # Calculate the top three hashtags combined for all users
    combined = three_most_common_hashtags_combined(data,usernames)
    
    # Calculate the top three hashtags individually for all users
    indi = three_most_common_hashtags_individuals(data,usernames)
    
    print("Top Three Hashtags Combined")
    print("{:>6s} {:<20s}".format("Count","Hashtag"))
    
    #loop for printing
    for item in combined:
        
        count = item[0]
        
        hashtag = item[1]
                       
        print("{:>6s} {:<20s}".format(str(count),hashtag))
    
    print()
    
    print("Top Three Hashtags by Individual")
    print("{:>6s} {:<20s} {:<20s}".format("Count","Hashtag","User"))
    
    #loop for printing
    for item in indi:
        
        count = item[0]
        
        hashtag = item[1]
        
        user = item[2]
        
        print("{:>6s} {:<20s} {:<20s}".format(str(count),hashtag,user))
    
    print()
    
    usernames_str = "MSUnews, WKAR, WKARnewsroom, michiganstateu"
    
    #create two swtitches
    u1 = False
    
    u2 = False
        
    print("Usernames: ", usernames_str)
    while True:
        # prompt for and validate user names
        try:
            
            user_str = input("Input two user names from the list, comma separated: ")
            
            users = user_str.split(",")
            
            user1 = users[0].strip()
            
            user2 = users[1].strip()
            
            #if users both in usernames exit loop and move on with program
            if user1 in usernames:
                
                u1 = True
                
            if user2 in usernames:
                
                u2 = True
                
            if u2 == True and u1 == True:
                
                break
            
            else:
                
                raise ValueError
        
        except:
            
            print("Error in user names.  Please try again") 
            
    # calculate similarity here
    simil = similarity(data,user1,user2)
    
    print()
    
    print("Similarities for "+users[0].strip()+" and "+users[1].strip())
    
    
    print("{:12s}{:6s}".format("Month","Count"))
    
    count = 0
    
    #convert numbers to month names and print
    
    for item in simil:
        
        month = (item[0] - 1)
        
        true_month = MONTH_NAMES[month]
        
        for thing in item[1]:
            
            count +=1
            
        print("{:12s}{:6s}".format(true_month,str(count)))
        
        count = 0
    
    print()
    
    #Prompt for a plot
    choice = input("Do you want to plot (yes/no)?: ")
    
    #prepare x and y list for plotting
    
    x_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    
    y_list = []
    
    count = 0
    
    for item in simil:
        
        common_hash = item[1]
        
        for item in common_hash:
        
            count += 1
            
        y_list.append(count)
            
        count = 0
    
    if choice.lower() == 'yes':
        #create x_list and y_list
        plot_similarity(x_list,y_list,users[0],users[1])

if __name__ == '__main__':
    main()
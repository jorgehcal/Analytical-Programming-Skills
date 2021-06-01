
#Suppose that we are interested in making a survey of 5 questions,and in
#repeating the survey when some time has passed. This second edition of the
#survey will be answered by two groups of people: new people joining the
#survey and people who have already answered the first survey. If the questions
#are related to life conditions (for example) in people's residence, and the
#interviewed person has answered the first survey, and not changed of residence,
#then it does not make sense to repeat the same questions (this would probably
#annoy him/her). In order not to repeat the questions if the circumstances
#have not changed, we add a FILTER QUESTION. In our case, it would be:

#Have you changed your residence since the last Survey?

#If the answer is negative, then we do not repeat the questions. The dataframe 
#gathering the information of 2 surveys has columns

# V1 V2 V3 V4 V5 F W1 W2 W3 W4 W5

#where V are the questions during the first survey, W the questions
#during the second one, and F the filter question. Note that W are the 
#same questions than their corresponding V, but new people may join the 
#survey. If the filter activates for the people who already answered the
#first survey, then the values of W are filled in withs NA's. One common 
#task in processing data from surveys is to recuperate the information from
#the first survey, of the people who activates the filter. In the following R
#code, I will show how to proceed for an easy dataframe like the one that I 
#have already mentioned.


#1) Creation of an example dataframe.
nfil <- 20
ncol <- 5
df  <- c(1:(nfil*ncol))

for (i in 1:(nfil*ncol)) df[i]<-runif(1,1,4) 
df <- matrix(df, nrow=nfil)

df  <- as.data.frame(df) #Creating this dataframe, the columns are named V1,...,V5

#To introduce a filter to our dataframe, we add one column to df, filter,
#to use as a Filter Question (with example values)
filter <- c(1:20)
for (i in 1:nfil) filter[i]<-trunc(runif(1,1,4))   #Filter takes 3 values: 1, 2, 3, 

#and we add it to df
df$f <- filter

#Now we add the variables corresponding to the second survey:
set <- "df"
for (i in 1:ncol) eval(parse(text=paste(set,"$",paste("W",i,"<-NA", sep=""))))

#and we obtain a dataframe of people who has answered both the
#first and the second edition of the survey, since all the rows
#for the V variables are filled.

#2) Copying the information.
#We make the list of the old variables and their corresponding new variables.
nvar_old <- c("V1","V2","V3","V4","V5")
nvar_new <- c("W1","W2","W3","W4","W5")

#Finally, we iterate to fill the values of the new variables with 
#the values from the old variables. I assume the filter activates
#when f == 2.
for (k in 1:nfil) {
  if (df$f[k] == 2) {
    for (i in 1:ncol){
      
      old <- nvar_old[i]
      new <- nvar_new[i]
      eval(parse(text=paste(set,"$",new,"[",k,"] <- ", set,"$",old,"[",k,"]")))
    }    
  }   
}

#As a result, we recuperate the information as desired.


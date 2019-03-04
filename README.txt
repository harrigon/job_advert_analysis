Job Advert Information
Harrigan Davenport

##TO DO
-Remove id from processed jobs, not useful
-Expand stop words
-Need to clean this up comment wise
-For god sake stop mixing up camelCase and underscores everywhere

This project is designed to automatically download the description of software engineering jobs and perform frequency
analysis into them. This is for the end goal of extracting information of what types of soft skills employers are
looking for from their new applicants.

------DOWNLOADER FILES
Currently there are two downloader files, tradeMe_job_downloader.py and github_job_downloader.py. These programs connect
to trademe.co.nz and jobs.github.com and make GET requests to the respective APIs to automatically download the job advert
information on the site. Once the descriptions are downloaded they are saved into .xls files in '/Job Descriptions'.

Both files only need to be run once to save all of the information, but can be rerun to ensure the information is upto date.

TradeMe and GitHub jobs were both chosen because of their easy to use APIs. For TradeMe the jobs are reduces to only
those in the appropriate categories. For GitHub Jobs all jobs are downloaded as the site is designed only for software
engineering and software related jobs.The downloaders could definitely be expanded in the future, with the only issue being
that many of the largest job sites (ie SEEK, Indeed) do not open their API up to external use.

TradeMe does require CONSUMERKEY and CONSUMERSECRET when accessing their API. This can be obtained through a dev account
on trademe.co.nz. As TradeMe is a general employment websites, only jobs from the following categoires were considered;
Programming and Development, Testing, Webdesign and Architects.


-----JOB ANALYSIS
This program requires that the two downloader files have successfully run. It takes the output of the downloaders and
processes them, by removing general stopwords (eg. to, the, is, at) as well as the type of job application based stopwords that
are found on job adverts(eg. careers, opportunity, CV, visa, etc). The frequency of the words are then calculated.

job_analysis.py takes two required arguments, as follows;

    ARGUMENT 1 - softSkills | allSkills
    ARGUMENT 2 - stem | noStem

The first argument determines what skills you are searching for in the word frequency. If softSkills is supplied, the
job descriptions will have the general and job application stop words removed, as well as those relating to hard skills (ie language names,
technologies, tools, etc.). If allSkills is supplied then only general and job application stop words will be removed, all hardskill words
will remain

The second argument determines if the words in the description are to be stemmed or not. The advantage to stemming is that
it is easier to filter out stop words. An advantage to not stemming is that context it better preserved, giving more meaning
to the frequency analysis (For example, we know that developer and developing have very different usages, but if stemmed
count as the same word).

The input to this script are the two job description files found in /Job Descriptions. These files are githubJobDescriptions.xls
and tradeMeJobDescriptions.xls and are the output files of the two downloaders described above.

This script has two outputs
   1 - The processed job is saved in /Processed Jobs. It is a csv file named after the options chosen when running the script.
   The csv has the job Id, followed by the job description after processing.
   ##Am going to remove id in future, serves no use
   2 - The word frequency is saved in /Word Frequency. It is a csv file named after the options chosen when running the script.
   The csv contains each word that appears in any description, and the total frequency of it in all descriptions.

Note: The following lines of code must be run the first time running the code, to import and download nltk's standard
list of stopwords

#import nltk
#nltk.download('stopwords')



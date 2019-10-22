# Python script for cleaning the performance and conversion csv files
#
# To execute the script (assuming you have Python 3.X installed) use
# python clean_data.py
#
# The script assumes your raw data is in a folder called Raw_data/ one
# level above your script.
#
# The cleaned data will be written to a folder called Clean_data/
# which is also one level above your script and must exist prior to
# running the script.

# Import required Python packages
import pandas as pd
import numpy as np

# Read in the raw data files. The raw csv files have header information which
# must be omitted when reading the data in. The header=? option controls how
# many lines will be skipped over before reading in the data.
uwe_performance_df=pd.read_csv('../Raw_data/UWE/Pivigo_UWE_Performance.csv',header=9)
tees_performance_df=pd.read_csv('../Raw_data/Teesside/Pivigo_Tees_Performance.csv',header=9)
uwe_conversion_df=pd.read_csv('../Raw_data/UWE/Pivigo_UWE_Conversion.csv',header=9)
tees_conversion_df=pd.read_csv('../Raw_data/Teesside/Pivigo_Tees_Conversion.csv',header=10)

# Append both performance files and both conversion files, so we don't have to
# work separately with each file. If more data is added in future it may be
# necessary to process each University dataset invidually as the performance
# file can get very large and thus you may run out of memory.
performance_df=uwe_performance_df.append(tees_performance_df,ignore_index=True)
conversion_df=uwe_conversion_df.append(tees_conversion_df,ignore_index=True)

# Check that the length of our combined datasets adds up to the sum of the
# components. The assert will fail and stop the code if this test is not true
assert(len(performance_df)==len(uwe_performance_df)+len(tees_performance_df))
assert(len(conversion_df)==len(uwe_conversion_df)+len(tees_conversion_df))

# Having combied the data into a single dataframe for performance and
# conversion. We can remove (delete) the original dataframes to save some memory
del uwe_performance_df
del uwe_conversion_df
del tees_performance_df
del tees_conversion_df

# Remove rows that have --- string. These indicate rows that have total sums
# of numerical values. These are not useful and can easily be recomputed should
# we later require them.
dashes_idx=performance_df[performance_df['Campaign ID']=='---']
performance_df=performance_df.drop(dashes_idx.index,axis=0)
dashes_idx=conversion_df[conversion_df['Campaign ID']=='---']
conversion_df=conversion_df.drop(dashes_idx.index,axis=0)

# Transform ID columns to string type
cols_to_mod=['Advertiser ID','Campaign ID','Site ID (DCM)']
for c in cols_to_mod:
    performance_df[c]=performance_df[c].astype(str)
    conversion_df[c] = conversion_df[c].astype(str)

# We fix negatives values on performance numerical columns Impressions,
# Clicks, Click Rate and Active View: Measurable Impressions. They all should
# be positive
cols_to_mod=['Impressions','Clicks','Active View: Measurable Impressions']
for c in cols_to_mod:
    performance_df[c] = performance_df[c].abs()

# In both files, 0x0 Placement Pixel Size are equivalent to 1x1, so we replace
# 0x0 by 1x1
performance_df.loc[performance_df['Placement Pixel Size']=='0 x 0',
                   'Placement Pixel Size'] = '1 x 1'
conversion_df.loc[conversion_df['Placement Pixel Size']=='0 x 0',
                  'Placement Pixel Size'] = '1 x 1'

# We group the different activities into bigger groups. The grouping suggestions
# were provided by SMRS.
conversion_df['Activity Bin'] = conversion_df['Activity']
act_bins = {
    'Apply Online Click' : 'Application',
    'Apply Now UG Button Click' : 'Application',
    'Apply Now PG Button Click' : 'Application',
    'Apply Online Complete' : 'Application',
    'UG UCAS Application (Exit)' : 'Application',
    'Part-time PDF Application Form' : 'Application',
    'International UG Online Application Form Complete (UWEB)' : 'Application',
    'UCAS Page Exit' : 'Application',
    'PG Application' : 'Application',
    'Launch Space Application' : 'Application',

    'Book an Open Day' : 'Open Day',
    'Book Now - Success' : 'Open Day',
    'UG Open Day Complete': 'Open Day',
    'Open Day': 'Open Day',
    'UG Open Day Registration': 'Open Day',
    'PG Open Day Complete': 'Open Day',
    'Part-Time Open Day Complete': 'Open Day',
    'PG Open Day Form': 'Open Day',
    'Book an Open Day Click': 'Open Day',
    'Open Day Landing Page': 'Open Day',
    'PG Open Day Registration': 'Open Day',
    'PG Open Event 22 May 2019': 'Open Day',
    'PG Open Event 24 April 2019': 'Open Day',
    'UG Open Day 16 November 2019': 'Open Day',
    'UG Open Day 2 November 2019': 'Open Day',
    'UG Open Day 8 June 2019': 'Open Day',
    'PG Open Event 17 Apr 2019': 'Open Day',

    'Prospectus' : 'Prospectus',
    'Prospectus Request' : 'Prospectus',
    'PG Prospectus Request Complete' : 'Prospectus',
    'Prospectus Request Complete' : 'Prospectus',
    'UG Prospectus Request Complete' : 'Prospectus',
    'UG Course Details Download' : 'Prospectus',

    'Course Enquiry - Thank You' : 'Enquiry',
    'International Enquiry' : 'Enquiry',
    'Clearing Enquiry Form Complete' : 'Enquiry',
    'International Enquiry Contact Us Confirmation (Microsite)' : 'Enquiry',
    'ODL Enquiry Complete' : 'Enquiry',
    'BBEC Enquiry Confirmation Page August' : 'Enquiry',
    'Intl Enquiry [UWE] OLD' : 'Enquiry',
    'Business Email' : 'Enquiry',
    'Offline Conversion Tracking - Phone Call' : 'Enquiry',
    'Click to Call' : 'Enquiry',
    'BBEC - Enquire Now Online Survey Click' : 'Enquiry',
    'Professional Development Course Enquiries Button Click' : 'Enquiry',
    'Enquire Now Click (The Forge)' : 'Enquiry',
    'Degree Apprenticeships Mail to Click' : 'Enquiry',
    'Exec Education Mail to Click' : 'Enquiry',
    'Faculty of Arts Creative Industries and Education Mail to' : 'Enquiry',
    'Faculty of Business and Law Mail to' : 'Enquiry',
    'Faculty of Environment and Technology Mail to' : 'Enquiry',
    'Faculty of Health and Applied Sciences Mail to' : 'Enquiry',
    'Exec Education Contact Us Button Click' : 'Enquiry',
    'HDA Enquire Now' : 'Enquiry',
    'International Enquire Now (Microsite)' : 'Enquiry',
    'International Enquire Now (UWEB)' : 'Enquiry',
    'Live Chat Started' : 'Enquiry',
    'Chat Now - International' : 'Enquiry',
    'Cyber Webinar Book' : 'Enquiry',

    'Clearing Page' : 'Clearing',
    'Clearing Page [30 Dwell Time]' : 'Clearing',
    'Clearing Landing Page' : 'Clearing',
    'Clearing Find Your Course Click' : 'Clearing',

    'PG Homepage' : 'Homepage',
    'Part-time Homepage' : 'Homepage',
    'UG Homepage' : 'Homepage',
    'International Homepage' : 'Homepage',

    'Study Pages' : 'Other Pages',
    'SOH School Pages' : 'Other Pages',
    'SSE School Pages' : 'Other Pages',
    'Undergraduate Pages' : 'Other Pages',
    'SOC School Pages' : 'Other Pages',
    'HDA Course Page' : 'Other Pages',
    'UG Scholarship' : 'Other Pages',
    'Part-Time Course' : 'Other Pages',
    'Global Floodlight' : 'Other Pages',
    'Course View' : 'Other Pages',

    'UWE International Global AUD REM' : 'Rare',
    'I4G External Site Link Click' : 'Rare',
}
conversion_df['Activity Bin'].replace(act_bins, inplace=True)

# Fix the inconsistencies in the media names
fixed_site_names=pd.read_excel("Site_names.xlsx", header=None)
new_sites_dict={}
for index,rows in fixed_site_names.iterrows():
    new_sites_dict[rows[0]]=rows[1]

performance_df[['Site (DCM)']]=performance_df[['Site (DCM)']].replace(new_sites_dict)
conversion_df[['Site (DCM)']]=conversion_df[['Site (DCM)']].replace(new_sites_dict)

# Now we create the unique ID columns for the performance dataset
performance_df['ID']=performance_df['Advertiser ID'].str.cat((
    performance_df['Campaign ID'],
    performance_df['Site ID (DCM)'],
    performance_df['Creative ID'],
    performance_df['Creative Type'],
    performance_df['Placement Pixel Size'],
    performance_df['Platform Type']),sep='_')

# Create unique IDs for the conversion dataset
conversion_df['ID']=conversion_df['Advertiser ID'].str.cat((
    conversion_df['Campaign ID'],
    conversion_df['Site ID (DCM)'],
    conversion_df['Creative ID'],
    conversion_df['Creative Type'],
    conversion_df['Placement Pixel Size'],
    conversion_df['Platform Type']),sep='_')

# Write out the cleaned data to csv files
performance_df.to_csv("../Clean_data/Clean_performance.csv", index=False)
conversion_df.to_csv('../Clean_data/Clean_conversion.csv',index=False)

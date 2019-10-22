# Python script for cleaning the performance and conversion csv files
#
# To execute the script (assuming you have Python 3.X installed) use
# python clean_data_per_uni.py uni_name
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
import sys

args = sys.argv
uni = str(args[1])

# Read in the raw data files. The raw csv files have header information which
# must be omitted when reading the data in. The header=? option controls how
# many lines will be skipped over before reading in the data.
if uni == 'UWE':
    header_perf=9
    header_conv=9
    performance_df = pd.read_csv('../Raw_data/%s/Pivigo_%s_Performance.csv' % (uni,uni),header=header_perf)
    conversion_df=pd.read_csv('../Raw_data/%s/Pivigo_%s_Conversion.csv' % (uni,uni),header=header_conv)
elif uni == 'Teesside':
    header_perf=9
    header_conv=10
    performance_df = pd.read_csv('../Raw_data/%s/Pivigo_%s_Performance.csv' % (uni,uni[0:4]),header=header_perf)
    conversion_df=pd.read_csv('../Raw_data/%s/Pivigo_%s_Conversion.csv' % (uni,uni[0:4]),header=header_conv)
elif uni == 'ARU' or uni == 'OBU' or uni=='Solent':
    header_perf=11
    header_conv=11
    performance_df = pd.read_excel('../Raw_data/%s/Pivigo_%s_Performance.xls' % (uni,uni),header=header_perf)
    conversion_df=pd.read_csv('../Raw_data/%s/Pivigo_%s_Conversion.csv' % (uni,uni),header=header_conv)
else:
    print("You've put in a University that's not in your folders you silly goose!")
    raise()

#### Change this later to get the dfs out of the if statements, but make sure you're uni names are uniform!

# Remove rows that have --- string. These indicate rows that have total sums
# of numerical values. These are not useful and can easily be recomputed should
# we later require them.
dashes_idx=performance_df[performance_df['Campaign ID']=='---']
performance_df=performance_df.drop(dashes_idx.index,axis=0)
dashes_idx=conversion_df[conversion_df['Campaign ID']=='---']
conversion_df=conversion_df.drop(dashes_idx.index,axis=0)

### Check to see if you have Advertiser ID in the performance file and, if not, create it
if 'Advertiser' not in performance_df.columns:
    performance_df['Advertiser'] = conversion_df['Advertiser'].unique()[0]

# Transform ID columns to string type
cols_to_mod=['Advertiser ID','Campaign ID','Site ID (DCM)', 'Creative ID', 'Placement Pixel Size']
for c in cols_to_mod:
    performance_df[c] = performance_df[c].astype(str)
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
    'PG Apply Online Clicks' : 'Application',
    'UCAS Exit' : 'Application',
    'International UG Apply Clicks' : 'Application',
    'How to Apply Click (UG)' : 'Application',
    'How to Apply Click (PG)' : 'Application',
    'Apply Now Click (PG)' : 'Application',
    'PG Apply Clicks' : 'Application',


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
    'Open Day Booking Complete' : 'Open Day',
    'Open Day Click to Book' : 'Open Day',
    'Open Day Book Now Click (UG)' : 'Open Day',
    'Open Day Book Now Click (PG)' : 'Open Day',
    'Open Day Book Now Click (Swindon)' : 'Open Day',
    'Open Day Page' : 'Open Day',
    'Open Day Clicks' : 'Open Day',
    'Open Day Booking Complete' : 'Open Day',
    'Eventbrite Click' : 'Open Day',

    'Prospectus' : 'Prospectus',
    'Prospectus Request' : 'Prospectus',
    'PG Prospectus Request Complete' : 'Prospectus',
    'Prospectus Request Complete' : 'Prospectus',
    'UG Prospectus Request Complete' : 'Prospectus',
    'UG Course Details Download' : 'Prospectus',
    'UG Prospectus Request' : 'Prospectus',
    'Prospectus Downloads' : 'Prospectus',
    '52 things to do' : 'Prospectus',

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
    'Click to Email' : 'Enquiry',
    'Enquiry Form Complete' : 'Enquiry',
    'International - Keep In Touch Form' : 'Enquiry',

    'Clearing Page' : 'Clearing',
    'Clearing Page [30 Dwell Time]' : 'Clearing',
    'Clearing Landing Page' : 'Clearing',
    'Clearing Find Your Course Click' : 'Clearing',
    'Clearing - Register For Clearing Updates Click' : 'Clearing',
    'Clearing - Landing' : 'Clearing',
    'Clearing - Landing (30secs)' : 'Clearing',
    'Clearing - Sign Up Click (Gecko)' : 'Clearing',
    'Clearing - YouTube Click' : 'Clearing',
    'Clearing - Click to Call' : 'Clearing',
    'Gecko Form - Clearing Open Evening' : 'Clearing',
    'Gecko Form - Clearing Open Day' : 'Clearing',

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
    'Student Ambassador Page Land' : 'Other Pages',

    'UWE International Global AUD REM' : 'Rare',
    'I4G External Site Link Click' : 'Rare',
    'TDE Event Book Now Click' : 'Rare',
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

if uni == 'ARU' or uni == 'OBU' or uni == 'Solent':
    ### Make the date in the performance file the same format as conversion
    performance_df['Date'] = performance_df['Date'].dt.strftime('%d/%m/%Y')  

# Write out the cleaned data to csv files
performance_df.to_csv("../Clean_data/Clean_performance_%s.csv" % uni, index=False)
conversion_df.to_csv('../Clean_data/Clean_conversion_%s.csv' % uni,index=False)

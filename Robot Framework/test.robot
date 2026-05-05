*** Settings ***
Library    SeleniumLibrary
Library    helper.py

*** Variables ***
${REPORT_FILE}      ${CURDIR}${/}report.html
${PARQUET_FOLDER}   ${CURDIR}${/}parquet_data${/}facility_type_avg_time_spent_per_visit_date
${FILTER_DATE}      2026-04-11

*** Test Cases ***
HTML table should match Parquet data
    Open Browser    file://${REPORT_FILE}   Chrome

    ${table_element}=    Get WebElement       class:table
    ${html_df}=    Read Html Table To Df      ${table_element}
    ${pq_df}=      Read Parquet To Df         ${PARQUET_FOLDER}    ${FILTER_DATE}


    ${match}    ${diff}=    Compare Dataframes    ${html_df}    ${pq_df}
    Run Keyword If    not ${match}    Fail    Data mismatch:\n${diff}
    
    [Teardown]    Close Browser


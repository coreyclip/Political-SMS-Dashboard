cd ../../political_sms_extracts
if [ $? -eq 0 ]
   then
       git add sms_extract.csv
       timestamp=$(date)
       git commit -m 'data update ${timestamp}'
       git push origin main
else
    echo "failed to access extract repo"
fi

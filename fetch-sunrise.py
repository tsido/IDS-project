import requests
from time import sleep

# fetch sunrise info from sunrise API and calclulate the the
# amount of twilight for the given timestamp
# 4 night
# 3 norming atronomical twilight
# 2 morning nautical twilight
# 1 morning civil twilight
# 0 daytime
# 1 evening civil twilight
# 2 eveming nautical twilight
# 3 evening astronomical twilight
def define_light_amount(timestamp, res):
    if (res['astronomical_twilight_begin'] > timestamp):
        return 4
    if (res['astronomical_twilight_begin'] <= timestamp < res['nautical_twilight_begin']):
        return 3
    if (res['nautical_twilight_begin'] <= timestamp < res['civil_twilight_begin']):
        return 2
    if (res['civil_twilight_begin'] <= timestamp < res['sunrise']):
        return 1
    if (res['sunrise'] <= timestamp < res['sunset']):
        return 0
    if (res['sunset'] <= timestamp < res['civil_twilight_end']):
        return -1
    if (res['civil_twilight_end'] <= timestamp < res['nautical_twilight_end']):
        return -2
    if (res['nautical_twilight_end'] <= timestamp < res['astronomical_twilight_end']):
        return -3
    if (res['astronomical_twilight_end'] <= timestamp):
        return -4   
output = open('daylight-api-output.txt', 'w')

def main():
    file = open('coordinates.csv', 'r')
    for row in  file.readlines():
        index, timestamp, lat, long = row.split(',')
        date,time = timestamp.split('T')
        query = "formatted=0&date="+date+"&lat="+lat+"&long="+long
        sleep(0.5)
        r = requests.get('https://api.sunrise-sunset.org/json?'+query)
        res = r.json()

        if (int(index) % 10 == 0):
            print ('Fetching row', str(index))
            output.flush()
        # figure out what twilight mode the time
        # falls between to
        if (res['status'] != 'OK'):
            raise Error('Failed to obtain results from the API')
        lightAmount = define_light_amount(timestamp, res['results'])
        # TODO write the result to new file
        output.write(str(index) +','+
                     timestamp +','+
                     str(lightAmount))
        output.write('\n')
    

    file.close()
    output.close()
    print("API calls completed.")


main()

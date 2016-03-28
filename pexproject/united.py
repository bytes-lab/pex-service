#!/usr/bin/env python 
import os, sys
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
from datetime import timedelta
import time
import customfunction  
import MySQLdb
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import json

def united(origin, destination, searchdate, searchkey):
    #return searchkey
    dt = datetime.datetime.strptime(searchdate, '%Y/%m/%d')
    date = dt.strftime('%Y-%m-%d')
    date_format = dt.strftime('%a, %b %-d')
    payload_date = dt.strftime('%d, %b %Y')
    
   
    currentdatetime = datetime.datetime.now()
    stime = currentdatetime.strftime('%Y-%m-%d %H:%M:%S')
    searchkey = searchkey
    db = customfunction.dbconnection()
    cursor = db.cursor()
    url = "https://www.united.com/ual/en/us/flight-search/book-a-flight/results/awd?f=" + origin + "&t=" + destination + "&d=" + date + "&tt=1&at=1&sc=7&px=1&taxng=1&idx=1"
    
    display = Display(visible=0, size=(800, 600))
    display.start()
    chromedriver = "/usr/bin/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    #driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    #driver.set_window_size(1120, 550)
    
    driver = webdriver.Chrome(chromedriver)
    

    driver.get(url)
    time.sleep(2)
    try:
        driver.execute_script("""
        (function(XHR) {
        "use strict";
        var count = 0;
        var open = XHR.prototype.open;
        var send = XHR.prototype.send;
        XHR.prototype.open = function(method, url, async, user, pass) {
            this._url = url;
            open.call(this, method, url, async, user, pass);
        };
        XHR.prototype.send = function(data) {
            var self = this;
            var oldOnReadyStateChange;
            var url = this._url;
            
            function onReadyStateChange() {
                if(self.readyState == 4) {
                    var json_response = JSON.parse(self.responseText);
                    
                    if(json_response.hasOwnProperty("status") && json_response["status"] == "success" && json_response.hasOwnProperty("data"))
                    {
                        var tripdata = json_response["data"]
                        if(tripdata["Trips"])
                        {
                            var element = document.createElement('div');
                            element.id = "interceptedResponse";
                            element.appendChild(document.createTextNode(""));
                            document.body.appendChild(element);
                            element.appendChild(document.createTextNode(self.responseText));
                            count = count+1;
                       }
                    }
                   
                 
                }
    
                if(oldOnReadyStateChange) {
                    oldOnReadyStateChange();
                }
            }
    
            /* Set xhr.noIntercept to true to disable the interceptor for a particular call */
            if(!this.noIntercept) {            
                if(this.addEventListener) {
                    this.addEventListener("readystatechange", onReadyStateChange, false);
                } else {
                    oldOnReadyStateChange = this.onreadystatechange; 
                    this.onreadystatechange = onReadyStateChange;
                }
            }
    
            send.call(this, data);
        }
    })(XMLHttpRequest);
    UA.Booking.FlightSearch.init();
    
        """)

    
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "interceptedResponse")))
    except:
        print "No data Found"
        display.stop()
        driver.quit()
        cursor.execute ("INSERT INTO pexproject_flightdata (flighno,searchkeyid,scrapetime,stoppage,stoppage_station,origin,destination,departure,arival,duration,maincabin,maintax,firstclass,firsttax,business,businesstax,cabintype1,cabintype2,cabintype3,datasource,departdetails,arivedetails,planedetails,operatedby,economy_code,business_code,first_code) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", ("flag", str(searchkey), stime, "flag", "test", "flag", "flag", "flag", "flag", "flag", "0","0", "0","0", "0", "0", "flag", "flag", "flag", "united", "flag", "flag", "flag", "flag", "flag", "flag", "flag"))
        db.commit()
        return searchkey

    html_page = driver.page_source
    soup = BeautifulSoup(html_page,"xml")
    maindata = soup.findAll("div",{"id":"interceptedResponse"})
    json_string = maindata[0].text
    jsonOb = json.loads(json_string)
    flightDetails = jsonOb["data"]["Trips"][0]["Flights"] #[0]["DepartTimeFormat"]
    
    for i in range(0,len(flightDetails)):
        print "=================================================="+str(i)+"======================================================"
        
        source = flightDetails[i]["Origin"]
        depttime = flightDetails[i]["DepartTimeFormat"]
        test = (datetime.datetime.strptime(depttime, '%I:%M %p'))
        test1 = test.strftime('%H:%M')
        
        
        lastdestination =  flightDetails[i]["LastDestination"]['Code']
        lastdesttime = flightDetails[i]["LastDestination"]['TimeFormatted']
        if '.' in lastdesttime:
            lastdesttime = lastdesttime.replace('.','')
        arivetime1 = (datetime.datetime.strptime(lastdesttime, '%I:%M %p'))
        arivetime = arivetime1.strftime('%H:%M')

        stoppage = flightDetails[i]["StopsandConnections"]
        if stoppage == 0:
            stoppage = "NONSTOP"
        elif stoppage == 1:
            stoppage = "1 STOP"
        else:
            stoppage = str(stoppage)+" STOPS"
        Flightno =flightDetails[i]["FlightNumber"]
        flightcode = flightDetails[i]["OperatingCarrier"]
        Flightno = "Flight "+flightcode+" "+str(Flightno)
        #print "FlightNumber",FlightNumber
        TravelMinutes = flightDetails[i]["TravelMinutes"]
        MaxLayoverTime = flightDetails[i]["MaxLayoverTime"]
        TravelMinutes = TravelMinutes
        firstFlighthour = int(TravelMinutes)/60
        firstFlightminute = int(TravelMinutes) % 60
        firstFlightDuration = str(firstFlighthour)+"h "+str(firstFlightminute)+"m"
        MaxLayoverTime = MaxLayoverTime
        firstFlightTotalTime = TravelMinutes
        TravelMinutesTotal = flightDetails[i]["TravelMinutesTotal"]
        travelhour = int(TravelMinutesTotal)/60
        travelminute = int(TravelMinutesTotal) % 60
        totaltime = str(travelhour)+"h "+str(travelminute)+"m"
        connection =  jsonOb["data"]["Trips"][0]["Flights"][i]["Connections"]
        lastFlightTravelDuration = ''
        if connection:
            lastFlightTravelTime = connection[0]["TravelMinutes"]
            lastFlightTravelhour = lastFlightTravelTime/60
            lastFlightTravelminute = lastFlightTravelTime % 60
            lastFlightTravelDuration = str(lastFlightTravelhour)+"h "+str(lastFlightTravelminute)+"m"
        
        #print "Connections",flightDetails[i]["Connections"]
        
        '''
        connectionFlight = flightDetails[i]["Connections"]
        if connectionFlight != None:
            #connectioninfo = json.loads(connectionFlight)
            print "+++++++++++++++++++++++++++++++++++++++++++++"
            print len(connectionFlight)
            for p in range(0,len(connectionFlight)):
                print "connectioninfo origin",connectionFlight[p]["OriginDescription"]
        '''   
        
        DepartDateFormat = flightDetails[i]["DepartDateFormat"]
        #print "**************Destination*****************/n"
        #print "DestinationDescription", flightDetails[i]["DestinationDescription"]
        DestinationDateTime = flightDetails[i]["DestinationDateTime"]
        lastdestdatetime =  flightDetails[i]["LastDestinationDateTime"]
        #print "******** Extra Info *******************\n"

        
        FlightSegmentJson = flightDetails[i]["FlightSegmentJson"]
        segmentJsonObj = json.loads(FlightSegmentJson)
        #print "segmentJsonObj",segmentJsonObj
        print "=============== segmentJsonObj ====================="
        departdetails = []
        arivaildetails = []
        flightdeatails = []
        operator = []
        for k in range(0,len(segmentJsonObj)):
            print "============= segmentJsonObj "+str(k)+"========================"
            #print "Origin", segmentJsonObj[k]["Origin"]
            FlightNumber = segmentJsonObj[k]["FlightNumber"]
            FlightDate = segmentJsonObj[k]["FlightDate"]
            OriginDescription = segmentJsonObj[k]["OriginDescription"]
            OperatingCarrierCode = segmentJsonObj[k]["OperatingCarrierCode"]
            deptdetail = FlightDate+" | from "+OriginDescription
            departdetails.append(deptdetail)
            stopstation = segmentJsonObj[k]["Stops"]
            if stopstation != None:
                stopnJsonobj = stopstation
                if len(stopnJsonobj) > 0:

                    for l in range(0,len(stopnJsonobj)):
                        print "----------------- stop "+str(l)+"----------------------"
                        stopOrigin = stopnJsonobj[l]["OriginDescription"]
                        stopFlightDate = stopnJsonobj[l]["FlightDate"]
                        stopOriginDetails = stopFlightDate+" from "+stopOrigin
                        departdetails.append(stopOriginDetails)
                        arivaildetails.append(stopOrigin)
                        stopDestination = stopnJsonobj[l]["DestinationDescription"]
                        if stopnJsonobj[l]["Destination"].strip() == lastdestination.strip():
                            destdetail = lastdestdatetime+" at "+stopDestination
                            arivaildetails.append(destdetail)
                        else:
                            fullAriveinfo = DestinationDateTime+" at "+stopDestination
                            arivaildetails.append(fullAriveinfo)
                        print "stopDestination",stopDestination
                        print "stopOrigin",stopOrigin
                        stopOperator = stopnJsonobj[l]["OperatingCarrierDescription"]
                        if stopOperator != None:
                            operator.append(stopOperator)
                        stopFlightNumber = stopnJsonobj[l]["FlightNumber"]
                        stopOperatingCarrierCode = stopnJsonobj[l]["OperatingCarrierCode"]
                        stopflightDetail = stopOperatingCarrierCode+" "+stopFlightNumber
                        stopEquipmentDescription = stopnJsonobj[l]["EquipmentDescription"]
                        stopflightDetail = stopflightDetail+" | "+stopEquipmentDescription
                        flightdeatails.append(stopflightDetail)
            else:
                DestinationDescription = segmentJsonObj[k]["DestinationDescription"]
                if segmentJsonObj[k]["Destination"].strip() == lastdestination.strip():
                    destdetail = lastdestdatetime+" at "+DestinationDescription
                else:
                    destdetail = DestinationDateTime+" at "+DestinationDescription
                arivaildetails.append(destdetail)
                
            operatedby = segmentJsonObj[k]["OperatingCarrierDescription"]
            if operatedby != None:
                operator.append(operatedby)
            
            EquipmentDescription = segmentJsonObj[k]["EquipmentDescription"]
            if source.strip() == segmentJsonObj[k]["Origin"].strip():
                filghtFormat = OperatingCarrierCode+" "+FlightNumber+" | "+EquipmentDescription+" ("+firstFlightDuration+")"
            else:
                filghtFormat = OperatingCarrierCode+" "+FlightNumber+" | "+EquipmentDescription+" ("+lastFlightTravelDuration+")"
            flightdeatails.append(filghtFormat)
            
            
  
        #print "AllEquipmentDisclosures",flightDetails[i]["AllEquipmentDisclosures"]
        
        #print "AirportsStopList",flightDetails[i]["AirportsStopList"]
        #print "TravelMinutes",flightDetails[i]["TravelMinutes"]
        #print "PricesByColumn",flightDetails[i]["PricesByColumn"]
      
        print "=====================price column ============================="
        economy = 0
        ecoTax = 0
        business = 0
        businessTax = 0
        first = 0
        firstTax = 0
        ecoFareClassCode = []
        busFareClassCode = []
        firtFareClassCode = []
        
        ecoFareCode = ''
        businessFareCode =''
        firstFareCode = ''
        for j in range(0, len(flightDetails[i]["Products"])):
            #print "FlightDetails", flightDetails[i]["Products"][j]["FlightDetails"]
            productstype = flightDetails[i]["Products"][j]["DataSourceLabelStyle"]
            pricesMiles = flightDetails[i]["Products"][j]["Prices"]
            tax = 0
            TaxAndFees = flightDetails[i]["Products"][j]["TaxAndFees"]
            if TaxAndFees:
                tax = TaxAndFees["Amount"]
            miles = 0
            if pricesMiles:
                miles = flightDetails[i]["Products"][j]["Prices"][0]["Amount"]
            Description = flightDetails[i]["Products"][j]["Description"]
            BookingCode = flightDetails[i]["Products"][j]["BookingCode"]
            ProductTypeDescription = flightDetails[i]["Products"][j]["ProductTypeDescription"]
            if ProductTypeDescription:
                BookingCode = BookingCode+" "+ProductTypeDescription
            if 'Economy' in productstype and economy == 0  :
                economy = miles
                ecoTax = tax
                ecoFareCode = BookingCode
                ecoFareClassCode.append(BookingCode)
            elif 'Business' in productstype and business == 0 and miles:
                business = miles
                businessTax = tax
                businessFareCode = BookingCode
                busFareClassCode.append(BookingCode)
            elif 'First' in productstype and first == 0 and miles:
                first = miles
                firstTax = tax
                firstFareCode = BookingCode
                firtFareClassCode.append(BookingCode)
        if connection:
            connectingFarecode = connection[0]["Products"]
            for m in range(0,len(connectingFarecode)):
                connectingDescription = connectingFarecode[m]["Description"]
                connectingProductstype = connectingFarecode[m]["DataSourceLabelStyle"]
                connectingBookingCode = connectingFarecode[m]["BookingCode"]
                productdesc = connectingFarecode[m]["ProductTypeDescription"]
                if productdesc:
                    connectingBookingCode = connectingBookingCode+" "+productdesc
                if 'Economy' in connectingProductstype:
                    ecoFareClassCode.append(connectingBookingCode)
                elif 'Business' in connectingProductstype:
                    busFareClassCode.append(connectingBookingCode)
                elif 'First' in connectingProductstype:
                    firtFareClassCode.append(connectingBookingCode)
        if len(ecoFareClassCode) > 0:
            ecoFareCode = '@'.join(ecoFareClassCode)
        if len(busFareClassCode) > 0:
            businessFareCode = '@'.join(busFareClassCode)
        if len(firtFareClassCode) > 0:
           firstFareCode = '@'.join(firtFareClassCode)
        

        
        '''
        print "stoppage",stoppage
        print "totaltime",totaltime
        print "Origin info",source, test1
        print "Final destination",lastdestination, arivetime
        print "economy",economy
        print "business",business
        print "first",first
        print "ecoFareCode",ecoFareCode
        print "businessFareCode",businessFareCode
        print "firstFareCode",firstFareCode
        print "firstTax",firstTax
        print "ecoTax",ecoTax
        print "businessTax",businessTax ''' 
        departdetailsText = '@'.join(departdetails) 
        arivedetailsText = '@'.join(arivaildetails) 
        planedetails = '@'.join(flightdeatails)
        operatedbytext = ''
        
        print operator
        print len(operator)
        if len(operator) > 0: 
            operatedbytext = '@'.join(operator) 
        
        cursor.execute ("INSERT INTO pexproject_flightdata (flighno,searchkeyid,scrapetime,stoppage,stoppage_station,origin,destination,departure,arival,duration,maincabin,maintax,firstclass,firsttax,business,businesstax,cabintype1,cabintype2,cabintype3,datasource,departdetails,arivedetails,planedetails,operatedby,economy_code,business_code,first_code) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", (Flightno, str(searchkey), stime, stoppage, "test", source, lastdestination, test1, arivetime, totaltime, str(economy), str(ecoTax), str(business), str(businessTax), str(first), str(firstTax),"Economy", "Business", "First", "united", departdetailsText, arivedetailsText, planedetails, operatedbytext,ecoFareCode,businessFareCode,firstFareCode))
        db.commit()
        print "row inserted"
    cursor.execute ("INSERT INTO pexproject_flightdata (flighno,searchkeyid,scrapetime,stoppage,stoppage_station,origin,destination,departure,arival,duration,maincabin,maintax,firstclass,firsttax,business,businesstax,cabintype1,cabintype2,cabintype3,datasource,departdetails,arivedetails,planedetails,operatedby,economy_code,business_code,first_code) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", ("flag", str(searchkey), stime, "flag", "test", "flag", "flag", "flag", "flag", "flag", "0","0", "0","0", "0", "0", "flag", "flag", "flag", "united", "flag", "flag", "flag", "flag", "flag", "flag", "flag"))
    db.commit()
    display.stop()
    driver.quit()              
    return searchkey              
        
    #maindata1 = soup.findAll("div",{"id":"interceptedResponse1"})
    '''
    maindata2 = soup.findAll("span",{"id":"interceptedResponse2"})
    maindata3 = soup.findAll("span",{"id":"interceptedResponse3"})
    '''

if __name__=='__main__':
    print "in united"
    united(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])



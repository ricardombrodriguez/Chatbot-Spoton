from django.db import models

# Create your models here.
class Airport(models.Model):
    
    #Hour dfference to GMT exemple for Tahiti = -10 should be int
    gmt = models.CharField()
    #should be int
    airport_id = models.CharField(max_length=10)
    icao_code= models.CharField(max_length=4)
    iata_code= models.CharField(max_length=3)
    city_iata_code = models.CharField(max_length=3)
    #two letter country identifier
    country_code= models.CharField(max_length=2)
    #Postal code should be int
    geoname= models.CharField()
    #both should be decimal field with 9 digits and 6 decimal places 
    latitude=models.CharField(max_length=9)
    longitude=models.CharField(max_length=9)   
    #airport and country name as a string
    aiport_name = models.CharField(max_length=50)
    country_name= models.CharField(max_length=50,nullable=True)
    #phone number for display only
    phone_number= models.CharField(max_length=50,nullable=True)
    #timezone as a string for airport "America/Bogota"
    timezone =   models.CharField(max_length=50) 

class Departure(models.Model):

    airport = models.CharField()
    timezone = models.CharField()
    
    iata = models.CharField()
    icao = models.CharField()
    
    terminal = models.CharField()
    gate = models.CharField()
    
    scheduled = models.CharField()
    estimated = models.CharField()
    
    """
    "airport": "Qingdao",
    "timezone": "Asia/Shanghai",
    "iata": "TAO",
    "icao": "ZSQD",
    "terminal": null,
    "gate": null,
    "delay": null,
    "scheduled": "2022-03-05T07:35:00+00:00",
    "estimated": "2022-03-05T07:35:00+00:00",
    "actual": null,
    "estimated_runway": null,
    "actual_runway": null 
    """
    
    

class Arrival(models.Model):

    airport = models.CharField()
    timezone = models.CharField()
    
    iata = models.CharField()
    icao = models.CharField()
    
    terminal = models.CharField()
    gate = models.CharField()
    
    scheduled = models.CharField()
    estimated = models.CharField()
    

class Airline(models.Model):

    airline_id = int( models.CharField() )
    airline_name = models.CharField() 
    country_name = models.CharField() 
    fleet_size = int( models.CharField() ) 
    status = models.CharField() 
    type = models.CharField() 
    
    callsign = models.CharField()
    hub_code = models.CharField(nullable=True)
    
    iata_code = models.CharField()
    icao_code = models.CharField()
    country_iso2 = models.CharField()
    date_founded = models.CharField()
    
    
    """ 
    "id": "7",
    "fleet_average_age": "11.1",
    "airline_id": "7",
    "callsign": "SKYWEST",
    "hub_code": "SLC",
    "iata_code": "OO",
    "icao_code": "SKW",
    "country_iso2": "UM",
    "date_founded": "1972",
    "iata_prefix_accounting": "302",
    "airline_name": "SkyWest Airlines",
    "country_name": "United States Minor Outlying Islands",
    "fleet_size": "382",
    "status": "active",
    "type": "scheduled" 
    """

class City(models.Model):
    
    city_id =  models.CharField() 
    city_name = models.CharField()
    latitude = models.CharField()
    longitude = models.CharField()
    timezone = models.CharField() 
    
    gmt = models.CharField()
    iata_code = models.CharField()
    country_iso2 = models.CharField()
    
    """ 
    "id": "1",
    "gmt": "-10",
    "city_id": "1",
    "iata_code": "AAA",
    "country_iso2": "PF",
    "geoname_id": null, 
    "latitude": "-17.05",
    "longitude": "-145.41667",
    "city_name": "Anaa",
    "timezone": "Pacific/Tahiti" 
    """

class Country(models.Model):
    ico24 = models.CharField()
    
    country_id = models.CharField()
    country_name = models.CharField()
    capital = models.CharField(nullable=True)
    currency_code = models.CharField(nullable=True)
    currency_name = models.CharField(nullable=True)
    
    continent = models.CharField()
    phone_prefix = models.CharField(nullable=True)
    population = models.CharField(nullable=True)
    
    """  
    "id": "1",
    "capital": "Andorra la Vella",
    "currency_code": "EUR",
    "fips_code": "AN",
    "country_iso2": "AD",
    "country_iso3": "AND",
    "continent": "EU",
    "country_id": "1",
    "country_name": "Andorra",
    "currency_name": "Euro",
    "country_iso_numeric": "20",
    "phone_prefix": "376",
    "population": "84000" 
    """

class Airplane(models.Model):
    ico24 = models.CharField()
    
    airplane_id = int( models.CharField() )
    
    iata_type = models.CharField()
    airline_iata_code = models.CharField() 
    iata_code_long = models.CharField() 
    iata_code_short = models.CharField() 
    airline_icao_code = models.CharField(nullable=True) 
    icao_code_hex = models.CharField() 
    
    construction_number = int( models.CharField() )
    registration_number = models.CharField()
    
    plane_owner = models.CharField()
    plane_series = int( models.CharField() )
    plane_status = models.CharField()
    production_line = models.CharField()
    
    """ 
      "id": "1",
      "iata_type": "B737-300",
      "airplane_id": "1",
      "airline_iata_code": "0B",
      "iata_code_long": "B733",
      "iata_code_short": "733",
      "airline_icao_code": null,
      "construction_number": "23653",
      "delivery_date": "1986-08-21T22:00:00.000Z",
      "engines_count": "2",
      "engines_type": "JET",
      "first_flight_date": "1986-08-02T22:00:00.000Z",
      "icao_code_hex": "4A0823",
      "line_number": "1260",
      "model_code": "B737-377",
      "registration_number": "YR-BAC",
      "test_registration_number": null,
      "plane_age": "31",
      "plane_class": null,
      "model_name": "737",
      "plane_owner": "Airwork Flight Operations Ltd",
      "plane_series": "377",
      "plane_status": "active",
      "production_line": "Boeing 737 Classic",
      "registration_date": "0000-00-00",
      "rollout_date": null """

class Codeshared(models.Model):
        
    airline_name = models.CharField()
    airline_iata = models.CharField()
    airline_icao = models.CharField()
    flight_number = models.CharField()
    flight_iata = models.CharField()
    flight_icao = models.CharField()

class Flight(models.Model):
    
    number = models.CharField()
    iata = models.CharField()
    icao = models.CharField()
    flight_date = models.CharField()
    flight_status = models.CharField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    departure = models.ForeignKey(Departure, on_delete=models.CASCADE)
    arrival = models.ForeignKey(Arrival, on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Airplane, on_delete=models.CASCADE, nullable=True)
    codeshare = models.ForeignKey(Codeshared, on_delete=models.CASCADE, nullable=True)
        
class Question(models.Model):
    pass
    
    
class Answer(models.Model):
    pass
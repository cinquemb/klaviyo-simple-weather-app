# View/Controller Logic #

- create a newsletter sign up page that allows someone to enter their email address and choose their location from a list of the top 100 cities in the US by population. 
- Once they submit their information and it's validated, it should be stored in a database and a confirmation message or page should be displayed
- Keep in mind, the same email address should only be allowed to sign up once.
- extra: use freegoip database and pull data gps coord data 
- use bootstrap and modals for process/html templating


# Management Command Logic # 

- Then create a Django management command or a Python script to send a personalized email to each email address in the list. 
	-For each recipient:
		-In all cases the email should be sent to the recipient's entered email address and come from your email address
		- The body of the email can be formatted however you like.  
			- It should contain a readable version of the recipient's location along with the current temperature and weather. 
			- For example, "55 degrees, sunny."
		- fetch the current weather for that recipient's location and change the subject of the email based on the weather (http://www.wunderground.com/weather/api). 
			- If it's nice outside (either sunny or 5 degrees warmer than the average temperature for that location at that time of year), 
				- the email's subject should be "It's nice out! Enjoy a discount on us." 
			- elif's it's not so nice out (either precipitating or 5 degrees cooler than the average temperature at that time of year),
				 - the subject should be "Not so nice out? That's okay, enjoy a discount on us." 
			- else
				- the email subject should read simply "Enjoy a discount on us." 

			- extra: tie in foursqaures location api (https://developer.foursquare.com/start/search/https://developer.foursquare.com/docs/venues/explore) by searching for venues nearby them and returing top ten cheapest priced items: https://developer.foursquare.com/docs/venues/menu.html 

# Mail server #
- localhost with spoof url addr? 
- sendgrid?

# pg pass # 
echo -n "klaviyo" | shasum -a 256 | awk '{printf("%s%s%s\n","A",substr($1,0,11),"B")}'


# code #

- finish utils (parse out relevant data from fs urls)
- emailing logic from weather api

- debug ui (properly show confirmation/errors)

- debug emails
- sign up for sendgrid
# View/Controller Logic #

- create a newsletter sign up page that allows someone to enter their email address and choose their location from a list of the top 100 cities in the US by population. 
- Once they submit their information and it's validated, it should be stored in a database and a confirmation message or page should be displayed
- Keep in mind, the same email address should only be allowed to sign up once.
- extra: use freegoip database and pull data gps coord data 
- use bootstrap and modals for process/html templating


# Management Command Logic # 

- Then create a Django management command or a Python script to send a personalized email to each email address in the list. 
	-For each recipient:
			- extra: tie in foursqaures location api (https://developer.foursquare.com/start/search/https://developer.foursquare.com/docs/venues/explore) by searching for venues nearby them and returing top ten cheapest priced items: https://developer.foursquare.com/docs/venues/menu.html 

# Mail server #
- localhost with spoof url addr? 
- sendgrid?

# pg pass # 
echo -n "klaviyo" | shasum -a 256 | awk '{printf("%s%s%s\n","A",substr($1,0,11),"B")}'


# code #

- debug data saving
- debug ui (properly show confirmation/errors)

- debug emails
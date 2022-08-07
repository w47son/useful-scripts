#Gets your PUBLIC IP Address and geoIP with the Duckduckgo Api

# Your IP address is x.x.x.x in Madrid, Spain (28005) #

#Add the function to your .zshrc and run it with getip


function getip(){
output="$(curl -s "https://api.duckduckgo.com/?q=ip&format=json&pretty=1" | jq .Answer | tr '><:' '\n' | tr -d '"' | awk 'NR==1; NR==4' | xargs)"

if [ "$output" != "" ]
then
	echo $output
else
	echo "No Internet :("
fi
}
getip

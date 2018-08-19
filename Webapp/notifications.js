var request = require("request");

var options = { method: 'GET',
  url: 'https://api.twilio.com/2010-04-01/Accounts/AC2ebde9587e0410118d41dd76174c2051/Messages.json%27%20-X%20POST%20/%20--data-urlencode%20%27To=+16692924707%27%20/%20--data-urlencode%20%27From=+17343047252%27%20/%20--data-urlencode%20%27Body=Hi,%20Vivek%27%20/%20-u%20AC2ebde9587e0410118d41dd76174c2051:391ee2a219a281a65abdfbdce8cc51cb',
  };

request(options, function (error, response, body) {
  if (error) throw new Error(error);

console.log(body);


});
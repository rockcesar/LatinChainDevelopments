LatinChain Platform
-----------------

Pi, Pi Network and the Pi logo are trademarks of the Pi Community Company.

Original Repository: https://github.com/rockcesar/PiNetworkDevelopments

Institutional Repository: https://github.com/pi-apps/LatinChain

Currently https://latin-chain.com is working with website_pinetwork_odoo and website_pinetwork_games_odoo, made in Odoo.

We won an Honorable mention in Pi Hackathon with our project, Pi Network Games from Latin America!!!:
https://minepi.com/blog/hackathon-winners-announcement

To use these sources codes in Pi Sandbox (https://developers.minepi.com/), put it in the root of HTTP Server: /var/www/html.
In the HTTP Server, where you put these codes, you can use domains or subdomains.

Apps
-----------------

sudoku (MIT License) is the Sudoku Solver. It's a modification of https://github.com/robatron/sudoku.js (MIT License, 2021)
#Put it in the root of HTTP Server: /var/www/html (You can use domains or subdomains)

snake (MIT License) is the Super Snake. It's a modification of https://github.com/iamchrismiller/responsive-snake (MIT License, 2021)
#Put it in the root of HTTP Server: /var/www/html (You can use domains or subdomains)

chess (GPLv3) is the Chess. It's a modification of https://github.com/LabinatorSolutions/stockfish-chess-web-gui (GPLv3, 2021)
#Put it in the root of HTTP Server: /var/www/html (You can use domains or subdomains)

piapp-example (PiOS License) is a test and example of how to use Pi Apps API in a Webpage.
#Put it in the root of HTTP Server: /var/www/html (You can use domains or subdomains)

website_pinetwork_odoo (PiOS License) is a LatinChain Platform (First App in Odoo for Pi).
#Run it in Odoo 13.0 or 14.0 Server. (You can use domains or subdomains)

website_pinetwork_games_odoo (PiOS License) is a LatinChain Platform (Games Engine and Platform in Odoo for Pi).
#Run it in Odoo 13.0 or 14.0 Server. (You can use domains or subdomains)

server1.php is a server side example for PiApps (PiOS License).

In client, for using Sandbox you must set, sandox: true, in Pi.init().

```javascript
  <script src="https://sdk.minepi.com/pi-sdk.js" ></script>
  <script> Pi.init({ version: "2.0", sandbox: true }) </script>
```

Apps published:

LatinChain Platform:
https://latin-chain.com

Pidoku
Snake
Chess
PiApp Example

LatinChain Platform (First App in Odoo for Pi):
https://apps.odoo.com/apps/modules/14.0/website_pinetwork_odoo/

LatinChain Platform (Games Engine and Platform in Odoo for Pi):
https://apps.odoo.com/apps/modules/14.0/website_pinetwork_games_odoo/

Link for info:
https://dev-rockcesar.blogspot.com/2021/05/pi-apps-published.html

Final Presentation of the Apps:
https://www.youtube.com/watch?v=9KqcyAoCZzo
